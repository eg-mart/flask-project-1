from flask import Flask, redirect, render_template
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_assets import Environment, Bundle
import os
import shutil
from database.db_session import create_session
from database.user import User
from resources.bookings_resources import BookingResource, BookingListResource
import locale
from webassets.filter import get_filter

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = os.urandom(16).hex()

assets = Environment(app)

try:
    shutil.rmtree('static/.webassets-cache')
    shutil.rmtree('static/dist')
except Exception as e:
    pass

bundles = {
    'js_all': Bundle(Bundle('assets/js/app.js', filters='jsmin'),
                     'assets/js/vendor/bootstrap/bootstrap.bundle.min.js',
                     output='dist/assets/js/app.js'),

    'css_all': Bundle('assets/scss/style.scss', filters='libsass,cssmin',
                      output='dist/assets/css/scss.css'),
}
assets.register(bundles)

# sass =
# all_css = Bundle(sass, filters='cssmin', output="dist/assets/css/style.css")
# assets.register('css_all', all_css)

login_manager = LoginManager()
login_manager.init_app(app)

api.add_resource(BookingListResource, '/bookings')
api.add_resource(BookingResource, '/bookings/<booking_id>')


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
    return render_template('index.html', title="Тайм-кафе Loft | Антикафе Саратов")


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
