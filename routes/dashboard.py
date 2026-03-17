from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    from app import mysql
    cur = mysql.connection.cursor()

    category = request.args.get('category', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

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

    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (current_user.id,))
    total = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM expenses WHERE user_id = %s", (current_user.id,))
    count = cur.fetchone()[0]

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


@dashboard.route('/api/summary')
@login_required
def summary():
    from app import mysql
    cur = mysql.connection.cursor()

    cur.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = %s GROUP BY category", (current_user.id,))
    category_data = cur.fetchall()

    cur.execute("""
        SELECT DATE_FORMAT(date, '%%b %%Y') as month, SUM(amount)
        FROM expenses
        WHERE user_id = %s
        GROUP BY DATE_FORMAT(date, '%%Y-%%m'), DATE_FORMAT(date, '%%b %%Y')
        ORDER BY MIN(date) DESC
        LIMIT 6
    """, (current_user.id,))
    monthly_data = cur.fetchall()
    cur.close()

    return jsonify({
        'categories': [row[0] for row in category_data],
        'category_amounts': [float(row[1]) for row in category_data],
        'months': [row[0] for row in monthly_data],
        'monthly_amounts': [float(row[1]) for row in monthly_data]
    })