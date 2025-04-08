import streamlit as st
from pymongo import MongoClient
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Trip Splitter", layout="wide")

# --- MongoDB Connection ---
client = MongoClient(st.secrets["mongo"]["uri"])
db = client["Trips"]

# --- Trip Selection ---
st.markdown("<h1 style='text-align: center;'>🌊 Trip Expense Splitter 🏄‍♂️</h1>", unsafe_allow_html=True)
trip_name = st.text_input("🧭 Enter Trip Name (e.g. Mulki)", value="Mulki")
trip_collection = db[trip_name]

# --- Participants & Default Categories ---
participants = ["CR", "PALLE", "DOG", "NANI", "BABA", "VACHU", "GODA"]
default_categories = ["Food", "Fuel", "Stay", "Travel", "Activities", "Misc"]

# --- Load Expenses from DB ---
def fetch_expenses():
    return list(trip_collection.find({"type": "expense"}, {"_id": 0}))

expenses = fetch_expenses()

# --- UI to Add Expense ---
st.markdown("---")
st.subheader("➕ Add New Expense")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        paid_by = st.selectbox("👤 Paid By", participants)
        amount = st.number_input("💸 Amount (₹)", min_value=0.0, step=100.0)
        description = st.text_input("📝 Description", placeholder="e.g. Hotel, Taxi")

    with col2:
        all_categories = list({e['category'] for e in expenses}) + default_categories
        all_categories = sorted(list(set(all_categories)))
        category_selection = st.selectbox("🏷️ Select Category", all_categories + ["Other (Type below)"])
        custom_category = ""
        if category_selection == "Other (Type below)":
            custom_category = st.text_input("✏️ Custom Category", placeholder="e.g. Ice Cream, Cigarettes")
            category = custom_category.strip()
        else:
            category = category_selection

    excluded_people = st.multiselect("🙅‍♂️ Exclude people from split (optional)", participants, default=[])

    if st.button("✅ Add Expense"):
        if paid_by and amount > 0 and category:
            included_people = [p for p in participants if p not in excluded_people]
            expense = {
                "type": "expense",
                "paid_by": paid_by,
                "amount": float(amount),
                "description": description,
                "category": category,
                "included": included_people,
                "timestamp": datetime.now().strftime("%Y-%m-%d")
            }
            trip_collection.insert_one(expense)
            st.success(f"🎉 Added ₹{amount:.2f} by {paid_by} under {category}")
            st.rerun()
        else:
            st.warning("⚠️ Please enter all fields including category.")

# --- Logs & History Section ---
st.markdown("---")
st.subheader("🔐 View Trip Summary (Protected)")
password = st.text_input("🔑 Enter password to view history", type="password")

if password == "mulki2024":
    if expenses:
        total = sum(e['amount'] for e in expenses)
        person_spent = defaultdict(float)
        category_spent = defaultdict(float)

        for e in expenses:
            person_spent[e['paid_by']] += e['amount']
            category_spent[e['category']] += e['amount']

        person_owes = defaultdict(float)
        for e in expenses:
            share = e['amount'] / len(e['included'])
            for p in e['included']:
                person_owes[p] += share

        balances = {p: round(person_spent[p] - person_owes[p], 2) for p in participants}

        st.markdown("---")
        st.subheader("💰 Total Trip Cost")
        st.metric("Total", f"₹{total:.2f}")

        with st.expander("📊 Category-wise Expense Breakdown"):
            if category_spent:
                df_cat = pd.DataFrame(list(category_spent.items()), columns=["Category", "Amount"])
                fig, ax = plt.subplots()
                ax.pie(df_cat["Amount"], labels=df_cat["Category"], autopct="%1.1f%%", startangle=90)
                ax.axis("equal")
                st.pyplot(fig)

        with st.expander("🗓️ Day-wise Expense Log"):
            df_exp = pd.DataFrame(expenses)
            df_exp["amount"] = df_exp["amount"].astype(float)
            for date in sorted(df_exp["timestamp"].unique()):
                st.markdown(f"#### 📅 {date}")
                df_day = df_exp[df_exp["timestamp"] == date]
                for _, row in df_day.iterrows():
                    st.write(f"💸 `{row['paid_by']}` paid ₹{row['amount']:.2f} for *{row['description']}* [{row['category']}] (Split among: {', '.join(row['included'])})")
                # Day-wise pie chart
                cat_day = df_day.groupby("category")["amount"].sum().reset_index()
                fig_day, ax_day = plt.subplots()
                ax_day.pie(cat_day["amount"], labels=cat_day["category"], autopct="%1.1f%%", startangle=90)
                ax_day.axis("equal")
                st.pyplot(fig_day)

        with st.expander("📋 Net Balances"):
            for p, b in balances.items():
                if b > 0:
                    st.success(f"✅ {p}: +₹{b:.2f}")
                elif b < 0:
                    st.error(f"❌ {p}: -₹{-b:.2f}")
                else:
                    st.info(f"💤 {p}: Settled")

        with st.expander("🔁 Who Owes Whom"):
            def optimize_settlements(bal):
                creditors = {k: v for k, v in bal.items() if v > 0}
                debtors = {k: -v for k, v in bal.items() if v < 0}
                txns = []
                creditors = dict(sorted(creditors.items(), key=lambda x: -x[1]))
                debtors = dict(sorted(debtors.items(), key=lambda x: -x[1]))
                for d in debtors:
                    for c in creditors:
                        if debtors[d] == 0:
                            break
                        if creditors[c] == 0:
                            continue
                        amt = round(min(debtors[d], creditors[c]), 2)
                        if amt > 0:
                            txns.append((d, c, amt))
                            debtors[d] -= amt
                            creditors[c] -= amt
                return txns

            transactions = optimize_settlements(balances)
            if transactions:
                for frm, to, amt in transactions:
                    st.write(f"👉 `{frm}` owes `{to}` ₹{amt:.2f}")
            else:
                st.success("Everyone is settled. No dues pending!")
else:
    if password:
        st.error("Incorrect password ❌")
