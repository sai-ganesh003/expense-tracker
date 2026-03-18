from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
import csv
import io

expenses = Blueprint('expenses', __name__)

@expenses.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add():
    from app import mysql
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (%s, %s, %s, %s, %s)",
                    (current_user.id, amount, category, date, description))
        mysql.connection.commit()
        cur.close()
        flash('Expense added!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('dashboard/add.html')


@expenses.route('/expenses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    from app import mysql
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        description = request.form['description']

        cur.execute("UPDATE expenses SET amount=%s, category=%s, date=%s, description=%s WHERE id=%s AND user_id=%s",
                    (amount, category, date, description, id, current_user.id))
        mysql.connection.commit()
        cur.close()
        flash('Expense updated!', 'success')
        return redirect(url_for('dashboard.index'))

    cur.execute("SELECT * FROM expenses WHERE id=%s AND user_id=%s", (id, current_user.id))
    expense = cur.fetchone()
    cur.close()
    return render_template('dashboard/edit.html', expense=expense)


@expenses.route('/expenses/delete/<int:id>')
@login_required
def delete(id):
    from app import mysql
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id=%s AND user_id=%s", (id, current_user.id))
    mysql.connection.commit()
    cur.close()
    flash('Expense deleted!', 'success')
    return redirect(url_for('dashboard.index'))


@expenses.route('/expenses/export')
@login_required
def export():
    from app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, category, description, amount FROM expenses WHERE user_id = %s ORDER BY date DESC",
                (current_user.id,))
    all_expenses = cur.fetchall()
    cur.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Category', 'Description', 'Amount (INR)'])
    for expense in all_expenses:
        writer.writerow(expense)

    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=expenses.csv'}
    )