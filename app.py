from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

from routes.auth import auth
from routes.dashboard import dashboard

app.register_blueprint(auth)
app.register_blueprint(dashboard)

if __name__ == '__main__':
    app.run(debug=True)