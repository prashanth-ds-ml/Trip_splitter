# src/trip_splitter/app.py
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pymongo import MongoClient

from .config import get_config
from .utils import compute_balances, optimize_settlements

st.set_page_config(page_title="Trip Splitter", layout="wide")


# ---------- DB & CONFIG ----------

cfg = get_config(st_secrets=st.secrets if hasattr(st, "secrets") else None)
mongo_uri = cfg["mongo"]["uri"]
db_name = cfg["mongo"]["db_name"]

if not mongo_uri:
    st.error(
        "MongoDB URI is not configured.\n\n"
        "Set it via environment variables, Streamlit secrets, or run `trip-splitter init` locally."
    )
    st.stop()

client = MongoClient(mongo_uri)
db = client[db_name]

TRIP_CONFIG_COLLECTION = db["_trip_configs"]


# ---------- SIDEBAR: TRIP MANAGEMENT ----------

with st.sidebar:
    st.title("🗺️ Trips")

    # Load existing trips
    trip_docs = list(TRIP_CONFIG_COLLECTION.find({}, {"_id": 0}))
    trip_names = [t["trip_name"] for t in trip_docs]

    selected_trip = st.selectbox(
        "Select trip",
        options=["-- Select a trip --"] + trip_names,
        index=0,
    )

    st.markdown("---")
    with st.expander("➕ Create new trip"):
        with st.form("new_trip_form"):
            new_trip_name = st.text_input("Trip name", placeholder="e.g. Mulki Surf Trip 2026")
            participants_input = st.text_input(
                "Participants (comma-separated)",
                placeholder="e.g. CR, PALLE, DOG, NANI, BABA, VACHU, GODA",
            )
            categories_input = st.text_input(
                "Categories (comma-separated)",
                value="Food, Fuel, Stay, Travel, Activities, Misc",
            )
            create_btn = st.form_submit_button("Create trip")

        if create_btn:
            if not new_trip_name.strip():
                st.warning("Trip name cannot be empty.")
            elif not participants_input.strip():
                st.warning("Please enter at least one participant.")
            elif new_trip_name in trip_names:
                st.warning("A trip with this name already exists. Choose a different name.")
            else:
                participants = [p.strip() for p in participants_input.split(",") if p.strip()]
                categories = [c.strip() for c in categories_input.split(",") if c.strip()]
                TRIP_CONFIG_COLLECTION.insert_one(
                    {
                        "trip_name": new_trip_name,
                        "participants": participants,
                        "categories": categories,
                        "created_at": datetime.now().isoformat(),
                    }
                )
                st.success(f"Trip '{new_trip_name}' created. Select it from the dropdown above.")
                st.experimental_rerun()


# ---------- MAIN HEADER ----------

st.markdown("<h1 style='text-align: center;'>🌊 Trip Expense Splitter 🏄‍♂️</h1>", unsafe_allow_html=True)

if not selected_trip or selected_trip == "-- Select a trip --":
    st.info("Select a trip from the sidebar or create a new one to get started.")
    st.stop()

# Load selected trip config
trip_config = TRIP_CONFIG_COLLECTION.find_one({"trip_name": selected_trip}, {"_id": 0})
if not trip_config:
    st.error("Selected trip configuration not found. Please re-create the trip.")
    st.stop()

participants = trip_config.get("participants", [])
default_categories = trip_config.get(
    "categories",
    ["Food", "Fuel", "Stay", "Travel", "Activities", "Misc"],
)

trip_collection = db[selected_trip]


# ---------- LOAD EXPENSES ----------

def fetch_expenses():
    return list(trip_collection.find({"type": "expense"}, {"_id": 0}))


expenses = fetch_expenses()


# ---------- ADD EXPENSE UI ----------

st.markdown("---")
st.subheader(f"➕ Add New Expense – {selected_trip}")

if not participants:
    st.warning("This trip has no participants configured. Edit the trip config in MongoDB.")
else:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            paid_by = st.selectbox("👤 Paid By", participants)
            amount = st.number_input("💸 Amount (₹)", min_value=0.0, step=100.0)
            description = st.text_input("📝 Description", placeholder="e.g. Hotel, Taxi")

        with col2:
            existing_cats = list({e.get("category", "") for e in expenses if e.get("category")})
            all_categories = sorted(list(set(existing_cats + default_categories)))
            category_selection = st.selectbox(
                "🏷️ Select Category",
                all_categories + ["Other (Type below)"],
            )
            custom_category = ""
            if category_selection == "Other (Type below)":
                custom_category = st.text_input("✏️ Custom Category", placeholder="e.g. Ice Cream, Cigarettes")
                category = custom_category.strip()
            else:
                category = category_selection

        excluded_people = st.multiselect(
            "🙅‍♂️ Exclude people from split (optional)",
            participants,
            default=[],
        )

        if st.button("✅ Add Expense", use_container_width=True):
            if paid_by and amount > 0 and category:
                included_people = [p for p in participants if p not in excluded_people]
                if not included_people:
                    st.warning("At least one person must be included in the split.")
                else:
                    expense = {
                        "type": "expense",
                        "paid_by": paid_by,
                        "amount": float(amount),
                        "description": description,
                        "category": category,
                        "included": included_people,
                        "timestamp": datetime.now().strftime("%Y-%m-%d"),
                    }
                    trip_collection.insert_one(expense)
                    st.success(f"🎉 Added ₹{amount:.2f} by {paid_by} under {category}")
                    st.experimental_rerun()
            else:
                st.warning("⚠️ Please enter all fields including category and a positive amount.")


# ---------- SUMMARY: TOTAL TRIP COST ----------

if expenses:
    total, balances, person_spent, person_owes, category_spent = compute_balances(
        expenses, participants
    )

    st.markdown("---")
    st.subheader("💰 Total Trip Cost")
    st.metric("Total Spent So Far", f"₹{total:.2f}")
else:
    st.info("No expenses yet. Add your first expense above.")
    st.stop()


# ---------- CATEGORY-WISE BREAKDOWN ----------

with st.expander("📊 Category-wise Expense Breakdown"):
    if category_spent:
        df_cat = pd.DataFrame(
            [{"Category": cat, "Amount": amt} for cat, amt in category_spent.items()]
        )
        fig, ax = plt.subplots()
        ax.pie(df_cat["Amount"], labels=df_cat["Category"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.write("No category data yet.")


# ---------- DAY-WISE EXPENSE LOG ----------

with st.expander("🗓️ Day-wise Expense Log"):
    df_exp = pd.DataFrame(expenses)
    if not df_exp.empty:
        df_exp["amount"] = df_exp["amount"].astype(float)
        for date in sorted(df_exp["timestamp"].unique()):
            st.markdown(f"#### 📅 {date}")
            df_day = df_exp[df_exp["timestamp"] == date]
            for _, row in df_day.iterrows():
                included_str = ", ".join(row.get("included", []))
                st.write(
                    f"💸 `{row['paid_by']}` paid ₹{row['amount']:.2f} for "
                    f"*{row.get('description', '')}* [{row.get('category', '')}] "
                    f"(Split among: {included_str})"
                )

            # Day-wise pie chart
            cat_day = df_day.groupby("category")["amount"].sum().reset_index()
            fig_day, ax_day = plt.subplots()
            ax_day.pie(
                cat_day["amount"],
                labels=cat_day["category"],
                autopct="%1.1f%%",
                startangle=90,
            )
            ax_day.axis("equal")
            st.pyplot(fig_day)
    else:
        st.write("No expenses to display yet.")


# ---------- NET BALANCES ----------

with st.expander("📋 Net Balances"):
    for p in participants:
        b = balances.get(p, 0.0)
        if b > 0:
            st.success(f"✅ {p}: +₹{b:.2f}")
        elif b < 0:
            st.error(f"❌ {p}: -₹{-b:.2f}")
        else:
            st.info(f"💤 {p}: Settled")


# ---------- WHO OWES WHOM ----------

with st.expander("🔁 Who Owes Whom"):
    transactions = optimize_settlements(balances)
    if transactions:
        for frm, to, amt in transactions:
            st.write(f"👉 `{frm}` owes `{to}` ₹{amt:.2f}")
    else:
        st.success("Everyone is settled. No dues pending!")
