from flask import Flask, flash, redirect, render_template, request, url_for
from flaskext.mysql import MySQL


#Modelos
from models.modelUser import ModelUser

#entities
from models.entities.User import User

app = Flask(__name__)

#MYSQL conection
mysql = MySQL()
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='talento-center'

mysql.init_app(app)
mysql.connect()

#settings
app.secret_key = 'mysecretkey'
 
@app.route('/')
def index():
 return render_template('index.html')


@app.route('/admin/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #print(request.form['usuario'])
        #print(request.form['password'])
        user=User(0,request.form['usuario'],
            request.form['password'],0)
        logged_user=ModelUser.login(mysql, user)
        if logged_user!=None:
            if logged_user.password:
                return redirect(url_for('admin_home'))
            else:
                flash('Contraseña incorrecta...!')
                return render_template('admin/login.html')
        else:
            flash('Usuario no encontrado...')
            return redirect(url_for('admin_home'))
    else:
        return render_template("admin/login.html")

@app.route('/admin/home')
def admin_home():
    return render_template("admin/home.html")

@app.route('/admin/citas')
def citas():
    return render_template("admin/listarCitas.html")

@app.route('/new_user',methods=['POST'])
def new_user():
    if request.method == 'POST':
        nombre = request.form['name']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        correo = request.form['correo']
        telefono = request.form['telefono']
        
        hora = request.form['hora']
        
        fecha = request.form['fecha']

        cur = mysql.get_db().cursor()
        cur.execute("insert into usuario (nombre, apellidos, correo, telefono, dni) VALUES(%s, %s, %s, %s, %s)",
        (nombre, apellidos, correo, telefono, dni))
        cur.execute("select id_user from usuario where dni ="+dni)
        res = cur.fetchall()
        for x in res:
            var = x
        mysql.get_db().commit()
        
        cur.execute("insert into reserva_cita(fecha, hora, id_user) VALUES(%s,%s, %s)",(fecha, hora, var))
        mysql.get_db().commit()
        cur.close()
        flash('Usuario agregado con exito')
    return redirect(url_for('index'))




if __name__=='__main__':
    app.run(
        port=4000,
        debug = True
)