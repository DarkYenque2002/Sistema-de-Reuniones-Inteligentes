import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
from typing import List, Optional
import streamlit as st
import pandas as pd

class EmailService:
    """Servicio para envío de correos electrónicos de reuniones"""
    
    def __init__(self):
        # Configuración SMTP (Gmail)
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        
    def send_meeting_invitation(
        self,
        recipients: List[str],
        meeting_data: dict,
        include_ics: bool = True
    ) -> bool:
        """
        Envía invitación de reunión por email
        
        Args:
            recipients: Lista de correos electrónicos
            meeting_data: Diccionario con datos de la reunión
            include_ics: Si incluir archivo .ics de calendario
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"📅 Invitación: {meeting_data['title']}"
            
            # Generar cuerpo HTML del email
            html_body = self._generate_email_html(meeting_data)
            
            # Adjuntar HTML
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Adjuntar archivo .ics si se solicita
            if include_ics:
                ics_content = self._generate_ics_file(meeting_data, recipients)
                ics_part = MIMEBase('text', 'calendar', method='REQUEST')
                ics_part.set_payload(ics_content.encode('utf-8'))
                encoders.encode_base64(ics_part)
                ics_part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="reunion_{meeting_data["title"].replace(" ", "_")}.ics"'
                )
                msg.attach(ics_part)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error al enviar email: {str(e)}")
            return False
    
    def _generate_email_html(self, meeting_data: dict) -> str:
        """Genera el HTML del email con el diseño de la invitación"""
        
        # Formatear fecha
        scheduled_at = meeting_data.get('scheduled_at')
        if isinstance(scheduled_at, str):
            scheduled_at = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        
        fecha_formateada = scheduled_at.strftime('%d de %B de %Y') if scheduled_at else 'Fecha por confirmar'
        hora_formateada = scheduled_at.strftime('%I:%M %p') if scheduled_at else 'Hora por confirmar'
        
        # Mapeo de prioridad a colores
        priority_colors = {
            'Alta': '#E74C3C',
            'Media': '#F39C12',
            'Baja': '#3498DB'
        }
        priority_color = priority_colors.get(meeting_data.get('priority', 'Media'), '#F39C12')
        
        # Participantes
        participants = meeting_data.get('participants', [])
        participants_html = '<br>'.join([f'• {p}' for p in participants])
        
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Invitación a Reunión</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7fa;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f7fa; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 40px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 32px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                        📅 Invitación a Reunión
                                    </h1>
                                    <p style="margin: 10px 0 0 0; color: #f0f0f0; font-size: 16px;">
                                        Has sido invitado a la siguiente reunión
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 40px;">
                                    <div style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #e8ecef;">
                                        <h2 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 24px; font-weight: 600;">
                                            {meeting_data.get('title', 'Reunión')}
                                        </h2>
                                        <div style="display: inline-block; background-color: {priority_color}; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                                            🚦 Prioridad {meeting_data.get('priority', 'Media')}
                                        </div>
                                    </div>
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fb; border-radius: 8px; padding: 25px; margin-bottom: 25px;">
                                        <tr>
                                            <td>
                                                <div style="margin-bottom: 20px;">
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="padding-right: 15px; vertical-align: top;">
                                                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                                                                    📅
                                                                </div>
                                                            </td>
                                                            <td style="vertical-align: top;">
                                                                <div style="color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 4px;">
                                                                    Fecha y Hora
                                                                </div>
                                                                <div style="color: #2c3e50; font-size: 16px; font-weight: 600; line-height: 1.4;">
                                                                    {fecha_formateada}
                                                                </div>
                                                                <div style="color: #667eea; font-size: 18px; font-weight: 700; margin-top: 4px;">
                                                                    {hora_formateada}
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                                <div style="margin-bottom: 20px;">
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="padding-right: 15px; vertical-align: top;">
                                                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #3498db, #2980b9); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                                                                    🏢
                                                                </div>
                                                            </td>
                                                            <td style="vertical-align: top;">
                                                                <div style="color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 4px;">
                                                                    Área Responsable
                                                                </div>
                                                                <div style="color: #2c3e50; font-size: 16px; font-weight: 600;">
                                                                    {meeting_data.get('area', 'No especificada')}
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                                <div style="margin-bottom: 20px;">
                                                    <table cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td style="padding-right: 15px; vertical-align: top;">
                                                                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #2ecc71, #27ae60); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                                                                    👥
                                                                </div>
                                                            </td>
                                                            <td style="vertical-align: top;">
                                                                <div style="color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 4px;">
                                                                    Participantes ({len(participants)})
                                                                </div>
                                                                <div style="color: #2c3e50; font-size: 14px; line-height: 1.8;">
                                                                    {participants_html}
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                    {f'''
                                    <div style="background-color: #fff9e6; border-left: 4px solid #f39c12; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
                                        <div style="color: #f39c12; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">
                                            📄 Descripción
                                        </div>
                                        <div style="color: #5d6d7e; font-size: 15px; line-height: 1.6;">
                                            {meeting_data.get('summary', 'No se proporcionó descripción adicional.')}
                                        </div>
                                    </div>
                                    ''' if meeting_data.get('summary') else ''}
                                    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 30px;">
                                        <tr>
                                            <td align="center">
                                                <a href="#" style="display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: #ffffff; text-decoration: none; padding: 16px 40px; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);">
                                                    ✅ Confirmar Asistencia
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e8ecef; text-align: center;">
                                        <p style="margin: 0; color: #95a5a6; font-size: 13px; line-height: 1.6;">
                                            💡 <strong>Importante:</strong> Por favor, confirma tu asistencia lo antes posible.<br>
                                            Si tienes alguna pregunta, contacta al organizador de la reunión.
                                        </p>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #2c3e50; padding: 30px 40px; text-align: center;">
                                    <p style="margin: 0 0 10px 0; color: #ecf0f1; font-size: 14px;">
                                        <strong>Gestor de Reuniones Inteligentes v3.0</strong>
                                    </p>
                                    <p style="margin: 0; color: #95a5a6; font-size: 12px;">
                                        Este es un mensaje automático, por favor no responder directamente a este correo.
                                    </p>
                                    <div style="margin-top: 15px;">
                                        <p style="margin: 0; color: #7f8c8d; font-size: 11px;">
                                            © {datetime.now().year} Sistema de Gestión de Reuniones. Todos los derechos reservados.
                                        </p>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html
    
    def _generate_ics_file(self, meeting_data: dict, recipients: List[str]) -> str:
        """Genera archivo .ics para calendario"""
        
        scheduled_at = meeting_data.get('scheduled_at')
        if isinstance(scheduled_at, str):
            scheduled_at = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        
        end_time = scheduled_at.replace(hour=scheduled_at.hour + 1) if scheduled_at else None
        
        dtstart = scheduled_at.strftime('%Y%m%dT%H%M%S') if scheduled_at else ''
        dtend = end_time.strftime('%Y%m%dT%H%M%S') if end_time else ''
        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
        
        attendees = '\n'.join([f'ATTENDEE;CN={email};RSVP=TRUE:mailto:{email}' for email in recipients])
        
        ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Gestor de Reuniones//ES
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{meeting_data.get('id', 'meeting')}@gestorreuniones.com
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{meeting_data.get('title', 'Reunión')}
DESCRIPTION:{meeting_data.get('summary', 'Reunión programada')}
LOCATION:{meeting_data.get('area', 'Oficina')}
PRIORITY:{meeting_data.get('priority', 'Media')}
STATUS:CONFIRMED
{attendees}
ORGANIZER;CN={self.email_user}:mailto:{self.email_user}
END:VEVENT
END:VCALENDAR
"""
        return ics


def add_email_section_to_dashboard(df):
    """Añade sección de envío de emails al dashboard"""
    st.markdown("### 📧 Enviar Invitaciones por Email")
    
    if df.empty:
        st.info("📭 No hay reuniones para enviar invitaciones")
        return
    
    with st.expander("✉️ Enviar invitación de reunión", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_meeting = st.selectbox(
                "Selecciona la reunión:",
                df["title"].tolist(),
                key="email_meeting_selector"
            )
        
        with col2:
            include_ics = st.checkbox(
                "Incluir archivo calendario (.ics)",
                value=True,
                help="Permite agregar automáticamente al calendario"
            )
        
        meeting = df[df["title"] == selected_meeting].iloc[0]
        
        st.markdown("#### 👁️ Vista previa de la reunión")
        
        scheduled_at = meeting['scheduled_at']
        if isinstance(scheduled_at, str):
            try:
                scheduled_at = pd.to_datetime(scheduled_at)
                fecha_preview = scheduled_at.strftime('%d/%m/%Y %H:%M')
            except:
                fecha_preview = scheduled_at
        elif pd.notna(scheduled_at):
            fecha_preview = scheduled_at.strftime('%d/%m/%Y %H:%M')
        else:
            fecha_preview = 'Sin fecha programada'
        
        col_preview1, col_preview2 = st.columns(2)
        with col_preview1:
            st.info(f"""
            **📝 Título:** {meeting['title']}
            **📅 Fecha:** {fecha_preview}
            **🏢 Área:** {meeting['area']}
            """)
        
        with col_preview2:
            participants = meeting['participants'] if isinstance(meeting['participants'], list) else []
            st.info(f"""
            **🚦 Prioridad:** {meeting['priority']}
            **👥 Participantes:** {len(participants)}
            **📄 Descripción:** {meeting.get('summary', 'Sin descripción')[:50]}...
            """)
        
        st.markdown("#### 📬 Destinatarios")
        
        participants_list = meeting['participants'] if isinstance(meeting['participants'], list) else []
        
        email_option = st.radio(
            "¿Cómo deseas agregar los destinatarios?",
            ["Usar participantes de la reunión", "Ingresar emails manualmente"],
            horizontal=True
        )
        
        if email_option == "Usar participantes de la reunión":
            if not participants_list:
                st.warning("⚠️ Esta reunión no tiene participantes registrados")
                recipients_emails = []
            else:
                recipients_emails = participants_list
                st.success(f"✅ Se enviarán invitaciones a {len(recipients_emails)} participantes")
                with st.expander("Ver destinatarios"):
                    for email in recipients_emails:
                        st.write(f"• {email}")
        else:
            manual_emails = st.text_area(
                "Ingresa los emails separados por comas:",
                placeholder="juan@example.com, maria@example.com, pedro@example.com",
                height=100
            )
            recipients_emails = [e.strip() for e in manual_emails.split(",") if e.strip()]
            
            if recipients_emails:
                st.success(f"✅ {len(recipients_emails)} destinatario(s) agregado(s)")
        
        col_send1, col_send2, col_send3 = st.columns([1, 1, 2])
        
        with col_send1:
            send_button = st.button(
                "📧 Enviar Invitaciones",
                use_container_width=True,
                type="primary",
                disabled=not recipients_emails
            )
        
        with col_send2:
            test_button = st.button(
                "🧪 Enviar Prueba",
                use_container_width=True,
                help="Envía solo a tu email para probar"
            )
        
        if send_button:
            if not recipients_emails:
                st.error("⚠️ Debes agregar al menos un destinatario")
            else:
                with st.spinner("📤 Enviando invitaciones..."):
                    email_service = EmailService()
                    
                    meeting_data = {
                        'id': meeting['id'],
                        'title': meeting['title'],
                        'summary': meeting.get('summary', ''),
                        'scheduled_at': meeting['scheduled_at'],
                        'area': meeting['area'],
                        'priority': meeting['priority'],
                        'participants': participants_list
                    }
                    
                    success = email_service.send_meeting_invitation(
                        recipients=recipients_emails,
                        meeting_data=meeting_data,
                        include_ics=include_ics
                    )
                    
                    if success:
                        st.success(f"✅ Invitaciones enviadas correctamente a {len(recipients_emails)} destinatarios!")
                        st.balloons()
                    else:
                        st.error("❌ Hubo un error al enviar las invitaciones")
        
        if test_button:
            email_service = EmailService()
            test_email = email_service.email_user
            
            if test_email:
                with st.spinner(f"📤 Enviando email de prueba a {test_email}..."):
                    meeting_data = {
                        'id': meeting['id'],
                        'title': meeting['title'],
                        'summary': meeting.get('summary', ''),
                        'scheduled_at': meeting['scheduled_at'],
                        'area': meeting['area'],
                        'priority': meeting['priority'],
                        'participants': participants_list
                    }
                    
                    success = email_service.send_meeting_invitation(
                        recipients=[test_email],
                        meeting_data=meeting_data,
                        include_ics=include_ics
                    )
                    
                    if success:
                        st.success(f"✅ Email de prueba enviado a {test_email}")
                    else:
                        st.error("❌ Error al enviar email de prueba")
            else:
                st.error("⚠️ No se encontró email configurado en las variables de entorno")