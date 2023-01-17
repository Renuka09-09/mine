from flask import Flask,redirect,render_template,url_for,request,jsonify
from flask_mysqldb import MySQL
from datetime import date
from datetime import datetime
from threading import Thread
from secretconfig import secret_key
from py_mail import mail_sender
import smtplib
from email.message import EmailMessage
app=Flask(__name__)
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='123'
app.config['MYSQL_DB']='students'
mysql=MySQL(app)

# here we will create db models that is tables

    

@app.route('/')
def home(): 
    return render_template('home.html')
@app.route('/studentdetails')
def studentdetails():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT count(*)FROM `admin`")
    result=int(cursor.fetchone()[0])
    cursor.close()
    if request.method=='POST':
        secret_key=request.form['key']
        user=request.form['user']
        password=request.form['password']
        email=request.form['email']
        passcode=request.form['p_key']
        secret_key=cursor.fetchall()
        cursor.close()
        if (secret_key,) in secret_key:
            flash('This Security code is alredy taken by Faculty')
            return render_template('login.html')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('insert into admin values(%s,%s,%s,%s)',[user,password,email,passcode])
            mysql.connection.commit()
            return redirect(url_for('home'))

    
    return render_template('studentdetails.html',query=query)
@app.route('/assignment',methods=['POST','GET'])
def validation():
     if request.method=='POST':
        data=request.form['id']
        return redirect(url_for('create'))
     if request.method=="POST":
        print(request.form)
        user=request.form['user']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT username from admin')
        users=cursor.fetchall()            
        password=request.form['password']
        cursor.execute('select password from admin where username=%s',[user])
        task=cursor.fetchone()
        cursor.close()
        print(user)
        print(task[0])
        print(task)
        if (user,) in users:
            if password==task[0]:
                 data=request.form['id']=user
                 print(request.form['id'])
                 return redirect(url_for('adminpanel'))
            else:
                flash('Invalid Password')
                return redirect(url_for('login'))
        else:
            flash('Invalid user id')
            return redirect(url_for('login'))
'''def assignment():
    if request.method=='POST':
        file=request.files['files']
        upload=uploaded(name=files.filename ,data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f'uploded:{file.filename}'
    
    return render_template('assignment.html',query=query)'''
           

@app.route('/triggers')
def triggers():
   cursor.execute(f"SELECT * FROM `trig`") 
   return render_template('triggers.html',query=query)

@app.route('/department',methods=['POST','GET'])
def department():
    if request.method=="POST":
        dept=request.form.get('dept')
        query=Department.query.filter_by(branch=dept).first()
        if query:
            flash("Department Already Exist","warning")
            return redirect('/department')
        dep=Department(branch=dept)
        mysql.connection.add(dep)
        mysql.connection.commit()
        flash("Department Addes","success")
    return render_template('department.html')

@app.route('/addattendance',methods=['POST','GET'])
def addattendance():
    query=cursor.execute(f"SELECT * FROM `student`") 
    if request.method=="POST":
        rollno=request.form.get('rollno')
        attend=request.form.get('attend')
        print(attend,rollno)
        atte=Attendence(rollno=rollno,attendance=attend)
        mysql.connection.add(atte)
        mysql.commit()
        flash("Attendance added","warning")

        
    return render_template('attendance.html',query=query)
@app.route('/addattendance',methods=['POST','GET'])
def addmarks():
    query=cursor.execute(f"SELECT * FROM `student`") 
    if request.method=="POST":
        rollno=request.form.get('rollno')
        marks=request.form.get('marks')
        print(marks,rollno)
        atte=Marks(rollno=rollno,marks=marks)
        mysql.connection.add(marks)
        mysq.commit()
        flash("marks added","warning")

        
    return render_template('attendance.html',query=query)


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        rollno=request.form.get('roll')
        bio=Student.query.filter_by(rollno=rollno).first()
        attend=Attendence.query.filter_by(rollno=rollno).first()
        return render_template('search.html',bio=bio,attend=attend)
    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])

def delete(id):
    cursor.execute(f"DELETE FROM `student` WHERE `student`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/studentdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])

def edit(id):
    dept=cursor.execute("SELECT * FROM `department`")
    posts=Student.query.filter_by(id=id).first()
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        query=cursorexecute("UPDATE `student` SET `rollno`='{rollno}',`sname`='{sname}',`sem`='{sem}',`gender`='{gender}',`branch`='{branch}',`email`='{email}',`number`='{num}',`address`='{address}'")
        flash("Slot is Updates","success")
        return redirect('/studentdetails')
    
    return render_template('edit.html',posts=posts,dept=dept)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=cursor.execute("INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')

def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addstudent',methods=['POST','GET'])

def addstudent():
    dept=cursor.execute("SELECT * FROM `department`")
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        query=cursor.execute("INSERT INTO `student` (`rollno`,`sname`,`sem`,`gender`,`branch`,`email`,`number`,`address`) VALUES ('{rollno}','{sname}','{sem}','{gender}','{branch}','{email}','{num}','{address}')")
    

        flash("Booking Confirmed","info")


    return render_template('student.html',dept=dept)
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    
