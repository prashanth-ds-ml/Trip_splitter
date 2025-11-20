from __future__ import annotations

from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pymongo import MongoClient

from config import get_config
from utils import compute_balances, optimize_settlements

st.set_page_config(page_title="Trip Splitter", layout="wide")


# ---------- DB & CONFIG ----------

# Safely try to access st.secrets (works on Streamlit Cloud, and locally if .streamlit/secrets.toml exists)
try:
    st_secrets = st.secrets
except Exception:
    st_secrets = None

try:
    cfg = get_config(st_secrets=st_secrets)
except RuntimeError as e:
    st.error(str(e))
    st.stop()

mongo_uri = cfg["mongo"]["uri"]
db_name = cfg["mongo"]["db_name"]

client = MongoClient(mongo_uri)
db = client[db_name]

# Trip config collection; you said yours is "Trip_names"
TRIP_CONFIG_COLLECTION = db["Trip_names"]  # change if you prefer a different name


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
    # ---- Create new trip ----
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

    # ---- Manage participants for selected trip ----
    if selected_trip and selected_trip != "-- Select a trip --":
        st.markdown("---")
        with st.expander("👥 Manage participants"):
            # Fetch latest participants for this trip
            trip_cfg = TRIP_CONFIG_COLLECTION.find_one(
                {"trip_name": selected_trip}, {"_id": 0, "participants": 1}
            )
            current_participants = trip_cfg.get("participants", []) if trip_cfg else []

            if current_participants:
                st.caption("Current participants:")
                st.write(", ".join(current_participants))
            else:
                st.caption("No participants configured yet.")

            new_participant = st.text_input(
                "Add new participant",
                placeholder="e.g. NEW_FRIEND",
                key="add_participant_input",
            )

            if st.button("Add participant", key="add_participant_button"):
                np_clean = new_participant.strip()
                if not np_clean:
                    st.warning("Participant name cannot be empty.")
                elif np_clean in current_participants:
                    st.info(f"'{np_clean}' is already in the participant list.")
                else:
                    TRIP_CONFIG_COLLECTION.update_one(
                        {"trip_name": selected_trip},
                        {"$addToSet": {"participants": np_clean}},
                    )
                    st.success(f"Added '{np_clean}' to participants.")
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
    # Keep _id so we can edit/delete
    return list(trip_collection.find({"type": "expense"}))


expenses = fetch_expenses()


# ---------- ADD EXPENSE UI ----------

st.markdown("---")
st.subheader(f"➕ Add New Expense – {selected_trip}")

if not participants:
    st.warning("This trip has no participants configured. Add participants in the sidebar.")
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
                custom_category = st.text_input(
                    "✏️ Custom Category", placeholder="e.g. Ice Cream, Cigarettes"
                )
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


# ---------- SUMMARY DATA ----------

if not expenses:
    st.info("No expenses yet. Add your first expense above.")
    st.stop()

total, balances, person_spent, person_owes, category_spent = compute_balances(
    expenses, participants
)

# Build a reusable DataFrame of expenses (for logs, edit/delete, export)
df_exp = pd.DataFrame(expenses)
if not df_exp.empty:
    if "amount" in df_exp.columns:
        df_exp["amount"] = df_exp["amount"].astype(float)


# ---------- TRIP HEADER METRICS ----------

st.markdown("---")
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Trip", selected_trip)
with m2:
    st.metric("Participants", len(participants))
with m3:
    st.metric("Total Spent", f"₹{total:.2f}")


# ---------- PER-PERSON SUMMARY ----------

with st.expander("👥 Per-person summary"):
    summary_rows = []
    for p in participants:
        summary_rows.append(
            {
                "Participant": p,
                "Total paid (₹)": round(person_spent.get(p, 0.0), 2),
                "Fair share (₹)": round(person_owes.get(p, 0.0), 2),
                "Balance (₹)": round(balances.get(p, 0.0), 2),
            }
        )
    df_summary = pd.DataFrame(summary_rows)
    st.dataframe(df_summary, use_container_width=True)


# ---------- CATEGORY-WISE BREAKDOWN ----------

with st.expander("📊 Category-wise expense breakdown"):
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

with st.expander("🗓️ Day-wise expense log"):
    if not df_exp.empty:
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

with st.expander("📋 Net balances by person"):
    for p in participants:
        b = balances.get(p, 0.0)
        if b > 0:
            st.success(f"✅ {p}: +₹{b:.2f}")
        elif b < 0:
            st.error(f"❌ {p}: -₹{-b:.2f}")
        else:
            st.info(f"💤 {p}: Settled")


# ---------- WHO OWES WHOM (SETTLEMENTS) ----------

with st.expander("🔁 Optimized settlements (who owes whom)"):
    transactions = optimize_settlements(balances)
    if transactions:
        for frm, to, amt in transactions:
            st.write(f"👉 `{frm}` owes `{to}` ₹{amt:.2f}")
    else:
        st.success("Everyone is settled. No dues pending!")


# ---------- EDIT / DELETE EXPENSES ----------

with st.expander("✏️ Edit or delete expenses"):
    if df_exp.empty:
        st.write("No expenses to edit or delete.")
    else:
        # Build a human-readable label for each expense
        def make_label(row):
            return (
                f"{row.get('timestamp', '')} | {row.get('paid_by', '')} "
                f"paid ₹{row.get('amount', 0):.2f} for {row.get('description', '')} "
                f"[{row.get('category', '')}]"
            )

        df_exp["__label__"] = df_exp.apply(make_label, axis=1)

        selected_label = st.selectbox(
            "Select an expense to edit or delete",
            options=df_exp["__label__"].tolist(),
        )

        selected_row = df_exp[df_exp["__label__"] == selected_label].iloc[0]
        selected_id = selected_row["_id"]

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            edit_paid_by = st.selectbox(
                "Paid by",
                participants,
                index=participants.index(selected_row["paid_by"])
                if selected_row["paid_by"] in participants
                else 0,
            )
            edit_amount = st.number_input(
                "Amount (₹)",
                value=float(selected_row["amount"]),
                min_value=0.0,
                step=100.0,
            )
            edit_description = st.text_input(
                "Description",
                value=selected_row.get("description", ""),
            )

        with col_e2:
            edit_category = st.text_input(
                "Category",
                value=selected_row.get("category", ""),
            )
            edit_included = st.multiselect(
                "Included in split",
                participants,
                default=selected_row.get("included", participants),
            )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("💾 Save changes"):
                if not edit_included:
                    st.warning("At least one participant must be included in the split.")
                else:
                    trip_collection.update_one(
                        {"_id": selected_id},
                        {
                            "$set": {
                                "paid_by": edit_paid_by,
                                "amount": float(edit_amount),
                                "description": edit_description,
                                "category": edit_category,
                                "included": edit_included,
                            }
                        },
                    )
                    st.success("Expense updated.")
                    st.experimental_rerun()
        with col_b2:
            if st.button("🗑️ Delete this expense"):
                trip_collection.delete_one({"_id": selected_id})
                st.success("Expense deleted.")
                st.experimental_rerun()


# ---------- EXPORT DATA ----------

with st.expander("⬇ Export data"):
    if df_exp.empty:
        st.write("No expenses to export.")
    else:
        export_df = df_exp.drop(columns=["_id", "__label__"], errors="ignore")
        csv_exp = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download expenses as CSV",
            data=csv_exp,
            file_name=f"{selected_trip}_expenses.csv",
            mime="text/csv",
        )

        csv_summary = df_summary.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download per-person summary as CSV",
            data=csv_summary,
            file_name=f"{selected_trip}_summary.csv",
            mime="text/csv",
        )
