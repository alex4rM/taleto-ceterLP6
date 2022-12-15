from flask import Flask, flash, redirect, render_template, request, url_for, make_response, flash
from flaskext.mysql import MySQL
from flask_weasyprint import HTML, render_pdf
from flask_login import LoginManager, login_user, logout_user,login_required
from flask_wtf.csrf import CSRFProtect

#Modelos
from models.modelUser import ModelUser

#entities
from models.entities.User import User

app = Flask(__name__)

csrf=CSRFProtect()

#MYSQL conection
mysql = MySQL()
app.config['MYSQL_HOST']='4lex22.mysql.pythonanywhere-services.com'
app.config['MYSQL_DATABASE_USER']='4lex22'
app.config['MYSQL_DATABASE_PASSWORD']='123Oswaldo'
app.config['MYSQL_DATABASE_DB']='4lex22$talento-center'

mysql.init_app(app)
mysql.connect()

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql,id)


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
            request.form['password'],0,0)
        logged_user=ModelUser.login(mysql, user)
        if logged_user!=None:
            if logged_user.contra_user:
                login_user(logged_user)
                return redirect(url_for('admin_home'))
            else:
                flash('Contraseña incorrecta...!')
                return render_template('admin/login.html')
        else:
            flash('Usuario no encontrado...')
            return redirect(url_for('login'))
    else:
        return render_template("admin/login.html")

@app.route('/admin/home')
@login_required
def admin_home():
    return render_template("admin/home.html")

@app.route('/admin/citas')
@login_required
def citas():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT persona.id_user,persona.nombre,persona.apellidos,persona.dni,persona.telefono,persona.correo,reserva_cita.fecha,reserva_cita.hora,reserva_cita.estado_cita FROM reserva_cita,persona WHERE reserva_cita.id_user=persona.id_user")
    citas=cur.fetchall()
    mysql.get_db().commit()
    return render_template("admin/listarCitas.html", citas=citas)

@app.route('/admin/estado-cita',methods=['post'])
@login_required
def admin_estadocita():
    _id=request.form['id_cita']
    #print(id)
    cur = mysql.get_db().cursor()
    cur.execute("UPDATE reserva_cita SET estado_cita='1' WHERE id_reserva=%s ",(_id))
    citas=cur.fetchall()
    mysql.get_db().commit()
    return redirect("/admin/citas")

@app.route('/admin/cancelar-cita',methods=['post'])
@login_required
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
        cur.execute("insert into persona (nombre, apellidos, correo, telefono, dni) VALUES(%s, %s, %s, %s, %s)",
        (nombre, apellidos, correo, telefono, dni))
        cur.execute("select id_user from persona where dni ="+dni)
        res = cur.fetchall()
        for x in res:
            var = x
        mysql.get_db().commit()
        estado_cita=0
        cur.execute("insert into reserva_cita(fecha, hora, estado_cita, id_user) VALUES(%s,%s, %s,%s)",(fecha, hora, estado_cita,var))
        mysql.get_db().commit()
        cur.close()
        cur = mysql.get_db().cursor()
        resultValue = cur.execute("SELECT persona.id_user,persona.nombre,persona.apellidos,persona.dni,persona.telefono,persona.correo,reserva_cita.fecha,reserva_cita.hora,reserva_cita.estado_cita FROM reserva_cita,persona WHERE persona.dni="+dni+" and persona.id_user=reserva_cita.id_user")
        mysql.get_db().commit()
        if resultValue > 0:
            citas = cur.fetchall()
        html = render_template('reservausuario.html', citas=citas)
        
    
    return render_pdf(HTML(string=html))
        #flash('Usuario agregado con exito')
        #return redirect(url_for('index'))

@app.route('/reporte')
@login_required
def reporte():
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT persona.id_user,persona.nombre,persona.apellidos,persona.dni,persona.telefono,persona.correo,reserva_cita.fecha,reserva_cita.hora,reserva_cita.estado_cita FROM reserva_cita,persona WHERE reserva_cita.id_user=persona.id_user")
    if resultValue > 0:
        citas = cur.fetchall()
    html = render_template('admin/pdf.html', citas=citas)
    
    return render_pdf(HTML(string=html))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__=='__main__':
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404, status_404)
    app.run(
        port=4000,
        debug = True
)