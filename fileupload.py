from flask import Flask,render_template,redirect,url_for,request,send_file
from io import BytesIO
from flask_mysqldb import MySQL
app=Flask(__name__)
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='123'
app.config['MYSQL_DB']='students'
mysql=MySQL(app)
@app.route('/',methods=['GET','POST'])
def welcome():
    if request.method=='POST':
        file=request.files['file']
        print(file.filename)
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO UPLOAD (file,filename) values(%s,%s)',[file.read(),file.filename])
        mysql.connection.commit()
        cursor.close()
    return render_template('fileupload.html')
@app.route('/download/<filename>')
def download(filename):
    cursor=mysql.connection.cursor()
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT file from upload where filename=%s',[filename])
    data=cursor.fetchone()[0]
    return send_file(BytesIO(data),download_name=filename,as_attachment=True)
@app.route('/view/<filename>')
def view(filename):
    cursor=mysql.connection.cursor()
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT file from upload where filename=%s',[filename])
    data=cursor.fetchone()[0]
    #mention as_attachment=True to download the file--remove it to display the file
    return send_file(BytesIO(data),download_name=filename)
app.run()
