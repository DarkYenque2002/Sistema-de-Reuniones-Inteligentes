import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import uuid

# 🔧 Cargar variables de entorno (¡IMPORTANTE!)
load_dotenv()

# 📧 Importar el servicio de email
from email_service import EmailService, add_email_section_to_dashboard

# ===============================================
# CONFIGURACIÓN DE LA PÁGINA
# ===============================================
st.set_page_config(
    page_title="Gestor de Reuniones v3.0",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================================
# INICIALIZAR SESSION STATE (para persistir datos)
# ===============================================
if 'reuniones' not in st.session_state:
    # Datos de ejemplo iniciales
    st.session_state.reuniones = pd.DataFrame({
        'id': ['reunion_1', 'reunion_2', 'reunion_3'],
        'title': [
            'Reunión de Planificación Q4',
            'Review Técnico Backend',
            'Presentación Proyecto Alpha'
        ],
        'area': ['Gerencia', 'Desarrollo', 'Marketing'],
        'priority': ['Alta', 'Media', 'Baja'],
        'scheduled_at': [
            datetime(2025, 11, 15, 10, 0),
            datetime(2025, 11, 16, 14, 30),
            datetime(2025, 11, 20, 9, 0)
        ],
        'summary': [
            'Revisión de objetivos y metas para el último trimestre del año',
            'Análisis de arquitectura y optimización de servicios backend',
            'Presentación final del proyecto Alpha al equipo directivo'
        ],
        'participants': [
            ['juan.perez@empresa.com', 'maria.garcia@empresa.com', 'carlos.lopez@empresa.com'],
            ['dev1@empresa.com', 'dev2@empresa.com', 'techlead@empresa.com'],
            ['marketing@empresa.com', 'gerencia@empresa.com', 'ventas@empresa.com']
        ]
    })

# ===============================================
# FUNCIONES CRUD
# ===============================================

def crear_reunion(titulo, area, prioridad, fecha, hora, descripcion, participantes_list):
    """Crea una nueva reunión"""
    nueva_reunion = pd.DataFrame({
        'id': [f'reunion_{uuid.uuid4().hex[:8]}'],
        'title': [titulo],
        'area': [area],
        'priority': [prioridad],
        'scheduled_at': [datetime.combine(fecha, hora)],
        'summary': [descripcion],
        'participants': [participantes_list]
    })
    
    st.session_state.reuniones = pd.concat(
        [st.session_state.reuniones, nueva_reunion], 
        ignore_index=True
    )
    return True

def actualizar_reunion(reunion_id, titulo, area, prioridad, fecha, hora, descripcion, participantes_list):
    """Actualiza una reunión existente"""
    idx = st.session_state.reuniones[st.session_state.reuniones['id'] == reunion_id].index[0]
    
    st.session_state.reuniones.at[idx, 'title'] = titulo
    st.session_state.reuniones.at[idx, 'area'] = area
    st.session_state.reuniones.at[idx, 'priority'] = prioridad
    st.session_state.reuniones.at[idx, 'scheduled_at'] = datetime.combine(fecha, hora)
    st.session_state.reuniones.at[idx, 'summary'] = descripcion
    st.session_state.reuniones.at[idx, 'participants'] = participantes_list
    return True

def eliminar_reunion(reunion_id):
    """Elimina una reunión"""
    st.session_state.reuniones = st.session_state.reuniones[
        st.session_state.reuniones['id'] != reunion_id
    ].reset_index(drop=True)
    return True

def buscar_reuniones(query, filtro_area=None, filtro_prioridad=None):
    """Busca reuniones por título, área o prioridad"""
    df = st.session_state.reuniones.copy()
    
    # Filtro por texto
    if query:
        mask = df['title'].str.contains(query, case=False, na=False) | \
               df['summary'].str.contains(query, case=False, na=False)
        df = df[mask]
    
    # Filtro por área
    if filtro_area and filtro_area != 'Todas':
        df = df[df['area'] == filtro_area]
    
    # Filtro por prioridad
    if filtro_prioridad and filtro_prioridad != 'Todas':
        df = df[df['priority'] == filtro_prioridad]
    
    return df

# ===============================================
# TÍTULO PRINCIPAL
# ===============================================
st.title("📅 Gestor de Reuniones Inteligentes v3.0")
st.markdown("---")

# ===============================================
# SIDEBAR
# ===============================================
with st.sidebar:
    st.header("⚙️ Configuración")
    st.info("Sistema de gestión de reuniones con CRUD completo")
    
    # Verificar configuración de email
    email_service = EmailService()
    if email_service.email_user:
        st.success(f"✅ Email: {email_service.email_user}")
    else:
        st.error("❌ Email no configurado")
    
    st.markdown("---")
    
    # Estadísticas rápidas
    st.markdown("### 📊 Resumen Rápido")
    total_reuniones = len(st.session_state.reuniones)
    st.metric("Total Reuniones", total_reuniones)
    
    if not st.session_state.reuniones.empty:
        alta_prioridad = len(st.session_state.reuniones[st.session_state.reuniones['priority'] == 'Alta'])
        st.metric("Prioridad Alta", alta_prioridad)

# ===============================================
# OBTENER DATAFRAME ACTUAL
# ===============================================
df_reuniones = st.session_state.reuniones

# ===============================================
# SECCIÓN PRINCIPAL CON TABS
# ===============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", 
    "🔍 Buscar", 
    "➕ Crear", 
    "✏️ Actualizar", 
    "🗑️ Eliminar",
    "📧 Enviar Email"
])

# ===============================================
# TAB 1: DASHBOARD INTERACTIVO
# ===============================================
with tab1:
    st.header("📊 Dashboard de Reuniones")
    
    if not df_reuniones.empty:
        # ========== MÉTRICAS PRINCIPALES ==========
        st.markdown("### 📈 Métricas Clave")
        
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        total_reuniones = len(df_reuniones)
        total_participantes = sum([len(p) for p in df_reuniones['participants']])
        promedio_participantes = round(total_participantes / total_reuniones, 1) if total_reuniones > 0 else 0
        reuniones_alta = len(df_reuniones[df_reuniones['priority'] == 'Alta'])
        
        with col_metric1:
            st.metric(
                label="Total Reuniones",
                value=total_reuniones,
                delta=f"{total_reuniones} activas",
                help="Número total de reuniones programadas"
            )
        
        with col_metric2:
            st.metric(
                label="Prioridad Alta",
                value=reuniones_alta,
                delta=f"{round(reuniones_alta/total_reuniones*100, 1)}% del total" if total_reuniones > 0 else "0%",
                help="Reuniones marcadas como alta prioridad"
            )
        
        with col_metric3:
            st.metric(
                label="Total Participantes",
                value=total_participantes,
                help="Suma de todos los participantes"
            )
        
        with col_metric4:
            st.metric(
                label="Promedio por Reunión",
                value=f"{promedio_participantes}",
                help="Participantes promedio por reunión"
            )
        
        st.markdown("---")
        
        # ========== GRÁFICOS INTERACTIVOS ==========
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            st.markdown("#### 📊 Reuniones por Área")
            area_counts = df_reuniones['area'].value_counts()
            st.bar_chart(area_counts, height=300)
            
            # Tabla de resumen por área
            with st.expander("📋 Ver detalles por área"):
                for area, count in area_counts.items():
                    participantes_area = sum([len(p) for p in df_reuniones[df_reuniones['area'] == area]['participants']])
                    st.write(f"**{area}:** {count} reuniones - {participantes_area} participantes")
        
        with col_graph2:
            st.markdown("#### 🚦 Distribución por Prioridad")
            priority_counts = df_reuniones['priority'].value_counts()
            
            # Ordenar por prioridad
            priority_order = ['Alta', 'Media', 'Baja']
            priority_counts = priority_counts.reindex([p for p in priority_order if p in priority_counts.index])
            
            st.bar_chart(priority_counts, height=300, color="#FF6B6B")
            
            # Porcentajes
            with st.expander("📊 Ver porcentajes"):
                for priority, count in priority_counts.items():
                    percentage = round(count/total_reuniones*100, 1)
                    st.write(f"**{priority}:** {count} ({percentage}%)")
        
        st.markdown("---")
        
        # ========== LÍNEA DE TIEMPO ==========
        st.markdown("### 📅 Línea de Tiempo de Reuniones")
        
        # Preparar datos para gráfico de línea de tiempo
        df_timeline = df_reuniones.copy()
        df_timeline['fecha'] = pd.to_datetime(df_timeline['scheduled_at']).dt.date
        timeline_counts = df_timeline.groupby('fecha').size().reset_index(name='reuniones')
        
        if len(timeline_counts) > 0:
            st.line_chart(timeline_counts.set_index('fecha')['reuniones'], height=250)
        
        st.markdown("---")
        
        # ========== FILTROS INTERACTIVOS ==========
        st.markdown("### 🔍 Filtros de Búsqueda")
        
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            areas_disponibles = ['Todas'] + sorted(df_reuniones['area'].unique().tolist())
            filtro_area = st.selectbox("Filtrar por área:", areas_disponibles, key="tab1_area")
        
        with col_filtro2:
            prioridades_disponibles = ['Todas'] + ['Alta', 'Media', 'Baja']
            filtro_prioridad = st.selectbox("Filtrar por prioridad:", prioridades_disponibles, key="tab1_priority")
        
        with col_filtro3:
            orden = st.selectbox("Ordenar por:", ["Fecha", "Prioridad", "Área"], key="tab1_orden")
        
        # Aplicar filtros
        df_filtrado = df_reuniones.copy()
        
        if filtro_area != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['area'] == filtro_area]
        
        if filtro_prioridad != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['priority'] == filtro_prioridad]
        
        # Aplicar ordenamiento
        if orden == "Fecha":
            df_filtrado = df_filtrado.sort_values('scheduled_at')
        elif orden == "Prioridad":
            prioridad_orden = {'Alta': 1, 'Media': 2, 'Baja': 3}
            df_filtrado['prioridad_num'] = df_filtrado['priority'].map(prioridad_orden)
            df_filtrado = df_filtrado.sort_values('prioridad_num')
            df_filtrado = df_filtrado.drop('prioridad_num', axis=1)
        else:
            df_filtrado = df_filtrado.sort_values('area')
        
        st.markdown(f"**📋 Mostrando {len(df_filtrado)} de {len(df_reuniones)} reuniones**")
        
        st.markdown("---")
        
        # ========== TARJETAS DE REUNIONES ==========
        st.markdown("### 📋 Listado de Reuniones")
        
        # Crear tarjetas interactivas para cada reunión
        for idx, reunion in df_filtrado.iterrows():
            # Color según prioridad
            if reunion['priority'] == 'Alta':
                border_color = "#E74C3C"
                emoji = "🔴"
            elif reunion['priority'] == 'Media':
                border_color = "#F39C12"
                emoji = "🟡"
            else:
                border_color = "#3498DB"
                emoji = "🟢"
            
            fecha_formateada = reunion['scheduled_at'].strftime('%d/%m/%Y %H:%M')
            
            with st.expander(f"{emoji} **{reunion['title']}** - {fecha_formateada}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    **📝 Descripción:**  
                    {reunion['summary'][:150]}{'...' if len(reunion['summary']) > 150 else ''}
                    
                    **🏢 Área:** {reunion['area']}  
                    **🚦 Prioridad:** {reunion['priority']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **📅 Fecha:**  
                    {reunion['scheduled_at'].strftime('%d/%m/%Y')}
                    
                    **🕐 Hora:**  
                    {reunion['scheduled_at'].strftime('%H:%M')}
                    """)
                
                with col3:
                    num_participantes = len(reunion['participants'])
                    st.markdown(f"""
                    **👥 Participantes:**  
                    {num_participantes} persona(s)
                    
                    **🆔 ID:**  
                    {reunion['id'][:12]}...
                    """)
                
                # Botones de acción
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button("👥 Ver Participantes", key=f"ver_part_{reunion['id']}", use_container_width=True):
                        st.write("**Lista de participantes:**")
                        for i, email in enumerate(reunion['participants'], 1):
                            st.write(f"{i}. {email}")
                
                with col_btn2:
                    if st.button("📄 Ver Completo", key=f"ver_full_{reunion['id']}", use_container_width=True):
                        st.info(f"**Descripción completa:**\n\n{reunion['summary']}")
                
                with col_btn3:
                    if st.button("📧 Enviar Email", key=f"send_{reunion['id']}", use_container_width=True):
                        st.success(f"Ve a la pestaña 'Enviar Email' para enviar invitación")
        
        st.markdown("---")
        
        # ========== PRÓXIMAS REUNIONES ==========
        st.markdown("### ⏰ Próximas 3 Reuniones")
        
        df_proximas = df_reuniones.sort_values('scheduled_at').head(3)
        
        cols_proximas = st.columns(3)
        
        for idx, (_, reunion) in enumerate(df_proximas.iterrows()):
            with cols_proximas[idx]:
                # Color según prioridad
                if reunion['priority'] == 'Alta':
                    color = "#FFEBEE"
                elif reunion['priority'] == 'Media':
                    color = "#FFF8E1"
                else:
                    color = "#E3F2FD"
                
                st.markdown(f"""
                <div style='background-color: {color}; padding: 20px; border-radius: 10px; border-left: 5px solid {"#E74C3C" if reunion["priority"] == "Alta" else "#F39C12" if reunion["priority"] == "Media" else "#3498DB"}'>
                    <h4 style='margin: 0; color: #2c3e50;'>{reunion['title']}</h4>
                    <p style='margin: 10px 0 5px 0; color: #5d6d7e;'><strong>📅</strong> {reunion['scheduled_at'].strftime('%d/%m/%Y %H:%M')}</p>
                    <p style='margin: 5px 0; color: #5d6d7e;'><strong>🏢</strong> {reunion['area']}</p>
                    <p style='margin: 5px 0; color: #5d6d7e;'><strong>👥</strong> {len(reunion['participants'])} participantes</p>
                </div>
                """, unsafe_allow_html=True)
        
    else:
        st.warning("📭 No hay reuniones programadas")
        st.info("👉 Ve a la pestaña '➕ Crear' para agregar tu primera reunión")

# ===============================================
# TAB 2: BUSCAR REUNIONES
# ===============================================
with tab2:
    st.header("🔍 Buscar Reuniones")
    
    col_search1, col_search2, col_search3 = st.columns([2, 1, 1])
    
    with col_search1:
        query_busqueda = st.text_input(
            "Buscar por título o descripción:",
            placeholder="Escribe palabras clave...",
            key="search_query"
        )
    
    with col_search2:
        areas_disponibles = ['Todas'] + sorted(df_reuniones['area'].unique().tolist())
        filtro_area_busqueda = st.selectbox("Área:", areas_disponibles, key="search_area")
    
    with col_search3:
        filtro_prioridad_busqueda = st.selectbox("Prioridad:", ['Todas', 'Alta', 'Media', 'Baja'], key="search_priority")
    
    # Realizar búsqueda
    if query_busqueda or filtro_area_busqueda != 'Todas' or filtro_prioridad_busqueda != 'Todas':
        resultados = buscar_reuniones(query_busqueda, filtro_area_busqueda, filtro_prioridad_busqueda)
        
        st.markdown(f"### 📊 Resultados: {len(resultados)} reunión(es) encontrada(s)")
        
        if not resultados.empty:
            for idx, reunion in resultados.iterrows():
                with st.expander(f"📅 {reunion['title']} - {reunion['scheduled_at'].strftime('%d/%m/%Y %H:%M')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🏢 Área:** {reunion['area']}")
                        st.write(f"**🚦 Prioridad:** {reunion['priority']}")
                        st.write(f"**👥 Participantes:** {len(reunion['participants'])}")
                    
                    with col2:
                        st.write(f"**📝 ID:** {reunion['id']}")
                        st.write(f"**📄 Descripción:**")
                        st.write(reunion['summary'][:100] + "...")
        else:
            st.info("No se encontraron reuniones con los criterios especificados")
    else:
        st.info("👆 Ingresa un término de búsqueda o selecciona filtros para comenzar")

# ===============================================
# TAB 3: CREAR NUEVA REUNIÓN
# ===============================================
with tab3:
    st.header("➕ Crear Nueva Reunión")
    
    with st.form("nueva_reunion_form"):
        st.markdown("### 📝 Información de la Reunión")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nuevo_titulo = st.text_input("Título *", placeholder="Ej: Reunión de Equipo")
            nueva_area = st.selectbox("Área *", ["Gerencia", "Desarrollo", "Marketing", "Ventas", "RRHH", "Operaciones"])
            nueva_prioridad = st.selectbox("Prioridad *", ["Alta", "Media", "Baja"])
        
        with col2:
            nueva_fecha = st.date_input("Fecha *", min_value=datetime.now().date())
            nueva_hora = st.time_input("Hora *", value=datetime.now().time())
        
        nueva_descripcion = st.text_area(
            "Descripción / Agenda *",
            placeholder="Describe el propósito de la reunión...",
            height=100
        )
        
        st.markdown("### 👥 Participantes")
        nuevos_participantes = st.text_area(
            "Emails (uno por línea) *",
            placeholder="juan@empresa.com\nmaria@empresa.com",
            height=120
        )
        
        submitted = st.form_submit_button("✅ Crear Reunión", use_container_width=True, type="primary")
        
        if submitted:
            if not nuevo_titulo or not nueva_descripcion or not nuevos_participantes:
                st.error("⚠️ Completa todos los campos obligatorios")
            else:
                emails_list = [email.strip() for email in nuevos_participantes.split('\n') if email.strip()]
                
                if crear_reunion(nuevo_titulo, nueva_area, nueva_prioridad, nueva_fecha, nueva_hora, nueva_descripcion, emails_list):
                    st.success(f"✅ Reunión '{nuevo_titulo}' creada exitosamente!")
                    st.balloons()
                    st.rerun()

# ===============================================
# TAB 4: ACTUALIZAR REUNIÓN
# ===============================================
with tab4:
    st.header("✏️ Actualizar Reunión")
    
    if not df_reuniones.empty:
        # Seleccionar reunión a actualizar
        reunion_actualizar = st.selectbox(
            "Selecciona la reunión a actualizar:",
            df_reuniones['title'].tolist(),
            key="update_select"
        )
        
        reunion_actual = df_reuniones[df_reuniones['title'] == reunion_actualizar].iloc[0]
        
        st.markdown("---")
        
        with st.form("actualizar_reunion_form"):
            st.markdown("### 📝 Editar Información")
            
            col1, col2 = st.columns(2)
            
            with col1:
                upd_titulo = st.text_input("Título *", value=reunion_actual['title'])
                upd_area = st.selectbox(
                    "Área *", 
                    ["Gerencia", "Desarrollo", "Marketing", "Ventas", "RRHH", "Operaciones"],
                    index=["Gerencia", "Desarrollo", "Marketing", "Ventas", "RRHH", "Operaciones"].index(reunion_actual['area']) if reunion_actual['area'] in ["Gerencia", "Desarrollo", "Marketing", "Ventas", "RRHH", "Operaciones"] else 0
                )
                upd_prioridad = st.selectbox(
                    "Prioridad *",
                    ["Alta", "Media", "Baja"],
                    index=["Alta", "Media", "Baja"].index(reunion_actual['priority'])
                )
            
            with col2:
                upd_fecha = st.date_input("Fecha *", value=reunion_actual['scheduled_at'].date())
                upd_hora = st.time_input("Hora *", value=reunion_actual['scheduled_at'].time())
            
            upd_descripcion = st.text_area(
                "Descripción *",
                value=reunion_actual['summary'],
                height=100
            )
            
            st.markdown("### 👥 Participantes")
            participantes_actuales = '\n'.join(reunion_actual['participants'])
            upd_participantes = st.text_area(
                "Emails (uno por línea) *",
                value=participantes_actuales,
                height=120
            )
            
            submitted_update = st.form_submit_button("💾 Guardar Cambios", use_container_width=True, type="primary")
            
            if submitted_update:
                emails_list = [email.strip() for email in upd_participantes.split('\n') if email.strip()]
                
                if actualizar_reunion(
                    reunion_actual['id'],
                    upd_titulo,
                    upd_area,
                    upd_prioridad,
                    upd_fecha,
                    upd_hora,
                    upd_descripcion,
                    emails_list
                ):
                    st.success(f"✅ Reunión actualizada exitosamente!")
                    st.balloons()
                    st.rerun()
    else:
        st.info("📭 No hay reuniones para actualizar")

# ===============================================
# TAB 5: ELIMINAR REUNIÓN
# ===============================================
with tab5:
    st.header("🗑️ Eliminar Reunión")
    
    if not df_reuniones.empty:
        st.warning("⚠️ **ADVERTENCIA:** Esta acción no se puede deshacer")
        
        reunion_eliminar = st.selectbox(
            "Selecciona la reunión a eliminar:",
            df_reuniones['title'].tolist(),
            key="delete_select"
        )
        
        reunion_a_eliminar = df_reuniones[df_reuniones['title'] == reunion_eliminar].iloc[0]
        
        # Vista previa
        st.markdown("### 👁️ Vista previa de la reunión a eliminar")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"""
            **📝 Título:** {reunion_a_eliminar['title']}
            **🏢 Área:** {reunion_a_eliminar['area']}
            **🚦 Prioridad:** {reunion_a_eliminar['priority']}
            """)
        
        with col2:
            fecha = reunion_a_eliminar['scheduled_at'].strftime('%d/%m/%Y %H:%M')
            st.info(f"""
            **📅 Fecha:** {fecha}
            **👥 Participantes:** {len(reunion_a_eliminar['participants'])}
            **📄 ID:** {reunion_a_eliminar['id']}
            """)
        
        st.markdown("---")
        
        # Confirmación
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            if st.button("🗑️ Eliminar Reunión", type="primary", use_container_width=True):
                if eliminar_reunion(reunion_a_eliminar['id']):
                    st.success("✅ Reunión eliminada exitosamente!")
                    st.rerun()
        
        with col_btn2:
            if st.button("❌ Cancelar", use_container_width=True):
                st.info("Operación cancelada")
    else:
        st.info("📭 No hay reuniones para eliminar")

# ===============================================
# TAB 6: ENVIAR EMAIL
# ===============================================
with tab6:
    st.header("📧 Envío de Invitaciones por Email")
    add_email_section_to_dashboard(df_reuniones)

# ===============================================
# FOOTER
# ===============================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    📅 <strong>Gestor de Reuniones Inteligentes v3.0</strong> con CRUD Completo | 
    Desarrollado con ❤️ usando Streamlit | 
    © 2025 Todos los derechos reservados
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar adicional
with st.sidebar:
    st.markdown("---")
    st.markdown("### ℹ️ Información")
    st.caption(f"**Última actualización:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("**Versión:** 3.0 - CRUD Completo")
    
    with st.expander("❓ Ayuda"):
        st.markdown("""
        **Funcionalidades CRUD:**
        
        - 📋 **Ver:** Lista todas las reuniones
        - 🔍 **Buscar:** Encuentra reuniones específicas
        - ➕ **Crear:** Agenda nuevas reuniones
        - ✏️ **Actualizar:** Modifica reuniones existentes
        - 🗑️ **Eliminar:** Borra reuniones
        - 📧 **Email:** Envía invitaciones
        """)