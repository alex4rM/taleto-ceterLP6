from crypt import methods
from flask import Flask,render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import datetime


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