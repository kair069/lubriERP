# LubriERP

LubriERP es un sistema ERP completo desarrollado con Django para la gestión integral de un **lubricentro**. Permite el control eficiente de ventas de aceites, repuestos, servicios, clientes, vehículos, pedidos, pagos y más.




## 🧩 Funcionalidades principales

- 🛒 Gestión de productos y stock (aceites, filtros, repuestos).
- 👤 Registro de clientes y vehículos asociados.
- 📦 Módulo de pedidos con historial y estados.
- 💳 Gestión de pagos y reportes contables.
- 📊 Dashboard interactivo (usando Django Plotly Dash).
- 🧾 Registro de logs y trazabilidad de acciones.
- 💬 Chatbot básico para atención al cliente.
- 🔐 Autenticación y roles de usuarios.
- 🌐 Compatible con despliegue en Render o servidor propio.

## 🛠️ Tecnologías usadas

- **Backend**: Django 5.1
- **Frontend**: HTML, CSS, JS (plantillas Django)
- **Base de datos**: MySQL
- **Otras libs**: Channels, Plotly Dash, Crispy Forms, CorsHeaders

## 📂 Estructura del proyecto

Proyecto1/
├── mi_app/
├── aplicacionLogs/
├── pedidos/
├── pagos/
├── vehiculos/
├── dashboardproductos/
├── chatbot1/
├── static/
├── media/
└── Proyecto1/ (configuración principal)


## ⚙️ Instalación


1. Clonar el repositorio:
git clone https://github.com/kair069/lubriERP.git

cpp
Copiar
Editar

2. Crear y activar un entorno virtual:
python -m venv env
source env/bin/activate # En Windows: env\Scripts\activate

markdown
Copiar
Editar

3. Instalar dependencias:
pip install -r requirements.txt

markdown
Copiar
Editar

4. Configurar la base de datos en `settings.py`

5. Aplicar migraciones:
python manage.py migrate

markdown
Copiar
Editar

6. Crear superusuario:
python manage.py createsuperuser

markdown
Copiar
Editar

7. Ejecutar el servidor:
python manage.py runserver

yaml
Copiar
Editar

## 🚀 Despliegue

Este proyecto está preparado para ser desplegado en plataformas como [Render](https://render.com), usando `asgi.py`, configuración de CORS, y `static/media`.

---

**Desarrollado por:** Jaret A.  
**Repositorio:** [https://github.com/kair069/lubriERP](https://github.com/kair069/lubriERP)
