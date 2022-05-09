from flask import Flask, redirect, render_template
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user
import os
from database.db_session import create_session
from database.user import User
from resources.routes import init_routes
from resources.jwt_init import init_jwt

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = os.urandom(16).hex()
app.config["JWT_SECRET_KEY"] = os.urandom(16).hex()


login_manager = LoginManager()
login_manager.init_app(app)

init_jwt(app)
init_routes(api)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    with session.begin():
        user = session.query(User).get(user_id)
        session.expunge(user)
    return user


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/news')
def news():
    return render_template('news.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
