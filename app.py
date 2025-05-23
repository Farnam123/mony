from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from models import db, User

app = Flask(__name__)
app.secret_key = 'secret-key'  # برای فلش مسیج‌ها و سشن‌ها
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return '<h1>خوش آمدید به سایت!</h1>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('این نام کاربری قبلاً ثبت شده است.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('ثبت‌نام با موفقیت انجام شد. اکنون وارد شوید.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login')
def login():
    return '<h2>صفحه ورود (در دست ساخت)</h2>'

if __name__ == '__main__':
    app.run(debug=True)
