from app import app, usuarios
from flask import render_template, request, redirect, session
import yagmail
import threading

 # Asegúrate de tener una clave secreta segura

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("frmLogin.html")
    else:
        if request.method == 'POST':
            username = request.form['txtUsername']
            password = request.form['txtPassword']
            usuario = {
                "username": username,
                "password": password
            }
            userExiste = usuarios.find_one(usuario)
            if userExiste:
                # Crear variable de sesión user
                session['user'] = usuario   
                
                # Configurar Yagmail
                email = yagmail.SMTP("royersolarte22@gmail.com", open(".password").read(), encoding='UTF-8')
                asunto = "Reporte ingreso al sistema usuario"
                mensaje = f"Se informa que el usuario {username} ha ingresado al sistema"
                
                # Enviar correo electrónico en un hilo separado
                thread = threading.Thread(target=enviarCorreo, args=(email, "royersolarte22@gmail.com", asunto, mensaje))
                thread.start()

                return redirect("/listarProductos")
            else:
                mensaje = "Credenciales de ingreso no válidas"
                return render_template("frmLogin.html", mensaje=mensaje)

@app.route("/salir")
def salir():
    session.pop('user', None)
    session.clear()
    return render_template("frmLogin.html", mensaje="Ha cerrado la sesión..")

# Función que envía correo electrónico
def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None):
    email.send(to=destinatario, subject=asunto, contents=mensaje)
