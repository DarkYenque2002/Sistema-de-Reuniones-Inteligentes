#!/usr/bin/env python3
"""
Script de verificación completa del entorno
Gestor de Reuniones Inteligentes v3.0
"""
import sys
import os
from pathlib import Path

def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    print(f"   Versión instalada: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Versión compatible (Python 3.8+)")
        return True
    else:
        print("   ❌ Se requiere Python 3.8 o superior")
        return False

def check_pip():
    """Verifica que pip esté disponible"""
    print("\n📦 Verificando pip...")
    try:
        import pip
        print(f"   ✅ pip está instalado (versión {pip.__version__})")
        return True
    except ImportError:
        print("   ❌ pip no está instalado")
        return False

def check_required_packages():
    """Verifica las dependencias requeridas"""
    print("\n📚 Verificando paquetes requeridos...")
    
    packages = {
        'streamlit': 'Streamlit (Framework Web)',
        'pandas': 'Pandas (Manipulación de datos)',
        'dotenv': 'Python-dotenv (Variables de entorno)'
    }
    
    all_installed = True
    
    for package, description in packages.items():
        try:
            if package == 'dotenv':
                import dotenv
                version = dotenv.__version__
            else:
                module = __import__(package)
                version = module.__version__
            
            print(f"   ✅ {description}")
            print(f"      └─ Versión: {version}")
        except ImportError:
            print(f"   ❌ {description} - NO INSTALADO")
            all_installed = False
        except AttributeError:
            print(f"   ✅ {description} - INSTALADO")
    
    return all_installed

def check_builtin_modules():
    """Verifica módulos incluidos en Python"""
    print("\n🔧 Verificando módulos estándar de Python...")
    
    modules = [
        ('smtplib', 'SMTP (Envío de emails)'),
        ('email', 'Email MIME (Construcción de emails)'),
        ('datetime', 'Datetime (Manejo de fechas)'),
        ('os', 'OS (Sistema operativo)'),
        ('typing', 'Typing (Type hints)')
    ]
    
    all_ok = True
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description} - NO DISPONIBLE")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print("\n📁 Verificando estructura del proyecto...")
    
    files = {
        'app.py': 'Aplicación principal',
        'email_service.py': 'Servicio de emails',
        'test_email_connection.py': 'Script de prueba',
        'requirements.txt': 'Dependencias',
        '.env': 'Variables de entorno (OPCIONAL)'
    }
    
    all_present = True
    
    for filename, description in files.items():
        if Path(filename).exists():
            print(f"   ✅ {filename} - {description}")
        else:
            if filename == '.env':
                print(f"   ⚠️  {filename} - {description} (crear antes de usar)")
            else:
                print(f"   ❌ {filename} - {description} - NO ENCONTRADO")
                all_present = False
    
    return all_present

def check_env_file():
    """Verifica el contenido del archivo .env"""
    print("\n⚙️  Verificando configuración .env...")
    
    if not Path('.env').exists():
        print("   ⚠️  Archivo .env no encontrado")
        print("   📝 Debes crear un archivo .env con:")
        print("      EMAIL_USER=tu_email@gmail.com")
        print("      EMAIL_PASSWORD=tu_contraseña_de_aplicación")
        print("      SMTP_SERVER=smtp.gmail.com")
        print("      SMTP_PORT=587")
        return False
    
    print("   ✅ Archivo .env encontrado")
    
    # Intentar cargar variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['EMAIL_USER', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT']
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                if var == 'EMAIL_PASSWORD':
                    print(f"   ✅ {var}=****** (configurada)")
                else:
                    print(f"   ✅ {var}={value}")
            else:
                print(f"   ❌ {var} - NO CONFIGURADA")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"   ❌ Error al cargar .env: {str(e)}")
        return False

def show_installation_guide():
    """Muestra guía de instalación"""
    print("\n" + "=" * 70)
    print("  📖 GUÍA DE INSTALACIÓN")
    print("=" * 70)
    print("\n1️⃣  Instalar dependencias:")
    print("   pip install -r requirements.txt")
    print("\n2️⃣  Crear archivo .env:")
    print("   Crea un archivo llamado '.env' con:")
    print("   EMAIL_USER=tu_email@gmail.com")
    print("   EMAIL_PASSWORD=tu_contraseña_de_aplicación")
    print("   SMTP_SERVER=smtp.gmail.com")
    print("   SMTP_PORT=587")
    print("\n3️⃣  Obtener contraseña de aplicación de Gmail:")
    print("   a) Ve a: https://myaccount.google.com/security")
    print("   b) Activa 'Verificación en 2 pasos'")
    print("   c) Ve a: https://myaccount.google.com/apppasswords")
    print("   d) Genera contraseña para 'Correo'")
    print("   e) Copia la contraseña de 16 caracteres")
    print("\n4️⃣  Probar conexión:")
    print("   python test_email_connection.py")
    print("\n5️⃣  Ejecutar aplicación:")
    print("   streamlit run app.py")
    print("\n" + "=" * 70)

def run_all_checks():
    """Ejecuta todas las verificaciones"""
    print_header("🔍 VERIFICACIÓN COMPLETA DEL ENTORNO")
    print("Gestor de Reuniones Inteligentes v3.0\n")
    
    checks = []
    
    # Verificar Python
    checks.append(("Python", check_python_version()))
    
    # Verificar pip
    checks.append(("pip", check_pip()))
    
    # Verificar paquetes requeridos
    checks.append(("Paquetes requeridos", check_required_packages()))
    
    # Verificar módulos estándar
    checks.append(("Módulos estándar", check_builtin_modules()))
    
    # Verificar estructura del proyecto
    checks.append(("Estructura del proyecto", check_project_structure()))
    
    # Verificar .env
    checks.append(("Configuración .env", check_env_file()))
    
    # Resumen final
    print_header("📊 RESUMEN DE VERIFICACIÓN")
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ OK" if result else "❌ FALTA"
        print(f"   {status:12} - {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("\n🎉 ¡TODO ESTÁ LISTO!")
        print("\n✅ Tu entorno está correctamente configurado")
        print("\n🚀 Puedes ejecutar:")
        print("   • python test_email_connection.py (para probar email)")
        print("   • streamlit run app.py (para iniciar la aplicación)")
    else:
        print("\n⚠️  FALTAN ALGUNOS COMPONENTES")
        print("\n❌ Completa los pasos faltantes antes de continuar")
        show_installation_guide()
    
    print("\n" + "=" * 70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {str(e)}")
        sys.exit(1)