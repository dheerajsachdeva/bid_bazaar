import flask
from flask import Flask, render_template, redirect, url_for, flash, request
import werkzeug
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'

# Login manager initialization
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    mobile_number = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return render_template("visitor/index.html")
    # return "Hello, World!"

@app.route('/buy')
@login_required
def buy():
    return render_template("visitor/buy.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.execute(db.select(User).where(User.email == email))
        passcode = db.session.execute(db.select(User).where(User.password == password))
        user = user.scalar()
        passcode = passcode.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not passcode:
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('buy'))
    return render_template("visitor/login.html")


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        new_user = User(
            email= request.form['email'],
            password= request.form['password'],
            name= request.form['name'],
            mobile_number = request.form['mobile_number'],
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flask.flash('Registered successfully.')
        return redirect(url_for('buy'))

    return render_template("visitor/register.html")


@app.route('/logout')
def logout():
    logout_user()
    flask.flash('Logged out successfully.')
    return render_template("visitor/index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)


