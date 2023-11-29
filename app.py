from flask import Flask,render_template
from flask_mysqldb import MySQL

# Crear una app para comprobar
# el funcionamiento del archivo main

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

@app.route('/productos')
def productos():
    #lista de datos de la DB
    #creamos un cursor
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()

    print(data)
    
    return render_template('productos.html',data=data)


if __name__=='__main__':
    app.run(debug=True, port=5000)
    
