
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import os 
from werkzeug.utils import secure_filename 

from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,validators,FileField,SubmitField
from passlib.hash import sha256_crypt
from functools import wraps
from os import environ




class RegisterForm(Form):
    name = StringField("İsim_Soyisim_Sınıf",validators=[validators.Length(min = 4,max = 25)])
    no = StringField("Veli Telefon Numarası(Lütfen başında 0 olmadan 10 haneli olacak şeilde giriniz)",validators=[validators.Length(min = 10,max = 10)])
    pic = FileField("Fotoğrafınız")
 
        
app = Flask(__name__)
app.secret_key= "FlaskDb"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "FlaskDb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

app.config['UPLOAD_FOLDER'] ="C:\\Users\BILICI\OneDrive\Masaüstü\Foto_kayit"
UPLOAD_FOLDER = "C:\\Users\BILICI\OneDrive\Masaüstü\Foto_kayit"

mysql = MySQL(app)



#Açılış Sayfası
@app.route("/")
def index():
   return render_template("index.html")

#Kayıt  
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
   

    if request.method == "POST" and form.validate():

        pic = request.files['pic']
        if not request.files.get('pic', None):
            pass

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


        imagepath = UPLOAD_FOLDER +'/'+ filename
        name = form.name.data
        no = form.no.data
        

        cursor = mysql.connection.cursor()

        sorgu = "Insert into students(name,no,imagepath) VALUES(%s,%s,%s)"

        cursor.execute(sorgu,(name,no,imagepath))
        mysql.connection.commit()
        cursor.close()

        flash("Başarıyla Kayıt Oldunuz...","success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html",form = form)





#Hakkımızda
@app.route("/about")
def about():
    return render_template("about.html")
    

# Arama URL
@app.route("/search",methods = ["GET","POST"])
def search():
   if request.method == "GET":
       return redirect(url_for("index"))
   else:
       keyword = request.form.get("keyword")

       cursor = mysql.connection.cursor()

       sorgu = "Select * from articles where title like '%" + keyword +"%'"

       result = cursor.execute(sorgu)

       if result == 0:
           flash("Aranan kelimeye uygun makale bulunamadı...","warning")
           return redirect(url_for("articles"))
       else:
           articles = cursor.fetchall()

           return render_template("articles.html",articles = articles)


if __name__ == "__main__":
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
