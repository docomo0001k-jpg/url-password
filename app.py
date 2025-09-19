from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

USERS = {}  # メールアドレスをキー
ADMIN_PASSWORD = "Minato112"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in USERS:
            return 'このメールアドレスは既に登録されています'
        USERS[email] = {'password_hash': generate_password_hash(password)}
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = USERS.get(email)
        if not user or not check_password_hash(user['password_hash'], password):
            return 'ログイン失敗'
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    if not email:
        return redirect('/signin')
    return f'ようこそ {email} さん！'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # 管理者ページはパスワードでアクセス
    if 'admin_auth' not in session:
        if request.method == 'POST':
            password = request.form['admin_password']
            if password == ADMIN_PASSWORD:
                session['admin_auth'] = True
                return redirect(url_for('admin'))
            else:
                return '管理者パスワードが違います'
        return render_template('admin_login.html')
    # 管理者ページ本体
    if request.method == 'POST':
        email = request.form['add_email']
        password = request.form['add_password']
        if email in USERS:
            return 'そのメールアドレスは既に登録済みです'
        USERS[email] = {'password_hash': generate_password_hash(password)}
        return '会員追加しました'
    return render_template('admin.html', users=USERS)

if __name__ == '__main__':
    app.run(debug=True)
