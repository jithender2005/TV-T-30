from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db import create_db, get_today_attendance, get_all_attendance, validate_admin

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong key
create_db()

@app.route('/')
def home():
    if 'admin' in session:
        data = get_today_attendance()
        return render_template("index.html", students=data, count=len(data))
    return redirect(url_for('login'))

@app.route('/log')
def full_log():
    if 'admin' in session:
        data = get_all_attendance()
        return render_template("log.html", full_data=data)
    return redirect(url_for('login'))

@app.route('/api/attendance')
def api_attendance():
    if 'admin' not in session:
        return jsonify({"error": "Unauthorized"}), 403
    data = get_today_attendance()
    return jsonify({
        "students": data,
        "count": len(data)
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if validate_admin(username, password):
            session['admin'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
