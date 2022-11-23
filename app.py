from flask import Flask, flash, redirect, render_template, request, url_for, make_response
from flaskext.mysql import MySQL
from flask_weasyprint import HTML, render_pdf

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
    cur = mysql.get_db().cursor()
    cur.execute("SELECT usuario.id_user,usuario.nombre,usuario.apellidos,usuario.dni,usuario.telefono,usuario.correo,reserva_cita.fecha,reserva_cita.hora,reserva_cita.estado_cita FROM reserva_cita,usuario WHERE reserva_cita.id_user=usuario.id_user")
    citas=cur.fetchall()
    mysql.get_db().commit()
    return render_template("admin/listarCitas.html", citas=citas)

@app.route('/admin/estado-cita',methods=['post'])
def admin_estadocita():
    _id=request.form['id_cita']
    #print(id)
    cur = mysql.get_db().cursor()
    cur.execute("UPDATE reserva_cita SET estado_cita='1' WHERE id_reserva=%s ",(_id))
    citas=cur.fetchall()
    mysql.get_db().commit()
    return redirect("/admin/citas")

@app.route('/admin/cancelar-cita',methods=['post'])
def admin_cancelarcita():
    _id=request.form['id_cita']
    #print(id)
    cur = mysql.get_db().cursor()
    cur.execute("UPDATE reserva_cita SET estado_cita='2' WHERE id_reserva=%s ",(_id))
    citas=cur.fetchall()
    mysql.get_db().commit()
    return redirect("/admin/citas")

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
        estado_cita=0
        cur.execute("insert into reserva_cita(fecha, hora, estado_cita, id_user) VALUES(%s,%s, %s,%s)",(fecha, hora, estado_cita,var))
        mysql.get_db().commit()
        cur.close()
        cur = mysql.get_db().cursor()
        resultValue = cur.execute("SELECT usuario.id_user,usuario.nombre,usuario.apellidos,usuario.dni,usuario.telefono,usuario.correo,reserva_cita.fecha,reserva_cita.hora,reserva_cita.estado_cita FROM reserva_cita,usuario WHERE usuario.dni="+dni+" and usuario.id_user=reserva_cita.id_user")
        mysql.get_db().commit()
        if resultValue > 0:
            citas = cur.fetchall()
        html = render_template('reservausuario.html', citas=citas)
        
    
    return write_pdf(HTML(string=html))
        #flash('Usuario agregado con exito')
    return redirect(url_for('index'))

@app.route('/reporte')
def reporte():
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT usuario.id_user,usuario.nombre,usuario.apellidos,usuario.dni,usuario.telefono,usuario.correo,reserva_cita.fecha,reserva_cita.hora,reserva_cita.estado_cita FROM reserva_cita,usuario WHERE reserva_cita.id_user=usuario.id_user")
    if resultValue > 0:
        citas = cur.fetchall()
    html = render_template('admin/pdf.html', citas=citas)
    
    return render_pdf(HTML(string=html))
    

if __name__=='__main__':
    app.run(
        port=4000,
        debug = True
)