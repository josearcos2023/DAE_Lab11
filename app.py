from flask import Flask,render_template
from flask import request,redirect,url_for
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

    # print(data)
    
    return render_template('productos.html',data=data)


@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Get form data
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']
        stock = request.form['stock']

        # Create a cursor
        cur = mysql.connection.cursor()

        # Insert new product into the database
        cur.execute("INSERT INTO productos (nombre, marca, precio, stock) VALUES (%s, %s, %s, %s)", (nombre, marca, precio, stock))

        # Commit the transaction and close the cursor
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('productos'))

    return render_template('nuevo_producto.html')

@app.route('/borrar_producto/<int:codigo>', methods=['GET', 'POST'])
def borrar_producto(codigo):
    if request.method == 'POST':
        # Create a cursor
        cur = mysql.connection.cursor()

        # Delete the product from the database
        cur.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))

        # Commit the transaction and close the cursor
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('productos'))

    return redirect(url_for('productos'))

if __name__=='__main__':
    app.run(debug=True, port=5000)
    
