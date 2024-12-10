from flask import Flask, request, session, redirect, render_template, url_for, flash
from backend import connectSQL, encrypt

app = Flask(__name__)
app.secret_key = '@SE_S3cr3t_K3y!'
app.config['REMEMBER_COOKIE_REFRESH_EACH_REQUEST'] = False

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/login', methods=["GET", "POST"])
def login():
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

                return redirect(url_for('index', id = session['user_id']))

            else:
                flash("Wrong email or password. Please try again.", "danger")

            cursor.close()
            conn.close()

        except Exception as e:
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

def validate_duplicate(column_name: str, data: str) -> None:
    '''
A function that validates the user input from a form for its uniqueness
    
Parameters:
    column_name - the name of the table column from the database
    
    data - the current value to validate
    
Returns:
    redirect() - redirects the user to same page then display error message if duplicate'''
    
    try:
        conn = connectSQL()
        cursor = conn.cursor()

        query = f"SELECT {column_name} FROM users"
        cursor.execute(query)

        data = data.lower()
        list = [row[0].lower() for row in cursor.fetchall()]

        cursor.close()
        print(data)
        print(list)

        if data in list: 
            flash(f"Error: {column_name} already exists!", "danger")
            return redirect(url_for('signup'))

    except Exception as e:
        print(f"Database Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
