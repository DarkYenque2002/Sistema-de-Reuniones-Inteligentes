import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_gmail_connection():
    """Prueba la conexión SMTP con Gmail"""
    
    # Obtener credenciales
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    print("🔍 Verificando configuración...")
    print(f"   Email: {email_user}")
    print(f"   Servidor SMTP: {smtp_server}")
    print(f"   Puerto: {smtp_port}")
    print(f"   Contraseña configurada: {'✅ Sí' if email_password else '❌ No'}")
    print()
    
    if not email_user or not email_password:
        print("❌ ERROR: EMAIL_USER o EMAIL_PASSWORD no están configurados en .env")
        print()
        print("📝 Instrucciones:")
        print("   1. Crea un archivo .env en la raíz del proyecto")
        print("   2. Agrega las siguientes líneas:")
        print("      EMAIL_USER=tu_email@gmail.com")
        print("      EMAIL_PASSWORD=tu_contraseña_de_aplicación")
        print("      SMTP_SERVER=smtp.gmail.com")
        print("      SMTP_PORT=587")
        return False
    
    try:
        print("🔄 Intentando conectar con Gmail...")
        
        # Crear mensaje de prueba
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user  # Enviar a ti mismo
        msg['Subject'] = "🧪 Prueba de Conexión - Gestor de Reuniones"
        
        body = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f7fa;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #4CAF50; text-align: center;">✅ ¡Conexión Exitosa!</h2>
                <p style="font-size: 16px; color: #333; line-height: 1.6;">
                    Tu configuración de Gmail está funcionando correctamente.
                </p>
                <p style="font-size: 16px; color: #333; line-height: 1.6;">
                    Ahora puedes enviar invitaciones de reuniones desde tu aplicación.
                </p>
                <hr style="border: none; border-top: 2px solid #e8ecef; margin: 25px 0;">
                <div style="background-color: #f8f9fb; padding: 20px; border-radius: 8px; margin-top: 20px;">
                    <h3 style="color: #667eea; margin-top: 0;">📋 Información de la prueba:</h3>
                    <ul style="color: #5d6d7e; line-height: 1.8;">
                        <li><strong>Servidor SMTP:</strong> smtp.gmail.com</li>
                        <li><strong>Puerto:</strong> 587</li>
                        <li><strong>Email configurado:</strong> {}</li>
                        <li><strong>Estado:</strong> ✅ Funcionando correctamente</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 30px;">
                    <p style="color: #95a5a6; font-size: 14px;">
                        🚀 ¡Listo para usar el Gestor de Reuniones Inteligentes v3.0!
                    </p>
                </div>
                <hr style="border: none; border-top: 1px solid #e8ecef; margin: 25px 0;">
                <p style="color: #999; font-size: 12px; text-align: center; margin-bottom: 0;">
                    Este es un mensaje de prueba automático del Gestor de Reuniones.<br>
                    Si recibiste este email, tu configuración es correcta.
                </p>
            </div>
        </body>
        </html>
        """.format(email_user)
        
        msg.attach(MIMEText(body, 'html'))
        
        # Conectar y enviar
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(0)  # Cambiar a 1 para ver logs detallados
            print("   ↳ Iniciando TLS...")
            server.starttls()
            
            print("   ↳ Autenticando...")
            server.login(email_user, email_password)
            
            print("   ↳ Enviando email de prueba...")
            server.send_message(msg)
        
        print()
        print("=" * 60)
        print("✅ ¡ÉXITO! Email de prueba enviado correctamente")
        print("=" * 60)
        print()
        print(f"📬 Revisa tu bandeja de entrada: {email_user}")
        print("   (Si no lo ves, revisa la carpeta de spam)")
        print()
        print("🎉 Tu configuración está lista para usar en la aplicación")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print()
        print("=" * 60)
        print("❌ ERROR DE AUTENTICACIÓN")
        print("=" * 60)
        print()
        print("Posibles causas:")
        print("   1. La contraseña de aplicación es incorrecta")
        print("   2. No has activado la verificación en 2 pasos")
        print("   3. No generaste una contraseña de aplicación")
        print()
        print("🔧 Pasos para solucionar:")
        print()
        print("   PASO 1: Activar verificación en 2 pasos")
        print("   → Ve a: https://myaccount.google.com/security")
        print("   → Busca 'Verificación en 2 pasos' y actívala")
        print()
        print("   PASO 2: Generar contraseña de aplicación")
        print("   → Ve a: https://myaccount.google.com/apppasswords")
        print("   → Selecciona 'Correo' y 'Otro (nombre personalizado)'")
        print("   → Copia la contraseña de 16 caracteres")
        print()
        print("   PASO 3: Actualizar archivo .env")
        print("   → Pega la contraseña en EMAIL_PASSWORD de tu .env")
        print("   → NO uses tu contraseña normal de Gmail")
        print()
        return False
        
    except smtplib.SMTPException as e:
        print()
        print("=" * 60)
        print("❌ ERROR SMTP")
        print("=" * 60)
        print()
        print(f"Mensaje de error: {str(e)}")
        print()
        print("Posibles causas:")
        print("   1. El servidor SMTP está bloqueado")
        print("   2. El puerto es incorrecto (debe ser 587)")
        print("   3. Problemas de conexión a internet")
        print()
        print("🔧 Verifica:")
        print("   → SMTP_SERVER=smtp.gmail.com")
        print("   → SMTP_PORT=587")
        print("   → Tu conexión a internet")
        print()
        return False
        
    except ConnectionRefusedError:
        print()
        print("=" * 60)
        print("❌ ERROR DE CONEXIÓN")
        print("=" * 60)
        print()
        print("No se pudo conectar al servidor SMTP")
        print()
        print("Posibles causas:")
        print("   1. Firewall bloqueando el puerto 587")
        print("   2. Sin conexión a internet")
        print("   3. El puerto SMTP es incorrecto")
        print()
        print("🔧 Verifica tu configuración de red y firewall")
        print()
        return False
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR INESPERADO")
        print("=" * 60)
        print()
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print()
        print("Si el problema persiste, verifica:")
        print("   1. Que el archivo .env esté en la raíz del proyecto")
        print("   2. Que las variables estén correctamente escritas")
        print("   3. Que no haya espacios extra en las variables")
        print()
        return False


def show_configuration_guide():
    """Muestra una guía de configuración completa"""
    print()
    print("=" * 60)
    print("  📖 GUÍA DE CONFIGURACIÓN DE GMAIL")
    print("=" * 60)
    print()
    print("Para usar el envío de emails, necesitas:")
    print()
    print("1️⃣  ARCHIVO .env en la raíz del proyecto:")
    print()
    print("    EMAIL_USER=tu_email@gmail.com")
    print("    EMAIL_PASSWORD=xxxx xxxx xxxx xxxx")
    print("    SMTP_SERVER=smtp.gmail.com")
    print("    SMTP_PORT=587")
    print()
    print("2️⃣  CONTRASEÑA DE APLICACIÓN de Google:")
    print()
    print("    a) Ve a: https://myaccount.google.com/security")
    print("    b) Activa 'Verificación en 2 pasos'")
    print("    c) Ve a: https://myaccount.google.com/apppasswords")
    print("    d) Genera una contraseña para 'Correo'")
    print("    e) Copia la contraseña de 16 caracteres")
    print("    f) Pégala en EMAIL_PASSWORD (sin espacios)")
    print()
    print("3️⃣  IMPORTANTE:")
    print()
    print("    ⚠️  NO uses tu contraseña normal de Gmail")
    print("    ⚠️  DEBES usar una contraseña de aplicación")
    print("    ⚠️  El archivo .env NO debe subirse a Git")
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  🧪 TEST DE CONEXIÓN GMAIL - GESTOR DE REUNIONES")
    print("=" * 60)
    print()
    
    # Verificar si existe el archivo .env
    if not os.path.exists('.env'):
        print("⚠️  ADVERTENCIA: No se encontró el archivo .env")
        print()
        show_configuration_guide()
        print("Crea el archivo .env y vuelve a ejecutar este script.")
        print()
        print("=" * 60)
        exit(1)
    
    # Ejecutar prueba
    success = test_gmail_connection()
    
    print()
    if success:
        print("=" * 60)
        print("  ✅ CONFIGURACIÓN COMPLETA Y FUNCIONANDO")
        print("=" * 60)
        print()
        print("Siguiente paso:")
        print("  → Ejecuta tu aplicación: streamlit run app.py")
        print()
    else:
        print("=" * 60)
        print("  ❌ CONFIGURACIÓN INCOMPLETA")
        print("=" * 60)
        print()
        print("Sigue las instrucciones anteriores y vuelve a intentar.")
        print()
        print("Si necesitas ayuda, revisa la guía completa:")
        show_configuration_guide()
    
    print("=" * 60)
    print()