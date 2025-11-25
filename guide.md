# 🌍 **Trip Splitter**

### *Share expenses with friends. Track everything. Settle instantly.*

A clean, cloud-hosted, real-time trip expense manager built with **Streamlit + MongoDB**.

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-blue?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb" />
  <img src="https://img.shields.io/badge/Python-Backend-yellow?style=for-the-badge&logo=python" />
</p>

---

# ✨ **What Is Trip Splitter?**

Trip Splitter is the easiest way to:

✔ Create trips with friends
✔ Add expenses on the go
✔ Track who paid what
✔ View category breakdowns
✔ Automatically calculate **who owes whom**

**No coding needed.**
Just follow the steps below like a cookbook and start using it for your next Vizag, Goa, or Manali trip.

---

# 🧭 **Table of Contents**

1. 🚀 Quick Start
2. 🍃 Create Your Free MongoDB Database
3. 🍴 Fork This GitHub Repo
4. ☁️ Deploy on Streamlit Cloud
5. 🔐 Add Secrets (MongoDB URI)
6. 🧳 Use the App for Your Trip
7. 📊 Analytics & Settlement
8. ⬇️ Export Options
9. 🔗 Sharing with Friends
10. 🛠️ Developer Notes

---

# 🚀 **Quick Start Summary**

Here’s everything you’ll do:

1️⃣ Create MongoDB database (free)
2️⃣ Fork this repository
3️⃣ Deploy to Streamlit Cloud
4️⃣ Paste your MongoDB URI into secrets
5️⃣ Open your app → create trip → share with friends

That’s it 😄

---

# 🍃 **1. Create Your Free MongoDB Atlas Database**

Your trips & expenses are stored safely in your private cloud database.

---

## 🟢 Step 1: Sign Up

👉 [https://cloud.mongodb.com](https://cloud.mongodb.com)
Choose Google or Email — Free tier is enough.

---

## 🟢 Step 2: Create a Free Cluster

* Choose **M0 Free Tier**
* Select any region
* Click **Create Cluster**

⏳ Takes 1–3 minutes (continue meanwhile)

---

## 🟢 Step 3: Create Database User

Go to **Database Access → Add User**

* Username: `tripuser`
* Password: *strong password*
* Role: **Read and write to any database**

---

## 🟢 Step 4: Allow Network Access

Network Access → Add IP →
🌍 **Allow from anywhere (0.0.0.0/0)** (easy for beginners)

---

## 🟢 Step 5: Copy MongoDB Connection URI

Database → Connect →
**Connect your application**

🔗 Copy your URI:

```
mongodb+srv://tripuser:YOUR_PASSWORD@cluster0.xxxxxx.mongodb.net/
```

💾 Save this for later (we’ll add it to secrets).

---

# 🍴 **2. Fork This Repository**

👉 [https://github.com/prashanth-ds-ml/Trip_splitter](https://github.com/prashanth-ds-ml/Trip_splitter)

Click **Fork** → choose your GitHub account.

Your version will be at:

```
https://github.com/<your-username>/Trip_splitter
```

Done 🎉

---

# ☁️ **3. Deploy on Streamlit Cloud**

Make your app live on the internet — for free.

👉 [https://share.streamlit.io](https://share.streamlit.io)

---

## 🟣 Step 1: Sign In with GitHub

## 🟣 Step 2: Deploy Your App

Click **New App** → Select your fork
Choose:

```
Repository: Trip_splitter
Branch: main
Main file: src/trip_splitter/app.py
```

➡️ Click **Deploy**

Don’t worry if it errors once — that’s because secrets aren’t added yet.

---

# 🔐 **4. Add MongoDB Secrets Safely**

This keeps passwords outside your code — professional & safe.

---

## 🔵 Step 1: Open Secrets

App Page → Menu (⋮) → **Edit App** → **Secrets**

---

## 🔵 Step 2: Paste Secrets

```
[mongo]
uri = "mongodb+srv://tripuser:YOUR_PASSWORD@cluster0.xxxxxx.mongodb.net/"
db_name = "Trips"
```

Replace the URI with your real one.

Save → Restart App

Your app will now fully load ✔

---

# 🧳 **5. Use the Trip Splitter App**

Now the magic begins ✨
On your Streamlit app:

---

## 🟠 Create a new trip

Sidebar → **➕ Create New Trip**

Example:

* Trip Name → *Vizag 2025*
* Participants → *ALICE, BOB, CHARAN, DEEPAK*
* Categories → *Food, Stay, Travel, Activities*

Click **Create Trip**

---

## 🟠 Manage Participants

Sidebar → **👥 Manage Participants**

* Add missing friends
* Remove extra names

These update immediately.

---

# 💸 **6. Add Expenses (Easy & Flexible)**

Main page → **➕ Add New Expense**

### Example 1 — Lunch

* Paid By: ALICE
* Amount: 1600
* Desc: Lunch near RK Beach
* Category: Food
* Exclude: (none)

### Example 2 — Coffee (Only 2 people)

* Paid By: BOB
* Amount: 300
* Exclude: CHARAN, DEEPAK

Click **Add Expense**

Behind the scenes, everything is stored cleanly in MongoDB.

---

# 📊 **7. Analytics & Settlement**

Your dashboard automatically updates with:

### 📌 **Per-person summary**

* Total paid
* Fair share
* Balance (positive = receive, negative = pay)

### 🥧 **Category-wise breakdown**

Pie charts for Food / Travel / Stay etc.

### 🗓️ **Day-wise logs**

Daily expenses + mini charts

### 🧮 **Net balances**

Shows how much each friend owes or is owed.

### 🔁 **Optimized settlement**

Clear instructions:

```
👉 BOB owes ALICE ₹850  
👉 DEEPAK owes CHARAN ₹1200
```

Perfect for end-of-trip settling.

---

# ⬇️ **8. Export Options**

Under **Export Data**:

* Export all expenses (CSV)
* Export per-person summary (CSV)

Great for:
📁 Records,
📤 Google Sheets,
🧾 Audit trail.

---

# 🔗 **9. Share the App With Friends**

Just send your Streamlit URL:

```
https://trip-splitter-<your-username>.streamlit.app
```

Friends can:

* Join instantly
* Select the same trip
* Add/view expenses live
* See balances update in real time

No installs, no accounts — just a link.
Works on phones too 📱

---

# 🛠️ **10. Developer Notes (Optional)**

### 🧱 Tech Stack

* Python
* Streamlit
* MongoDB Atlas
* Pandas
* Altair

### 📁 Project Structure

```
src/
  trip_splitter/
    app.py
    db.py
    logic.py
    ui_components/
    utils/
requirements.txt
README.md
```

### 🔒 Security

MongoDB password is **never** stored in GitHub.
Only inside Streamlit **Secrets Manager**.

---

# 🎉 **You're All Set!**

Your Trip Splitter is now:

✨ Live
✨ Cloud-hosted
✨ Multi-user
✨ Private
✨ Beginner-friendly
✨ Easily shareable

Perfect for Vizag, Goa, Kerala, Ooty, Thailand, or ANY group trip!

---
