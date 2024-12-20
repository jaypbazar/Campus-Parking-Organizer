from flask import Flask, request, session, redirect, render_template, url_for, flash
from backend import *

app = Flask(__name__)
app.secret_key = '@SE_S3cr3t_K3y!'
app.config['REMEMBER_COOKIE_REFRESH_EACH_REQUEST'] = False

@app.route('/')
def index():
    session['no_of_available_lots'] = 0
    try:
        conn = connectSQL()
        cursor = conn.cursor()

        query = "SELECT * FROM parking_lots"

        cursor.execute(query) 

        # Convert database results to a list of dictionaries
        lots = []
        for row in cursor.fetchall():
            lots.append({
                'name': row[0],
                'coords': [[row[1], row[2]], [row[3], row[4]]],
                'status': row[5]
            })
            if row[5] == 'available':
                session['no_of_available_lots'] += 1

    except Exception as e:
        print(f"Index Error: {e}")
        lots = []  # Ensure lots is defined even if there's an error
        color = '#6aff00'

    if session.get('no_of_available_lots') > 2: 
        color = '#34ff12'
    elif session.get('no_of_available_lots') > 0:
        color = '#ffff00'
    else: 
        color = '#ff2828'

    return render_template("index.html", parkingLots=lots, available_lots=session.get('no_of_available_lots'), color=color)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for("index"))
    
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
                session['role'] = user[4]

                if session.get('role') == "admin":
                    return redirect(url_for('adminPanel'))

                return(redirect(url_for('index')))
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
    if 'user_id' in session:
        return redirect(url_for("index"))
    
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
            flash("Sign up error. Please try again.", "danger")
                
    return render_template('signup.html')

@app.route('/booking', methods=["POST", "GET"])
def booking():
    if 'user_id' in session:
        parkingLot = request.form.get('parkingSpace')
        bookingDate = request.form.get('reservationDate')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')

        try:
            conn = connectSQL()
            cursor = conn.cursor()

            query = "INSERT INTO bookings VALUES(%s, %s, %s, %s, %s)"
            values = (parkingLot, bookingDate, startTime, endTime, session.get('user_id'))

            cursor.execute(query, values)
            conn.commit()

            query = "UPDATE parking_lots SET status = %s WHERE name = %s"
            values = ('reserved', parkingLot)
            
            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            
        except Exception as e:
            flash("Reservation failed. Try again.", "danger")
            print(f"Booking Error: {e}")

        flash("Reserved Successfully.", "success")
        return redirect(url_for("index"))

    return redirect(url_for("index"))

@app.route('/update_booking', methods=["POST"])
def update_booking():
    parkingLotName = request.form.get('lot_name')
    bookingDate = request.form.get('booking_date')
    startTime = request.form.get('time_start')
    endTime = request.form.get('time_end')

    try:
        conn = connectSQL()
        cursor = conn.cursor()

        query = "UPDATE bookings SET bookingDate = %s, timeStarted = %s, timeEnded = %s WHERE lotName = %s"
        values = (bookingDate, startTime, endTime, parkingLotName)

        cursor.execute(query, values)
        conn.commit()

        flash("Reservation updated successfully.", "success")

        cursor.close()
        conn.close()
    
    except Exception as e:
        flash("Error updating reservation.", "danger")
        print(f"Reservation Update Error: {e}")

    return redirect(url_for('adminPanel'))

@app.route('/delete_booking', methods=["POST"])
def delete_booking():
    parkingLotName = request.form.get('lotName')

    try:
        conn = connectSQL()
        cursor = conn.cursor()

        query = "DELETE FROM bookings WHERE lotName = %s"
        values = (parkingLotName,)

        cursor.execute(query, values)
        conn.commit()

        query = "UPDATE parking_lots SET status = %s WHERE name = %s"
        values = ('available', parkingLotName)

        cursor.execute(query, values)
        conn.commit()

        flash("Reservation removed successfully.", "success")

        cursor.close()
        conn.close()

    except Exception as e:
        flash("Error in deleting reservation.", "danger")
        print(f"Deleting Error: {e}")
    
    return redirect(url_for('adminPanel'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

@app.route('/adminPanel')
def adminPanel():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            try:
                conn = connectSQL()
                cursor = conn.cursor()

                query = "SELECT * FROM parking_lots"
                cursor.execute(query) 

                lots = cursor.fetchall()

                query = "SELECT * FROM bookings"
                cursor.execute(query)

                bookings = cursor.fetchall()

            except Exception as e:
                print(f"Admin Panel Error: {e}")
                
            return render_template('adminPanel.html', parkingLots=lots, reservations=bookings)
        
        flash("Access denied! Only admins are allowed.", "danger")
        return redirect(url_for("index"))
    
    flash("You must log in first.", "danger")
    return redirect(url_for("login"))

@app.route('/update_status', methods=["POST"])
def update_status():
    lotName = request.form.get('lot_name')
    status = request.form.get('status')

    try:
        conn = connectSQL()
        cursor = conn.cursor()

        query = "UPDATE parking_lots SET status = %s WHERE name = %s"
        values = (status, lotName)

        cursor.execute(query, values)
        conn.commit()

        flash("Parking status updated successfully.", "success")

        cursor.close()
        conn.close()

    except Exception as e:
        flash("Error updating details. Try again.", "danger")
        print(f"Update Error: {e}")

    return redirect(url_for('adminPanel'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
