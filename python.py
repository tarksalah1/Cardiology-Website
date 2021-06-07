from types import MethodType
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm

from flask_mail import Message, Mail
import mysql.connector

mail = Mail()


app = Flask(__name__)

app.secret_key = 'your secret key'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'tarksalah@gmail.com'
app.config["MAIL_PASSWORD"] = 'your-password'

mail.init_app(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="cardiology department"
)


@app.route("/")
def index():
    session.clear()
    print("wwefas")

    cursor = mydb.cursor()

    # cursor.execute(
    #     "CREATE TABLE Admin (Assn INT NOT NULL PRIMARY KEY, name  VARCHAR(40), PhoneNumber VARCHAR(40))")
    # cursor.execute("CREATE TABLE Patient  (Pssn INT NOT NULL PRIMARY KEY, name  VARCHAR(40), DateOfBirth DATE,Gender VARCHAR(40),Age INT ,doctorID INT,PhoneNumber VARCHAR(50),AppointID INT)")
    # cursor.execute("CREATE TABLE Doctor (Dssn INT NOT NULL PRIMARY KEY,name VARCHAR(40) , DateOfBirth DATE ,Gender VARCHAR(40),Age INT ,PhoneNumber VARCHAR(255),Role VARCHAR(50))")
    # cursor.execute("CREATE TABLE Appointment (ID INT NOT NULL PRIMARY KEY,DoctorID INT REFERENCES Doctor(Dssn),PatientID INT REFERENCES Patient(Pssn),AppointmentDate DATETIME Not NULL)")
    # cursor.execute(
    #     "CREATE TABLE Room (RoomNumber INT NOT NULL PRIMARY KEY,VacancyState VARCHAR(50),PatientID INT REFERENCES Patient(Pssn))")
    # cursor.execute(
    #     "CREATE TABLE Account (SSN INT NOT NULL PRIMARY KEY,Password VARCHAR(50),flag VARCHAR(10))")
    # cursor.execute(
    #     "CREATE TABLE Doctor_Attendance (Doctor_DSSN INT NOT NULL PRIMARY KEY REFERENCES Doctor(Dssn),Attendance DATETIME NOT NULL)")
    # cursor.execute(
    #     "CREATE TABLE Record(ID INT NOT NULL PRIMARY KEY,AppointID INT REFERENCES Appointment (ID),HealthProblem VARCHAR (50),DateOfRecord date)")
    # cursor.execute("CREATE TABLE Test(TestID INT NOT NULL PRIMARY KEY,PatientID INT REFERENCES Patient(Pssn),DateOfTest DATE,RecordID INT REFERENCES Record(ID),name VARCHAR(40),results VARCHAR(1000))")
    # cursor.execute(
    #     "ALTER TABLE Patient ADD FOREIGN KEY (AppointID)  REFERENCES Appointment (ID)")

    # cursor.execute(
    #     "ALTER TABLE Appointment ADD FOREIGN KEY (PatientID)  REFERENCES Patient (Pssn),ADD FOREIGN KEY (DoctorID)  REFERENCES Doctor (Dssn)")
    mydb.commit()
    cursor.close()
    return render_template('/mainPage.html')


@app.route('/Home')
def Home2():
    return render_template('/mainPage.html')


# @app.route('/Patients')
# def Patients2():
#     return render_template('/Patients.html')


# @app.route('/FindaDoctor')
# def find():
#     return render_template('/find_doctor.html')


@app.route('/MyAppointments')
def Appointments():
    return render_template('/My_Appointments.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    print("asda")

    session.pop('loggedin', None)
    session.pop('flag', None)
    session.pop('username', None)
    # Redirect to login page
    return render_template('/mainPage.html')


# @app.route('/Signin', methods=['GET', 'POST'])
# def Login0():
#     return render_template('/Signin.html')


@app.route('/Signin', methods=['GET', 'POST'])
def Login():

    msg = ''

    if request.method == 'POST' and 'SSN' in request.form and 'psw' in request.form:
        username = request.form['SSN']
        password = request.form['psw']
        cursor = mydb.cursor()

        cursor.execute(
            'SELECT * FROM account WHERE SSN = %s AND Password = %s', (username, password,))
        account = cursor.fetchone()

        if account:

            session['loggedin'] = True

            session['flag'] = account[2]

            session['username'] = account[0]
            # Redirect to home page
            msg = "you have succesfully logged in"
            return render_template('/mainPage.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('/Signin.html', msg=msg)


@app.route('/Register', methods=['GET', 'POST'])
def Register():
    cursor = mydb.cursor()

    if request.method == "POST":
        #details = request.form
        SSN = request.form['SSN']
        Psw = request.form['psw']
        flag = request.form['flag']
        if flag == "Y":
            cursor = mydb.cursor()
            cursor.execute('SELECT Dssn FROM doctor WHERE Dssn = %s' % (SSN))
            Dssn1 = cursor.fetchone()
            Dssn = Dssn1[0]

            print(Dssn)
            print(SSN)
            x = int(SSN)
            y = int(Dssn)

            if x == y:

                #cursor.execute("INSERT INTO account(SSN, Password,flag) VALUES (%s, %s, %s)" % (SSN, Psw, "Doctor"))
                sql = "INSERT INTO account (SSN,Password, flag) VALUES (%s, %s, %s)"
                val = (SSN, Psw, "Doctor")
                cursor.execute(sql, val)
                mydb.commit()

                return render_template('mainPage.html')
        else:
            #cursor = mydb.cursor()
            cursor.execute('SELECT Pssn FROM Patient WHERE Pssn = %s' % (SSN))
            Pssn1 = cursor.fetchone()
            Pssn = Pssn1[0]
            x = int(SSN)
            y = int(Pssn)
            if y == x:
                cursor = mydb.cursor()
               # cursor.execute("INSERT INTO Account(SSN, Password,flag) VALUES (%s, %s, %s)", (SSN, Psw, "Patient",))
                sql = "INSERT INTO account (SSN,Password, flag) VALUES (%s, %s, %s)"
                val = (SSN, Psw, "patient")
                cursor.execute(sql, val)
                mydb.commit()
                cursor.close()
                return render_template('mainPage.html')

    return render_template('Register.html')


@app.route('/addDoctor', methods=['GET', 'POST'])
def addDoctor():

    cursor = mydb.cursor()

    if request.method == "POST":

        try:
            if (session['flag'] == "admin"):

                Dssn = request.form['Dssn']

                name = request.form['fname']

                Age = request.form['Age']

                Gender = request.form['Gender']

                phone = request.form['Phone']

                sql = "INSERT INTO doctor (name,Dssn, DateOfBirth,Gender,Age,PhoneNumber,Role ) VALUES (%s, %s, %s,%s,%s,%s,%s)"
                val = (name, Dssn, None, Gender, Age, phone, "doctor")
                cursor.execute(sql, val)
                mydb.commit()

            else:
                flash("You Can't add a Doctor", 'category2')
        except:
            flash("You Can't add a Doctor", 'category2')

    # return render_template('/find_doctor.html')
    return redirect(url_for('FindaDoctor'))


@app.route('/addPatient', methods=['GET', 'POST'])
def addPatient():

    cursor = mydb.cursor()
    if request.method == "POST":

        try:
            if (session['flag'] == "admin"):

                Pssn = request.form['Pssn']
                print("1")

                name = request.form['fname']

                print("2")

                Age = request.form['Age']
                print("3")
                Gender = request.form['Gender']
                print("4")
                phone = request.form['Phone']
                print("5")
                sql = "INSERT INTO patient (Pssn,name, DateOfBirth,Gender,Age, doctorID, PhoneNumber, AppointID ) VALUES (%s, %s, %s,%s,%s,%s,%s, %s)"
                val = (Pssn, name, None, Gender, Age, None, phone, None)
                cursor.execute(sql, val)
                mydb.commit()

            else:
                flash("You Can't add a Patient", 'category4')
        except:
            flash("You Can't add a Patient", 'category4')

    return redirect(url_for('Patients'))


@app.route('/FindaDoctor', methods=['GET', 'POST'])
def FindaDoctor():
    cursor = mydb.cursor()

    cursor.execute(
        'SELECT Dssn, name,Age ,Gender,PhoneNumber FROM doctor')
    Results = cursor.fetchall()
    return render_template('find_doctor.html', Doctors=Results)


@app.route('/Patients', methods=['GET', 'POST'])
def Patients():

    cursor = mydb.cursor()

    cursor.execute(
        'SELECT Pssn, name,Age,Gender,PhoneNumber FROM patient')
    Results = cursor.fetchall()

    return render_template('Patients.html', Patients=Results)


@app.route('/delete_doctor/<string:id>', methods=['GET', 'POST'])
def delete_doctor(id):

    try:

        if session['flag'] == "admin":
            cursor = mydb.cursor()

            cursor.execute('DELETE FROM doctor WHERE Dssn = %s' % (id))

            mydb.commit()

        else:

            flash("You Can't delete a Doctor", 'category1')

    except:

        flash("You Can't delete a Doctor", 'category1')

    return redirect(url_for('FindaDoctor'))


@app.route('/delete_Patient/<string:id>', methods=['GET', 'POST'])
def deletePatient(id):

    try:

        if session['flag'] == "admin":
            cursor = mydb.cursor()

            cursor.execute('DELETE FROM patient WHERE Pssn = %s' % (id))

            mydb.commit()

        else:

            flash("You Can't delete a Patient", 'category3')

    except:

        flash("You Can't delete a Patient", 'category3')

    return redirect(url_for('Patients'))


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():

#     form = ContactForm()

#     if request.method == 'POST':
#         if form.validate() == False:
#             flash('All fields are required.')
#             return render_template('contact.html', form=form)
#         else:
#             msg = Message(form.subject.data, sender='contact@example.com',
#                           recipients=['tarksalah@gmail.com'])
#             msg.body = """
#       From: %s <%s>
#       %s
#       """ % (form.name.data, form.email.data, form.message.data)
#             mail.send(msg)

#             return 'Form posted.'

#     elif request.method == 'GET':
#         return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
