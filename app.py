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
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos')
        data = cur.fetchall()
        cur.close()
        return render_template('productos.html', data=data)
    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred while fetching data from the database."


@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Get form data
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']
        stock = request.form['stock']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO productos (nombre, marca, precio, stock) VALUES (%s, %s, %s, %s)", (nombre, marca, precio, stock))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('productos'))

    return render_template('nuevo_producto.html')

# @app.route('/borrar_producto/<int:codigo>', methods=['POST'])
# def borrar_producto(codigo):

#     cur = mysql.connection.cursor()
        
#     cur.execute("DELETE FROM productos WHERE codigo = %s", (codigo))

#     mysql.connection.commit()
#     cur.close()

#     return redirect(url_for('productos'))

@app.route('/borrar_producto', methods=['POST'])
def borrar_producto():
    id = request.form.get("id")
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE codigo = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('productos'))

if __name__=='__main__':
    app.run(debug=True, port=5000)
    
