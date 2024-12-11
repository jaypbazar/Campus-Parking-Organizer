from flask import Flask, request, session, redirect, render_template, url_for, flash
from backend import *

app = Flask(__name__)
app.secret_key = '@SE_S3cr3t_K3y!'
app.config['REMEMBER_COOKIE_REFRESH_EACH_REQUEST'] = False

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', id = session['user_id'])
    
    return render_template("index.html")

@app.route('/about')
def about():
    if 'user_id' in session:
        return render_template('about.html', id = session['user_id'])
    
    return render_template('about.html')

@app.route('/terms')
def terms():
    if 'user_id' in session:
        return render_template('terms.html', id = session['user_id'])

    return render_template('terms.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for("index", id = session['user_id']))
    
    if request.method == "POST":
        user_id = request.form.get('id')
        password = encrypt(request.form.get('password'))
        
        try:
            conn = connectSQL()
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE ID = %s AND Password = %s"
            values = (user_id, password)

            cursor.execute(query, values)

            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]

                if user[4] == "admin":
                    return redirect(url_for('adminPanel', id = session['user_id']))

                return redirect(url_for('index', id = session['user_id']))

            else:
                session.clear()
                flash("Wrong email or password. Please try again.", "danger")

            cursor.close()
            conn.close()

        except Exception as e:
            session.clear()
            flash("Login failed. Please try again.", "danger")
            print(f"Login Error: {e}")
    
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = request.form.get("id")
        firstname = request.form.get("fname")
        middlename = request.form.get("mname")
        lastname = request.form.get("lname")
        role = request.form.get("role")
        contact = request.form.get("contact")
        email = request.form.get("email")
        password = encrypt(request.form.get("password"))

        validate_duplicate("ID", user_id)
        validate_duplicate("CspcEmail", email)

        try:
            conn = connectSQL()
            cursor = conn.cursor()

            query = "INSERT INTO users (ID, FirstName, MiddleName, LastName, Role, CspcEmail, PhoneNumber, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (user_id, firstname, middlename, lastname, role, email, contact, password)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

            flash("Registered successfully.", "success")
            return render_template("login.html")

        except Exception as e:
            print(f"Signup Error: {e}")
                
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

@app.route('/adminPanel/<user_id>')
def adminPanel(user_id):
    if 'user_id' in session:
        return render_template('adminPanel.html', id = session['user_id'])
    
    flash("You must log in first.", "danger")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
