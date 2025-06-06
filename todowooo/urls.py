"""
todowooo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
     #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    #Todos y rutas para colaboradores
    path('current/', views.currenttodos, name='currenttodos'),
    path('completed/', views.completetodos, name='completetodos'),
    path('', views.home, name='home'),
    path('create/', views.createtodo, name='createtodo'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
    path('ubicacion/create/', views.crear_ubicacion, name='crear_ubicacion'),
    path('ordenentrada/create/', views.crear_orden_entrada, name='crear_orden_entrada'),
    path('picking/create/', views.crear_picking, name='crear_picking'),
     path('picking/despacho/',  views.programar_despacho, name='programar_despacho'),
     path('devoluciones/create/', views.crear_devolucion, name='crear_devolucion'),
      path('reportes/movimientos/', views.reporte_movimientos,    name='reporte_movimientos'),
    path('reportes/movimientos/pdf/', views.reporte_movimientos_pdf, name='reporte_movimientos_pdf'),
    path('reportes/productos/',   views.reporte_productos,      name='reporte_productos'),
    path('reportes/productos/pdf/',   views.reporte_productos_pdf,    name='reporte_productos_pdf'),
]

