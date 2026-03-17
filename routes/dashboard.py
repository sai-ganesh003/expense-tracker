from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    from app import mysql
    cur = mysql.connection.cursor()

    # Get filter values from URL
    category = request.args.get('category', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    # Build query based on filters
    query = "SELECT * FROM expenses WHERE user_id = %s"
    params = [current_user.id]

    if category:
        query += " AND category = %s"
        params.append(category)

    if date_from:
        query += " AND date >= %s"
        params.append(date_from)

    if date_to:
        query += " AND date <= %s"
        params.append(date_to)

    query += " ORDER BY date DESC"

    cur.execute(query, params)
    expenses = cur.fetchall()

    # Total amount spent (all time)
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (current_user.id,))
    total = cur.fetchone()[0] or 0

    # Total count (all time)
    cur.execute("SELECT COUNT(*) FROM expenses WHERE user_id = %s", (current_user.id,))
    count = cur.fetchone()[0]

    # This month's spending
    current_month = datetime.now().strftime('%Y-%m')
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s",
                (current_user.id, current_month))
    month = cur.fetchone()[0] or 0

    cur.close()

    return render_template('dashboard/index.html',
                           user=current_user,
                           expenses=expenses,
                           total=round(total, 2),
                           count=count,
                           month=round(month, 2),
                           category=category,
                           date_from=date_from,
                           date_to=date_to)