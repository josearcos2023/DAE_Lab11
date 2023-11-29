from flask import Flask,render_template
from flask import request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'david2023'
app.config['MYSQL_DB'] = 'bda'

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def index():
       
    #lista de cursos
    cursos=['PHP','Python','JavaScript','TypeScript','C#','Kotlin']
    data={
        'titulo':'index',
        'bienvenido':'Clase de Flask',
        'cursos':cursos
    }
    # return "<h1>Alumnos de Flask</h1>"
    return render_template('index.html',data=data)

@app.route('/empleados')
def empleados():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empleado')
        data = cur.fetchall()
        cur.close()
        return render_template('empleados.html', data=data)
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Ha ocurrido un error al tomar la información de la base de datos"


@app.route('/nuevo_empleado', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        carrera = request.form['carrera']
        pais = request.form['pais']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empleado (nombre, apellido, telefono, carrera, pais) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, telefono, carrera, pais))
        mysql.connection.commit()
        cur.close()

        return redirect('empleados')
        # return redirect(url_for('empleados'))

    return render_template('nuevo_empleado.html')

@app.route('/borrar_empleado', methods=['POST'])
def borrar_producto():
    id = request.form.get("id")
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM empleado WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect('/empleados')

@app.route('/editar_empleado', methods=['GET','POST'])
def editar_producto():
    if request.method == 'POST':
        id = request.form.get("id")
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM empleado WHERE id = %s', (id,))
        data = cur.fetchall()
        print(data)
        cur.close()
    return render_template('editar_empleado.html', data=data)

@app.route('/editar', methods=['POST'])
def editar():
    
    id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    carrera = request.form['carrera']
    pais = request.form['pais']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE empleado SET nombre=%s, apellido=%s, telefono=%s, carrera=%s, pais=%s WHERE id=%s", (nombre, apellido, telefono, carrera, pais, id))
    mysql.connection.commit()
    cur.close()
    
    return redirect("/empleados")


if __name__=='__main__':
    app.run(debug=True, port=5000)
    
