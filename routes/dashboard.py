from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    from app import mysql
    cur = mysql.connection.cursor()

    # Get all expenses for this user
    cur.execute("SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC", (current_user.id,))
    expenses = cur.fetchall()

    # Total amount spent
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (current_user.id,))
    total = cur.fetchone()[0] or 0

    # Total count
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
                           month=round(month, 2))