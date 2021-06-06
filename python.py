from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mysqldb import MySQL
from flask.wtf import TextField, TextAreaField, SubmitField, validators, ValidationError
from forms import ContactForm
from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField
from flask.ext.mail import Message, Mail

mail = Mail()
print("asdasd")

class ContactForm(Form):
    name = TextField("Name",  [validators.Required()])
    emsail = TextField("Email",  [validators.Required()])
    subject = TextField("Subject",  [validators.Required()])
    message = TextAreaField("Message",  [validators.Required()])
    submit = SubmitField("Send")


app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'tarksalah@gmail.com'
app.config["MAIL_PASSWORD"] = 'your-password'

mail.init_app(app)
app.config['MYSQL_USER'] = 'sql11416365'
app.config['MYSQL_PASSWORD'] = 'vFw2EsUfJB'
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql11416365'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    # cursor.execute("CREATE TABLE Admin (Assn VARCHAR(50) NOT NULL PRIMARY KEY, name  VARCHAR(40), PhoneNumber VARCHAR(40))")
    # cursor.execute("CREATE TABLE Patient  (Pssn VARCHAR(50) NOT NULL PRIMARY KEY, name  VARCHAR(40), DateOfBirth DATE,Gender VARCHAR(40),Age INT ,doctorID INT,PhoneNumber VARCHAR(50),AppointID INT)")
    # cursor.execute("CREATE TABLE Doctor (Dssn VARCHAR(50) NOT NULL PRIMARY KEY,name VARCHAR(40) , DateOfBirth DATE ,Gender VARCHAR(40),Age INT ,PhoneNumber VARCHAR(255),Role VARCHAR(50))")
    # cursor.execute("CREATE TABLE Appointment (ID INT NOT NULL PRIMARY KEY,DoctorID INT REFERENCES Doctor(Dssn),PatientID INT REFERENCES Patient(Pssn),AppointmentDate DATETIME Not NULL)")
    # cursor.execute("CREATE TABLE Room (RoomNumber INT NOT NULL PRIMARY KEY,VacancyState VARCHAR(50),PatientID INT REFERENCES Patient(Pssn))")
    # cursor.execute("CREATE TABLE Account (SSN INT NOT NULL PRIMARY KEY,Password VARCHAR(50),flag VARCHAR(10))")
    # cursor.execute("CREATE TABLE Doctor_Attendance (Doctor_DSSN INT NOT NULL PRIMARY KEY REFERENCES Doctor(Dssn),Attendance DATETIME NOT NULL)")
    # cursor.execute("CREATE TABLE Record(ID INT NOT NULL PRIMARY KEY,AppointID INT REFERENCES Appointment (ID),HealthProblem VARCHAR (50),DateOfRecord date)")
    # cursor.execute("CREATE TABLE Test(TestID INT NOT NULL PRIMARY KEY,PatientID INT REFERENCES Patient(Pssn),DateOfTest DATE,RecordID INT REFERENCES Record(ID),name VARCHAR(40),results VARCHAR(1000))")
    # cursor.execute("ALTER TABLE Patient ADD FOREIGN KEY (AppointID)  REFERENCES Appointment (ID)")
    # cursor.execute("ALTER TABLE Patient ADD FOREIGN KEY (AppointID)  REFERENCES Appointment (ID)")
    # cursor.execute("ALTER TABLE Appointment ADD FOREIGN KEY (PatientID)  REFERENCES Patient (Pssn),ADD FOREIGN KEY (DoctorID)  REFERENCES Doctor (Dssn)")
    mysql.connection.commit()
    cursor.close()
    return render_template('/mainPage.html')


@app.route('/Home')
def Home2():
    return render_template('/mainPage.html')

@app.route('/FindaDoctor')
def find():
    return render_template('/find_doctor.html')

@app.route('/MyAppointments')
def Appointments():
    return render_template('/My_Appointments.html')

@app.route('/logout',methods=['GET', 'POST'])
def logout():

   session.pop('loggedin', None)
   session.pop('flag', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/Signin',methods=['GET', 'POST'])
def Login():

    # msg = ''

    # if request.method == 'POST' and 'SSN' in request.form and 'psw' in request.form:
    #     username = request.form['SSN']
    #     password = request.form['psw']
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('SELECT * FROM accounts WHERE SSN = %s AND password = %s', (username, password))
    #     account = cursor.fetchone()
    #     if account:
    #         session['loggedin'] = True
    #         session['flag'] = account['flag']
    #         session['username'] = account['username']
    #         # Redirect to home page
    #         return 'Logged in successfully!'
    #     else:
    #         # Account doesnt exist or username/password incorrect
    #         msg = 'Incorrect username/password!'
     return render_template('/Signin.html', msg=msg)

@app.route('/Register',methods=['GET', 'POST'])
def Register():

    # if request.method == "POST":
    #     details = request.form
    #     SSN = details['SSN']
    #     Psw = details['psw']
    #     if(request.form.get('flag')=="yes"):
            # cursor = mysql.connection.cursor()
            # cursor.execute('SELECT Assn FROM Admin WHERE Assn = %s', (SSN))
            # Assn = cursor.fetchone()
            # if SSN = Assn :
                #cursor.execute("INSERT INTO Account(SSN, Password,flag) VALUES (%s, %s)", (SSN, Psw,"Doctor"))
                #mysql.connection.commit()
                #cur.close()
        #else :
            # cursor = mysql.connection.cursor()
            # cursor.execute('SELECT Pssn FROM Admin WHERE Pssn = %s', (SSN))
            # Pssn = cursor.fetchone()
            # if SSN = Pssn
                # cursor = mysql.connection.cursor()
                #cursor.execute("INSERT INTO Account(SSN, Password,flag) VALUES (%s, %s)", (SSN, Psw,"Patient"))
                #mysql.connection.commit()
                #cur.close()
            return render_template('/Register.html')

@app.route('/addDoctor',methods=['GET', 'POST'])
def addDoctor():

    if (session['flag']=="admin") :

        name = request.form['fname']
        Age = request.form['Age']
        Gander = request.form['Gander']
        phone = request.form['Phone']
        #add to doctor's table

    else :
        flash("You Can't add a Doctor")

    return render_template('/find_doctor.html')

@app.route('/Patients',methods=['GET', 'POST'])
def addPatient():
    if (session['flag']=="admin") :

        name = request.form['fname']
        Age = request.form['Age']
        Gander = request.form['Gander']
        phone = request.form['Phone']
        #add to Patient's table
    else :
        flash("You Can't add a Patient")

    return render_template('/Patients.html')

@app.route('/find_doctor',methods=['GET', 'POST'])
def Doctors():

    # Results = Select all Doctors from Doctors table
    return render_template('find_doctor.html',Patients=Results)

@app.route('/Patients',methods=['GET', 'POST'])
def Patients():

    # Results = Select all Patients from Patients table
    return render_template('find_doctor.html',Patients=Results)

@app.route('/delete_doctor/<string:id>',methods=['GET', 'POST'])
def deleteDoctor(id):

    if session['flag']=="admin" :
        x=1
        #Delete a doctor from database

    else :
        flash("You Can't delete a Doctor")


    return redirect(url_for('find_doctor'))

@app.route('/delete_Patient/<string:id>',methods=['GET', 'POST'])
def deletePatient(id):

    if session['flag']=="admin" :
        x=1
        #Delete a Patient from database

    else :
        flash("You Can't delete a Patient")

    return redirect(url_for('Patients'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():

  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['tarksalah@gmail.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return 'Form posted.'
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
