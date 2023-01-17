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


'''def background_task():
    with app.app_context():
        while True:
            cursor=mydb.cursor()
            cursor.execute('select id,date from task')
            task=cursor.fetchall()
            #print(data)
            if len(task)==0:
                pass
            else:
                for i in task:
                    today=date.today()
                    current_date=datetime.strptime(f'{str(today.day)}-{str(today.month)}-{str(today.year)}','%d-%m-%Y')
                    due_date=i[1]
                    due_date1=datetime.strptime(f'{str(due_date.day)}-{str(due_date.month)}-{str(due_date.year)}','%d-%m-%Y')
                    
                    mydb.commit()
                    subject=f'remainding task '
                    body=f'you are not submited today is the last date {id1[3]}\n\n\n submit task!'
                    cursor.close()
                    try:
                        mail_sender(email_from,email,subject,body,passcode)
                    except Exception as e:
                        print(e)
                        return render_template('check2.html')'''
                        


        #print(cursor.fetchall())'''
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/adminlogin')
def login():
    if request.method=='POST':
        data=request.form['id']
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
            cursor.execute('insert into admin values(%s,%s,%s,%s)',[user,password,email,passcode])
            mysql.connection.commit()
            return redirect(url_for('home'))
    return render_template('create.html')


@app.route('/validation',methods=['POST'])
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
@app.route('/adminlogout')
def logoutadmin():
     
     return redirect(url_for('home'))
@app.route('/adminpanel')
def adminpanel():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT stud_id from student')
    students=cursor.fetchall()
    cursor.close()
    return render_template('adminpanel.html',students=students)
@app.route('/create1',methods=['GET','POST'])
def create1():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT count(*) from student')
    re=int(cursor.fetchone()[0])
    cursor.close()
    if request.method=='POST':
        cursor=mysql.connection.cursor()
        stud_id=request.form['stud_id']
        cursor.execute('SELECT stud_id from student')
        students=cursor.fetchall()
        cursor.execute('SELECT email from student')
        emails=cursor.fetchall()
        if (stud_id,) in students:
            flash('Employee id already exists')
            return render_template('signin.html')
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        if (email,) in emails:
            flash('Email is  already exists')
            return render_template('signin.html')
        password=request.form['password']
        phone=request.form['phonenumber']
        cursor.close()
        cursor=mysql.connection.cursor()
        cursor.execute('insert into student values(%s,%s,%s,%s,%s,%s)',[empid,firstname,lastname,email,password,phone])
        mysql.commit()
        return redirect(url_for('home'))
    return render_template('signin.html')
'''@app.route('/validation1',methods=['POST'])
def validation1():
    if session.get('email'):
        return redirect(url_for('create1',user=session['email']))
    if request.method=="POST":
        email=request.form['email']
        cursor=mydb.cursor()
        cursor.execute('SELECT email from empolyee')
        users=cursor.fetchall()            
        password=request.form['password']
        cursor.execute('select password from empolyee where email=%s',[email])
        task=cursor.fetchall()
        cursor.close() 
        if (email,) in users:
            if password==task[0]:
                session['email']=email
                print(session['email'])
                return redirect(url_for('home'))
            else:
                flash('Invalid Password')
                return render_template('employeelogin.html')
        else:
            flash('Invalid user id')
            return render_template('employeelogin.html')'''
@app.route('/taskemployee')
def taskemployee():
    if request.method=='POST':
         data=request.form['email']
         cursor=mysql.connection.cursor(buffered=True)
         cursor.execute('SELECT stud_id from student where email=%s',[request.form['email']])
         data=cursor.fetchone()
         id1=data[0]
         cursor.execute('SELECT * from assignment where assign_to=%s',[id1])
         tasks=cursor.fetchall()
         print(tasks)
         cursor.close()
         return render_template('taskemployee.html',id1=id1,students=student)
    return redirect(url_for('employeelogin'))
@app.route('/employeelogin',methods=['GET','POST'])
def employeelogin():
    if request.method=='POST':
        data=request.form['email']
        return redirect(url_for('taskemployee'))
    if request.method=="POST":
        email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT email from empolyee')
        emails=cursor.fetchall()
        password=request.form['password']
        cursor.execute('select password from empolyee where email=%s',[email])
        task=cursor.fetchone()
        cursor.close()
        if (email,) in emails:
            if password==task[0]:
                data=request.form["email"]=email
                return redirect(url_for('taskemployee'))
            else:
                flash('Invalid Password')
                return render_template('employeelogin.html')
        else:
            flash('Invalid faculty id')
            return render_template('employeelogin.html') 
    return render_template('employeelogin.html')
    
@app.route('/delete',methods=['POST'])
def delete():
    if request.method=='POST':
        print(request.form)
        s=request.form['option'].split()
        cursor=mysql.connection.cursor()
        cursor.execute('delete from student where id=%s',[s[0]])
        mysql.commit()
        cursor.close()
        return redirect(url_for('adminpanel'))
@app.route('/addtask',methods=['GET','POST'])
def addassignment():
    if request.method=='POST':
        id1=request.form['assign_id']
        name=request.form['assign_name']        
        assign_to=request.form['assign_to']
        duedate=request.form['date']
        cursor=mysql.connection.cursor()
        id2=request.get('id')
        print(id2)
        
        cursor.execute('insert into assignment(id,name,assigning,status,assign_to,date) values(%s,%s,%s,%s,%s,%s)',[id1,name,id2,'NOT AVAILABLE',assign_to,duedate])
        mysql.commit()
        cursor.close()
        return redirect(url_for('adminpanel'))
    return render_template('addtask.html')
@app.route('/viewtask')
def view():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from student')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('alltasktable.html',students=assignment)
@app.route('/viewtask1')
def view1():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * from students order by date')
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('table1.html',students=students)
        
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
            cursor=mydb.cursor()
            cursor.execute('update empolyee set password=%s,email=%s',[password,email])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('password1'))
    return render_template('empforgetpass.html')



@app.route('/update',methods=['POST'])
def update1():
    option1=request.form['id'].split()[0]
    return redirect(url_for('update',id=option1))
@app.route('/update/<id1>',methods=['GET','POST'])
def update(id):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM student where id=%s',[id])
    option=cursor.fetchall()
    id=option[0][0]
    sname=option[0][1]
    print(option)
    assign_to=option[0][5]
    print(assign_to)
    date=option[0][3]
    cursor.close()
    if request.method=='POST':
        name2=request.form['name']
        
        assign_to2=request.fo+rm['assign_to']
        
        date2=request.form['date']
        
        cursor=mysql.connection.cursor()
        
        cursor.execute('SELECT assignment,assign_to from student where id=%s',[id])
    
        task=cursor.fetchone()
        cursor.execute('update assignment set name=%s,date=%s,assign_to=%s where stud_id=%s',[name2,date2,assign_to2,id1])
        mysql.connection.commit()
        cursor.close()
        subject=f'assignment updated'
        body=f'You completed the assignment with in time'
        cursor.close()
        try:
            mail_sender(email_from,email,subject,body)
        except Exception as e:
            print(e)
            return render_template('check2.html')
        return redirect(url_for('adminpanel'))
    
    return render_template('update.html',name=name,assign_to=assign_to,date=date,stud_id=stud_id)

app.run(debug=True)

