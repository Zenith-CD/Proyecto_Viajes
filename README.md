                                                                                                           Ruta Austral Viajes
  
Blog de viajes hechos con Django
tiene una API REST (la parte de atrás) y un frontend simple en HTML + Bootstrap que le habla a esa API con fetch(nada de formularios de Django, todo va por JSON/FormData).

--> La idea: que cualquiera pueda leer los viajes, pero solo quien inicie sesion pueda crear, editar o borrar <--

ocupa
Python + Django
Marco REST de Django (la API)
SimpleJWT (tokens de inicio de sesión)
MySQL (base viajes_db)
Pillow (para las fotos)
Bootstrap 5 por CDN (no hay que instalar nada para eso)

Los modelos (3 en total)
Persona --> rut (unico, formato 12345678-9sin puntos) nombre, apellido, email (unico), fecha de nacimiento y foto opcional <--
Lugar --> nombre, pais, ciudad, descripción y foto opcional <--
Viaje --> une una persona con un lugar (FK a los dos) + fecha de visita, título, relato, foto opcional y calificacion de 1 a 5 <--

Si borras una persona o un lugar se borran también sus viajes ( CASCADE), ojo con eso.


Validaciones que ya trae
El RUT se revisa con una expresión regular (7 u 8 dígitos, guion y dígito verificador o K)
La fecha de nacimiento y la fecha de visita no pueden ser futuras
La calificación solo acepta del 1 al 5
Para correrlo
Clona o descomprime el proyecto y entra a la carpeta (donde está manage.py).
Crea un entorno virtual e instala lo necesario:
intento
python -m venv venv
venv\Scripts\activate 
pip install django djangorestframework djangorestframework-simplejwt mysqlclient pillow
Crea la base de datos en MySQL:
SQL
CREATE DATABASE viajes_db CHARACTER SET utf8mb4;
Revisa en Proyecto_Viajes/settings.pyel bloque DATABASESy deja tu usuario y clave de MySQL (<---- ahí mismo está el host 127.0.0.1 y el puerto 3306, cámbialos si lo tuyo es distinto).
Migraciones y usuario admin:
intento
python manage.py makemigrations api FrontEnd
python manage.py migrate
python manage.py createsuperuser
Levantar el servidor:
intento
python manage.py runserver

Y listo, entras a http://127.0.0.1:8000/.

Páginas del frontend
Ruta	Qué hace
/	Blog con todos los viajes (se puede filtrar por lugar y por persona)
/viaje/<id>/	Detalle de un viaje
/viajes/nuevo/y/viajes/<id>/editar/	Formulario de viaje (pide iniciar sesión)
/personas/,/personas/nueva/	Lista y formulario de personas
/lugares/,/lugares/nuevo/	Lista y formulario de lugares
/login/	Inicio de sesión
/admin/	Panel de Django
La API

Todo cuelga de /api/(hay van personas/, lugares/y viajes/, con el CRUD completo en cada uno).

GET /api/viajes/?lugar=1&persona=2--> filtra por id (si mandas algo que no es numero, simplemente lo ignora) <--
POST /api/token/recibe usernamey password, devuelve access yrefresh
POST /api/token/refresh/renueva el acceso con el refresco
Cómo funciona la seguridad

Leer (GET) es libre, no pide nada
Escribir (POST, PUT, PATCH, DELETE) pide el encabezadoAuthorization: Bearer <access>
El acceso dura 30 minutos y el refresco 1 día.
El api.jsguarda los tokens en localStoragey, si el acceso se vence, intenta renovarlo solo; si no se puede, te manda de vuelta a/login/

Los viajes salen con persona_detalley lugar_detalle(un resumen legible) además de los ids, para que el frontend no tenga que hacer más peticiones.

Cosas a tener en cuenta
DEBUG = Truey la SECRET_KEYestán en el settings tal cual, sirve para desarrollo pero no para subirlo a produccion
Las fotos se guardan en la carpeta media/(se crea sola al subir la primera)
