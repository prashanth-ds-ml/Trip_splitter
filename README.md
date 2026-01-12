# 🌍 **Trip Splitter**

### *A Modern, Cloud-Based Group Expense Manager*

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Web App-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb" />
  <img src="https://img.shields.io/badge/Python-Backend-blue?style=for-the-badge&logo=python" />
</p>

---

# ✨ **What is Trip Splitter?**

**Trip Splitter** is a simple and beautifully designed web app to manage shared expenses during group trips.

Whether you're traveling to **Vizag, Goa, Himachal, Thailand, or Europe** — this app helps you and your friends:

✔ Track who paid what
✔ Split expenses fairly
✔ Manage categories
✔ View analytics
✔ Instantly see **who owes whom**
✔ Export the entire trip spending

All from your phone or browser.
No login. No installations.
Just a clean shared link.

---

Check this out for demo: https://tripsplitter.streamlit.app/

---
# 🧠 **Why We Built This**

Most expense-splitter apps are either:

❌ Too complicated
❌ Require account creation
❌ Filled with ads
❌ Not customizable
❌ Hard to deploy privately

**Trip Splitter solves all of this.**

We wanted:

* A **simple, one-page** interface
* A clean databased-backed approach
* No passwords stored in code
* An app that anyone can deploy for their friends
* Real-time updates
* Professional-grade UI and analytics

This repo helps you deploy your **own** hosted Trip Splitter using:

⚡ Streamlit Cloud
🍃 MongoDB Atlas
🐍 Python
📊 Altair (charts)

---

# 🏗️ **How It’s Built**

Trip Splitter is built with a clean and modular architecture so beginners can understand it — and developers can extend it.

```
src/
 └── trip_splitter/
       ├── app.py            # Main Streamlit app UI
       ├── db.py             # MongoDB connection logic
       ├── logic.py          # Splitting + settlement logic
       ├── ui_components/    # Reusable UI elements
       └── utils/            # Helpers, validation, formatting
```

### 🚀 Frontend

* Built using **Streamlit**
* Responsive sidebar-based navigation
* Auto-refresh UI
* Clean expanders & charts
* Works on **mobile & desktop**

### 🧩 Backend

* Python + MongoDB Atlas
* Collections auto-created
* All write operations validated
* Optimized settlement logic (greedy settlement algorithm)

### 📊 Visualizations

* Powered by **Altair**
* Category breakdowns
* Day-wise trend charts
* Per-person balances
* Exportable CSVs

### 🔐 Security

* No secrets in code
* Database credentials stored safely in **Streamlit Secrets Manager**
* Each user deploys their **own private DB**
* App only reads your secrets — never exposes them

---

# 🔧 **Main Components**

### 🧳 1. Trip Management

* Create multiple trips
* Add/edit participants
* Add custom categories

### 💸 2. Expense Recording

* Select payer
* Add amount & description
* Choose category
* Exclude people from split (optional)
* Timestamp auto-recorded

### 📊 3. Visual Analytics

* Per-person summary
* Pie chart per category
* Daily log view
* Total expense overview

### 🤝 4. Settlement Engine

Automatically computes:

```
ALICE should receive ₹1,200
BOB should pay ₹650
CHARAN should pay ₹550
```

And displays **optimized pairwise settlements**, like:

```
👉 BOB → ALICE: ₹650
👉 CHARAN → ALICE: ₹550
```

### ⬇️ 5. Export System

* Export full raw expenses as CSV
* Export summary as CSV

### 🔗 6. Share With Friends

Once deployed:

* You get a public URL
* Anyone can open on phone
* Everyone sees the same trip data
* Works in real time

---

# 🧭 **How to Deploy & Use the App**

We moved the full, detailed step-by-step beginner guide to:

📄 **guide.md** → *A complete cookbook to set up MongoDB, Streamlit, secrets, and start using the app.*

<p align="center">
  <a href="./guide.md">
    <img src="https://img.shields.io/badge/OPEN%20SETUP%20GUIDE-blue?style=for-the-badge" />
  </a>
</p>

This README gives the high-level overview.
guide.md helps beginners deploy it in < 10 minutes.

---

# 🖼️ **Screenshots**

<p align="center">
  <img src="https://github.com/Vineel-Vaddi/Trip_splitter/blob/9946555aa268791cc6cc62d738e434d6b17a3e25/screenshots/Screenshot%202025-11-25%20052323.png" />
  <br/><br/>
  <img src="https://github.com/Vineel-Vaddi/Trip_splitter/blob/9946555aa268791cc6cc62d738e434d6b17a3e25/screenshots/Screenshot%202025-11-25%20052333.png" />
  <br/><br/>
  <img src="https://github.com/Vineel-Vaddi/Trip_splitter/blob/9946555aa268791cc6cc62d738e434d6b17a3e25/screenshots/Screenshot%202025-11-25%20052350.png" />
</p>

---

# 🛡️ **Features at a Glance**

| Feature                   | Status     |
| ------------------------- | ---------- |
| Create trips              | ✅          |
| Add participants          | ✅          |
| Add expenses              | ✅          |
| Category-wise charts      | ✅          |
| Day-wise logs             | ✅          |
| Net balances              | ✅          |
| Optimized settlements     | ✅          |
| CSV Export                | ✅          |
| Multi-user cloud usage    | ✅          |
| Edit/Delete expense       | 🔜 planned |
| Trip header card redesign | 🔜 planned |

---

# ⚙️ **Tech Stack**

| Layer      | Technology      |
| ---------- | --------------- |
| Frontend   | Streamlit       |
| Backend    | Python          |
| Database   | MongoDB Atlas   |
| Charts     | Altair          |
| Deployment | Streamlit Cloud |
| Storage    | Secrets Manager |

---

# 🤝 **Contributing**

Contributions, issues, and feature requests are welcome!

Want to add a feature?
Feel free to:

* Open an issue
* Submit a pull request
* Help improve UI/UX
* Add new export formats
* Improve settlement algorithms

---

# 🌟 **Credits**

### 👨‍💻 Built by:

**Prashanth**
💼 ML/AI Enthusiast | Independent Researcher | Python

**Vineel**
💼 ML/AI Enthusiast | Independent Researcher | Python

### 🤝 Contributors:

Community contributors are welcome. Add your name after your first PR!

### ❤️ Inspiration:

* The need for an easy, personal, cloud-hosted expense splitter
* Simplicity & accessibility during group travel
* The idea that **deployment should be beginner-friendly**

---

# ⭐ **If You Like the Project**

Please consider giving the repo a **star ⭐**
It helps others discover it and motivates future development.

---

# 🎉 **Enjoy Your Trip — and the Splitting!**

Trip Splitter makes group travel **fair, transparent, and stress-free.**
Happy journeys! 🌄✈️🏖️

---
