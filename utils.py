# -*- coding: utf-8 -*-
import datetime 
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

def fibonacci_series(x, y, n):
    if n <= 0:
        return []  # Retorna una lista vacía si n es negativo o cero
    
    if x == 0 and y == 0:
        return []
    
    if x < 0 or y < 0:
        return []
    
    series = [x, y]
    while len(series) < n:
        next_num = series[-1] + series[-2]  # Siguiente número es la suma de los dos últimos
        series.append(next_num)  # Añadir el siguiente número al final de la lista
    
    return list(reversed(series))


def get_seeds_from_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Obtener la hora actual
    current_time_split  =current_time.split(":")
    seed_x = int(current_time_split[1])//10  # Obtener el segundo dígito para la semilla x
    seed_y = int(current_time_split[1])%10  # Obtener el tercer dígito para la semilla y
    seconds = int(current_time_split[2])  # Obtener los segundos para la cantidad de números
    return seed_x, seed_y, seconds, current_time  # Devolver las semillas, los segundos y la hora actual

def enviar_correo(mensaje, email_1, email_2, current_time):
    remitente = "<danielfuentesardila@gmail.com>"
    destinatario1 = f"<{email_1}>"
    destinatario2 = f"<{email_2}>" if email_2 else None
    
    # Crear un objeto MIMEMultipart
    email = MIMEMultipart()
    email['From'] = remitente
    email['To'] = ", ".join(filter(None, [destinatario1, destinatario2]))
    email['Subject'] = "Prueba Técnica - Daniel Alejandro Fuentes Ardila"
    
    # Agregar el mensaje como parte del correo electrónico
    mensaje = f"""<b>Hora Actual:</b> {current_time}<br><b>Serie Generada:</b> {mensaje}"""
    
    email.attach(MIMEText(mensaje, 'html'))

    try:
        # Configurar el servidor SMTP de Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Puerto para TLS
        smtp_username = 'danielfuentesardila@gmail.com'  # Tu dirección de correo electrónico
        smtp_password = 'dvzw rpir xkwz bjib'  # Tu contraseña de aplicación específica para Gmail

        # Iniciar una conexión segura al servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

         # Iniciar sesión en el servidor SMTP de Gmail
        server.login(smtp_username, smtp_password)

        # Enviar el correo electrónico
        destinatarios = filter(None, [destinatario1, destinatario2])
        server.sendmail(remitente, ", ".join(destinatarios), email.as_string())
        
        # Cerrar la conexión con el servidor SMTP
        server.quit()

        print("Correo enviado exitosamente.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: el mensaje no pudo enviarse.")
