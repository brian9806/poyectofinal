from flask import Flask,render_template, request, redirect, url_for,jsonify,g,flash,session
import sqlite3

app = Flask(__name__)
app.secret_key ='spbYO0JJ0PUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
db = sqlite3.connect('data.db', check_same_thread=False)

# Rutas permisos
@app.route('/', methods=['GET']) # / Ruta del Menu principal 
def index():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET','POST']) # / Ruta del Login
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    usuario =db.execute(""" select * from usuarios where email = ? and password = ? """,(email,password)).fetchone()
    if usuario is None:
        flash('Las credenciales no son validas','badge bg-danger')
        return redirect(url_for('login'))
    session['usuario'] = usuario #/ Almacena mi usuario
    return redirect(url_for('index'))

@app.route('/logout',methods=['GET','POST']) #/ Ruta de cerrar sesión
def logout():
    session.clear()
    return redirect(url_for('login'))

#Rutas de Producto
@app.route('/productos', methods=['GET']) # / Ruta de listado de categorias
def productos():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    
    productos = db.execute("""select id_pro,producto,categoria,precio,id,nombre from producto, categoria where categoria.id=producto.categoria and producto.usuario = ? """,(session['usuario'][0],))
    return render_template('productos/listar.html', productos=productos)

#Crear Producto
@app.route('/productos/crear', methods=['GET', 'POST']) #/ Ruta de Crear Producto
def crear_producto():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        categorias = db.execute("""select * from categoria where categoria.id_usuario = ? """,(session['usuario'][0],))
        return render_template('productos/crear.html',categorias = categorias)
    
    
    producto = request.form.get('nombre')
    categoria = request.form.get('categoria')
    precio = request.form.get('precio')
    usuario = session['usuario'][0]
    cursor = db.cursor()
    cursor.execute("""insert into producto(
            producto,
            categoria,
            precio,
            usuario
        )values (?,?,?,?)
    """, (producto,categoria,precio,usuario))

    db.commit()
    flash("El producto fue creado!!..","success")
    return redirect(url_for('productos'))

#Formulario para actualizar productos
@app.route('/productos/actualizar',methods=['GET','POST',])
def actualizar_producto():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('productos'))

    id = request.form.get('id')
    cursor = db.cursor()
    sql = """ select * from producto as pro where pro.id_pro = ?"""
    cursor.execute(sql,(id,))
    producto = cursor.fetchall()  
    cursor = db.cursor()
    sql = """ select * from categoria as cat where cat.id_usuario = ?"""
    cursor.execute(sql,(session['usuario'][0],))
    categoria = cursor.fetchall()     
    return render_template('productos/actualizar.html',producto =producto,categoria =categoria)

#Actualizar formulario Productos
@app.route('/productos/actualizado', methods=['GET', 'POST'])
def solicitud_producto():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('productos'))
    if request.method == 'POST':
        identificador= request.form.get('identificador')
        producto = request.form.get('nombre')
        categoria = request.form.get('categoria')
        precio = request.form.get('precio')
        usuario = session['usuario'][0]

        cursor = db.cursor()
        cursor.execute("""update producto set
                producto = ?,
                categoria = ?,
                precio = ?,
                usuario = ?
                where id_pro = ?
        """, (producto,categoria,precio,usuario,identificador))
        db.commit()
        flash("El producto fue actualizado!!..","info")
    return redirect(url_for('productos'))

#Eliminar Productos
@app.route('/productos/delete', methods=['GET','POST',])
def delete_producto():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('productos'))
    
    # Si recibe post
    data = request.get_json()
    id = data['id']
    db.execute('DELETE FROM producto WHERE id_pro = ?', (id,))
    db.commit()
    flash("El producto fue eliminado!..","warning")
    return url_for('productos')

#Rutas de Categoria
@app.route('/categorias', methods=['GET']) # / Ruta de listado de categorias
def categorias():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    
    categorias = db.execute("""select * from categoria where categoria.id_usuario = ? """,(session['usuario'][0],))
    return render_template('categorias/listar.html', categorias=categorias)

#Crear 
@app.route('/categorias/crear', methods=['GET', 'POST']) #/ Ruta de Crear Categoria
def crear_categoria():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('categorias/crear.html')
    
    
    nombre = request.form.get('nombre')
    usuario = session['usuario'][0]
    cursor = db.cursor()
    cursor.execute("""insert into categoria(
            nombre,
            id_usuario
        )values (?,?)
    """, (nombre,usuario))

    db.commit()
    flash("La categoria fue creada!!..","success")
    return redirect(url_for('categorias'))

#Formulario para actualizar
@app.route('/categorias/actualizar',methods=['GET','POST',])
def actualizar_categoria():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('categorias'))

    id = request.form.get('id')
    cursor = db.cursor()
    sql = """ select * from categoria as cat where cat.id = ?"""
    cursor.execute(sql,(id,))
    categoria = cursor.fetchall()     
    return render_template('categorias/actualizar.html',categoria =categoria)

#Actualizar formulario
@app.route('/categorias/actualizado', methods=['GET', 'POST'])
def solicitud_categoria():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('categorias'))
    if request.method == 'POST':
        identificador= request.form.get('identificador')
        nombre = request.form.get('nombre')
        usuario = session['usuario'][0]
        print(nombre," ",usuario," ",identificador)
        cursor = db.cursor()
        cursor.execute("""update categoria set
                nombre = ?,
                id_usuario = ?
                where id = ?
        """, (nombre,usuario,identificador))
        db.commit()
        flash("La categoria fue actualizada!!..","info")
    return redirect(url_for('categorias'))

#Eliminar categorias
@app.route('/categorias/delete', methods=['GET','POST',])
def delete_categoria():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('categorias'))
    
    # Si recibe post
    data = request.get_json()
    id = data['id']
    db.execute('DELETE FROM categoria WHERE id = ?', (id,))
    db.commit()
    flash("La categoria fue eliminada!..","warning")
    return url_for('categorias')

#Rutas de usuario
@app.route('/usuario', methods=['GET']) # / Ruta de listado de categorias
def usuario():
    return render_template('index.html')

@app.route('/login/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'GET':
        return render_template('crear.html')
    
    nombres = request.form.get('nombres')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("""insert into usuarios(
            nombres,
            email,
            password
        )values (?,?,?)
    """, (nombres, email, password))
    flash("Usuario creado con exito, ya puedes ingresar!!..","badge bg-success")
    db.commit()

    return redirect(url_for('login'))

#Formulario para actualizar perfil usuario
@app.route('/perfil/actualizar',methods=['GET','POST',])
def actualizar_perfil():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        id = session['usuario'][0]
        cursor = db.cursor()
        sql = """ select * from usuarios  where usuarios.id = ?"""
        cursor.execute(sql,(id,))
        usuario = cursor.fetchall()     
        return render_template('usuarios/actualizar.html',usuario =usuario)

#Actualizar formulario perfil usuario
@app.route('/perfil/actualizado', methods=['GET', 'POST'])
def solicitud_perfil():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('index'))
    if request.method == 'POST':
        
        nombre = request.form.get('nombres')
        email = request.form.get('email')
        usuario = session['usuario'][0]
        password = request.form.get('password')
        cursor = db.cursor()
        cursor.execute("""update usuarios set
                nombres = ?,
                email = ?,
                password = ?
                where id = ?
        """, (nombre,email,password,usuario))
        db.commit()
        flash("El usuario fue actualizado!!..","info")
    return redirect(url_for('index'))
