# 💰 Expense Tracker

A full-stack web application to track your daily expenses, built with Python and Flask.

## 🌐 Live Demo
https://expense-tracker-7qcz.onrender.com/login

## ✨ Features
- User Registration & Login with secure password hashing
- Add, Edit, Delete expenses
- Categories — Food, Travel, Bills, Shopping, Health, Entertainment, Education
- Filter expenses by category and date range
- Dashboard with stats — Total spent, count, this month
- Doughnut chart — spending by category
- Bar chart — monthly spending
- CSV Export — download all expenses as spreadsheet

## 🛠️ Tech Stack
- **Backend** — Python, Flask
- **Database** — MySQL
- **Frontend** — HTML, CSS, Jinja2
- **Charts** — Chart.js
- **Auth** — Flask-Login, bcrypt
- **Hosting** — Render
- **Database Hosting** — Aiven

## 📁 Project Structure
expense-tracker/
├── app.py
├── config.py
├── requirements.txt
├── Procfile
├── models/
│   └── user.py
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   └── expenses.py
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── dashboard/
│       ├── index.html
│       ├── add.html
│       └── edit.html
└── static/
    ├── css/style.css
    └── js/charts.js

## 🚀 Run Locally
git clone https://github.com/sai-ganesh003/expense-tracker
cd expense-tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

## 👨‍💻 Developer
Kolusu Sai Ganesh
