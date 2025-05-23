from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ذخیره کاربران به صورت دیکشنری (در دنیای واقعی از دیتابیس استفاده کنید)
users = {}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_password_hash = users.get(username)
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = "نام کاربری یا رمز عبور اشتباه است."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            error = "نام کاربری قبلاً ثبت شده است."
            return render_template('register.html', error=error)
        
        users[username] = generate_password_hash(password)
        success = "ثبت نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید."
        return render_template('register.html', success=success)

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
