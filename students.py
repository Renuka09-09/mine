from flask import Flask,redirect,render_template,url_for,request,jsonify,session,flash,send_file
from flask_mysqldb import MySQL
from flask_session import Session
from datetime import date
from datetime import datetime
from io import BytesIO
from threading import Thread
from py_mail import mail_sender
import smtplib
from email.message import EmailMessage
app=Flask(__name__)
app.secret_key='projects'
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='123'
app.config['MYSQL_DB']='students'
mysql=MySQL(app)
Session(app)

@app.route('/')
def start():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/adminlogin')
def login():
    if session.get('id'):
        return redirect(url_for('adminpanel'))
    return render_template('adminlogin.html')

@app.route('/create',methods=['GET','POST'])
def create():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT count(*) from admin')
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
            return render_template('adminlogin.html')
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('insert into admin values(%s,%s,%s,%s)',[password,email,passcode,user])
            mysql.connection.commit()
            return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/validation',methods=['POST'])
def validation():
    if session.get('id'):
        return redirect(url_for('create',user=session['id']))
    if request.method=="POST":
        print(request.form)
        user=request.form['user']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT username from admin')
        users=cursor.fetchall()            
        password=request.form['password']
        cursor.execute('select password from admin where username=%s',[user])
        assignments=cursor.fetchone()
        cursor.close()
        print(user)
        print(assignments[0])
        print(assignments)
        if (user,) in users:
            if int(password)==assignments[0]:
                session['id']=user
                return redirect(url_for('adminpanel'))
            else:
                flash('Invalid Password')
                return redirect(url_for('login'))
        else:
            flash('Invalid user id')
            return redirect(url_for('login'))
        return redirect(url_for('login'))
        
    
    

@app.route('/adminlogout')
def logoutadmin():
    session.pop('id',None)
    return redirect(url_for('start'))
@app.route('/adminpanel')
def adminpanel():
     
     cursor=mysql.connection.cursor()
     cursor.execute('SELECT id from assignments')
     tasks=cursor.fetchall()
     cursor.close()
     return render_template('adminpanel.html',tasks=tasks)


@app.route('/create1',methods=['GET','POST'])
def create1():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT count(*) from students')
    re=int(cursor.fetchone()[0])
    cursor.close()
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        studid=request.form['studid']
        cursor.execute('SELECT studid from students')
        assignments=cursor.fetchall()
        cursor.execute('SELECT email from students')
        emails=cursor.fetchall()
        cursor.execute('SELECT section from students')
        
        assignments=cursor.fetchall()
        if (studid,) in assignments:
            flash('student id already exists')
            return render_template('signin.html')
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        section=request.form['section']
        if (email,) in emails:
            flash('Email is  already exists')
            return render_template('signin.html')
        password=request.form['password']
        phone=request.form['phonenumber']
        cursor.close()
        cursor=mysql.connection.cursor()
        cursor.execute('insert into students values(%s,%s,%s,%s,%s,%s,%s)',[studid,firstname,lastname,email,password,phone,section])
        mysql.connection.commit()
        return redirect(url_for('home'))
    return render_template('signin.html')

@app.route('/studentemp' ,methods=['GET','POST'])
def studentemp():
    
     if session.get('email'):
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT studid  from students where email=%s',[session['email']])
        data=cursor.fetchone()
        id1=data[0]
        cursor.execute('SELECT * from assignments where assign_to=%s',[id1])
        assignments=cursor.fetchall()
        print(assignments)
        cursor.close()
        return render_template('studentemp.html',id1=id1,data=assignments)
     return redirect(url_for('studentlogin'))

@app.route('/studentlogin',methods=['GET','POST'])
def studentlogin():
    if request.method=="POST":
        email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT email from students')
        emails=cursor.fetchall()
        password=request.form['password']
        
        cursor.execute('select password from students where email=%s',[email])
        assignments=cursor.fetchone()
        cursor.close()
        if (email,) in emails:
            if password==assignments[0]:
                session["email"]=request.form['email']
                
                return redirect(url_for('studentemp'))
            else:
                 flash('Invalid Password')
                 return render_template('studentlogin.html')
        else:
            flash('Invalid faculty id')
            return render_template('studentlogin.html') 
    return render_template('studentlogin.html')
@app.route('/logoutstud')
def logout():
    session.pop('email',None)
    return redirect(url_for('start'))
    
@app.route('/delete',methods=['POST'])
def delete():
    if request.method=='POST':
        print(request.form)
        s=request.form['option'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from assignments where id=%s',[s[0]])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminpanel'))


@app.route('/addmarks',methods=['POST','GET'])
def addmarks():
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM marks") 
    if request.method=="POST":
        studid=request.form.get('studid')
        marks=request.form.get('marks')
        print(marks,studid)
        
        cursor.execute('insert into marks(studid,marks) values(%s,%s)',[studid,marks])
        mysql.connection.commit()
        marks=cursor.fetchall()
        
        mysql.connection.commit()
        flash("marks added","warning")

        
    return render_template('marks.html')
@app.route('/viewmarks')
def view2():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from marks')
    marks=cursor.fetchall()
    cursor.close()
    return render_template('allmarks.html',marks=marks)

@app.route('/addstudents',methods=['GET','POST'])
def addstudents():
    if request.method=='POST':
        id1=request.form['studid']
        name=request.form['firstname']        
        name1=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        phonenumber=request.form['phonenumber']
        section=request.form['section']
        cursor=mysql.connection.cursor()
        id2=session.get('id')
        print(id2)
        
        cursor.execute('insert into students(studid,firstname,lastname,email,password,phonenumber,section) values(%s,%s,%s,%s,%s,%s,%s)',[id1,name,name1,email,password,phonenumber,section])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminpanel'))
    return render_template('student.html')
    
   
@app.route('/viewstudents',methods=['GET','POST'])
def view3():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from students')
    students=cursor.fetchall()
    cursor.close()
    return render_template('allstudents.html',students=students)


@app.route('/addattendence',methods=['GET','POST'])
def addattendence():
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM attendence") 
    if request.method=="POST":
        studid=request.form.get('studid')
        attendence=request.form.get('attendence')
        print(attendence,studid)
        
        cursor.execute('insert into attendence(attendence,studid) values(%s,%s)',[attendence,studid])
        mysql.connection.commit()
        tasks=cursor.fetchall()
        
        mysql.connection.commit()
        flash("attendence added","warning")

        
    return render_template('addattendence.html')
@app.route('/viewattendence')
def view1():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from attendence')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('allattendence.html',tasks=tasks)
    
@app.route('/addassignment',methods=['GET','POST'])
def addtask():
    
    if request.method=='POST':
        id1=request.form['id']
        assign_to=request.form['assign_to']    
        
        duedate=request.form['date']
        
        cursor=mysql.connection.cursor()
        id2=session.get('id')
        print(id2)
        
        cursor.execute('insert into assignments(id,assigning,date,assign_to) values(%s,%s,%s,%s)',[id1,id2,duedate,assign_to])
        cursor=mysql.connection.cursor()
        
        cursor.execute('SELECT PASSCODE from admin')
        passcode=cursor.fetchone()[0]
        cursor.execute('SELECT email from admin')
       
        
        
        
        
        cursor.execute('SELECT email from students where studid=%s',[assign_to])
        email_to=cursor.fetchone()[0]
        mysql.connection.commit()
        subject=f'assidnment is updated'
        body=f'\nYou completed the assignment with in time'
        cursor.close()
        return redirect(url_for('adminpanel'))
    return render_template('addassignment.html')

@app.route('/viewassignment')
def view():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from assignments order by date')
    data=cursor.fetchall()
    cursor.close()
    return render_template('allassignment.html',data=data)
@app.route('/viewtask1')
def view4():
    cursor=mydbcursor()
    cursor.execute('SELECT * from assignments order by date')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('table1.html',tasks=tasks)

@app.route('/fileupload',methods=['GET','POST'])
def fileupload():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT id FROM assignments')
    data=cursor.fetchall()
    cursor.execute('select studid from students where email=%s',[session.get('email')])
    id2=cursor.fetchone()[0]
    print(data)
    if request.method=='POST':
          assignid=request.form['option']
          File=request.files['file']
          filename=File.filename
          section=request.form['section']
          cursor=mysql.connection.cursor()
          cursor.execute('insert into upload values(%s,%s,%s,%s,%s)',[File.read(),id2,assignid,section,filename])
          mysql.connection.commit()
          cursor.close()
          return redirect(url_for('studentemp'))
    return render_template('fileupload.html',assignments=data)
@app.route('/viewfile/<id2>')
def view6(id2):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT file from upload where assignid=%s',[id2])
    data=cursor.fetchone()[2]
    print(data)
    cursor.execute('select filename from upload where assignid=%s',[id2])
    filename=cursor.fetchone()[2]
    print(filename)
   #mention as_attachment=True to download the file--remove it to display the file
    return send_file(BytesIO(data),download_name=filename)
    return render_template('allfiles.html',data=filename)

    
@app.route('/forgetpassword',methods=['GET','POST'])
def password():
    if request.method=='POST':
        print(request.form)
        key=request.form['key']
        password=request.form['password']
        email=request.form['email']
        passcode=request.form['p_key']
        if key==secret_key:
            cursor=mysql.connection.cursor()
            cursor.execute('update admin set password=%s,email=%s,passcode=%s',[password,email,passcode])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('password'))
    return render_template('secret.html')
@app.route('/password1',methods=['GET','POST'])
def password1():
    if request.method=='POST':
        print(request.form)
        email=request.form['email']
        password=request.form['password']
        if key==secret_key:
            cursor=mysql.connection.cursor()
            cursor.execute('update students set password=%s,email=%s',[password,email])
            mysql.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('password1'))
    return render_template('studforgetpass.html')



@app.route('/update',methods=['POST'])
def update1():
    option1=request.form['id1'].split()[0]
    return redirect(url_for('update',id1=option1))
@app.route('/update/<id1>',methods=['GET','POST'])
def update(id1):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM assignments where id=%s',[id1])
    option=cursor.fetchall()
    id1=option[0][0]
   
    print(option)
    assign_to=option[0][3]
    print(assign_to)
    date=option[0][2]
    cursor.close()
    if request.method=='POST':
        
        
        assign_to2=request.form['assign_to']
        
        date2=request.form['date']
        
        cursor=mysql.connection.cursor()
        
        cursor.execute('SELECT assigning,assign_to from assignments where id=%s',[id1])
    
        assignments=cursor.fetchone()
        cursor.execute('update assignments set date=%s,assign_to=%s where id=%s',[id1,date2,assign_to2])
        mysql.connection.commit()
        cursor.close()
        subject=f'assignment updated'
        body=f'You completed the task with in time'
        cursor.close()
        
        return redirect(url_for('adminpanel'))
    
    return render_template('update.html',assign_to=assign_to,date=date,id1=id1)

app.run(debug=True)



