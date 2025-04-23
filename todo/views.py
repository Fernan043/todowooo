# -*- coding: utf-8 -*-

from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError #preguntar porque
from django.contrib.auth import login, logout, authenticate
from .forms import DevolucionFormSet
from .forms import TodoForm, UbicacionForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from .forms import OrdenEntradaForm, DetalleOrdenFormSet
from .models import OrdenEntrada, Movimiento, Ubicacion
from .forms import MovimientoSalidaFormSet
from todo.models import Proveedor
import datetime
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
         return render(request, 'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        #Create a new user
        if request.POST['password1'] == request.POST['password2']:
           try:
            user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('currenttodos')
           except IntegrityError:
               return render(request, 'todo/signupuser.html',{'form':UserCreationForm(), 'error':'That username is currently in use'})
        else:
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm(), 'error':'Passwords did not match'})


def currenttodos(request):
    #esta linea declara que solo jale los todo de el usuario en especifico para que los que no correspondan a el no sea visibles
    todos= Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html',{'todos':todos})

@login_required
def logoutuser(request):
    #este post es basicamente porque sin el despues de un login el navegador nos hecharia ya que tiene precargada dicha accion o pagina
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def loginuser(request):
    if request.method == 'GET':
         return render(request, 'todo/loginuser.html',{'form':AuthenticationForm})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',{'form':AuthenticationForm,'error':'Username and password incorrect'})
        else:
            login(request, user)
            return redirect('currenttodos')
        
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            #la linea de abajo evita que se guarde en la base de datos sin antes una autorizacion el false es la clave como tal, sino se guardaria de manera automatica en BD
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',{'form':TodoForm(),'error':'Bad data pass in'})
        
@login_required
def viewtodo(request, todo_pk):
    todo= get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form,'error':'bad info'})


@login_required
def completetodo(request,todo_pk):
    todo= get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect('currenttodos')
   
@login_required
def deletetodo(request,todo_pk):
    todo= get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completetodos(request):
    #esta linea declara que solo jale los todo de el usuario en especifico para que los que no correspondan a el no sea visibles
    todos= Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')# esta es la difencia principal ya que antes en current estos estaba en true y este es false ya que el valor cambia una vez que se genera el complete
    return render(request, 'todo/completetodos.html',{'todos':todos})


@login_required
def crear_ubicacion(request):
    if request.method == 'GET':
        return render(request, 'todo/crearubicacion.html', {
            'form': UbicacionForm()
        })
    else:
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createtodo')      # Vuelve al formulario de crear TODO
        else:
            return render(request, 'todo/crearubicacion.html', {
                'form': form,
                'error': 'Datos invalidos al crear ubicacion.'
            })

@login_required
def crear_orden_entrada(request):
    if request.method == 'GET':
        form = OrdenEntradaForm()
        formset = DetalleOrdenFormSet()
        return render(request, 'todo/crear_ordenentrada.html', {
            'form': form,
            'formset': formset
        })

    # POST
    form = OrdenEntradaForm(request.POST)
    formset = DetalleOrdenFormSet(request.POST)
    if form.is_valid() and formset.is_valid():
        with transaction.atomic():
            orden = form.save()
            for detalle in formset.save(commit=False):
                detalle.orden = orden
                detalle.save()

                #  Registro de movimiento de entrada
                Movimiento.objects.create(
                    producto=detalle.producto,
                    tipo='entrada',
                    cantidad=detalle.cantidad
                )

                #  Asignación automática de ubicación si no tiene
                prod = detalle.producto
                if not prod.ubicacion:
                    bodega = Ubicacion.objects.annotate(
                        carga=Count('todo')
                    ).order_by('carga').first()
                    if bodega:
                        prod.ubicacion = bodega
                        prod.save()

        return redirect('currenttodos')

    # si hay errores
    return render(request, 'todo/crear_ordenentrada.html', {
        'form': form,
        'formset': formset
    })

@login_required
def crear_picking(request):
    """
    Crea un picking como una serie de movimientos tipo 'salida'.
    Luego calcula una 'ruta' ordenada por pasillo y estante.
    """
    if request.method == 'GET':
        formset = MovimientoSalidaFormSet(queryset=Movimiento.objects.none())
        return render(request, 'todo/crear_picking.html', {
            'formset': formset
        })

    # POST
    formset = MovimientoSalidaFormSet(request.POST)
    if formset.is_valid():
        movimientos_creados = []
        for form in formset:
            mov = form.save(commit=False)
            mov.tipo = 'salida'
            mov.save()
            movimientos_creados.append(mov)

        # Construimos la ruta: ordenar por pasillo y estante de la ubicación del producto
        ruta = sorted(
            movimientos_creados,
            key=lambda m: (
                m.producto.ubicacion.pasillo if m.producto.ubicacion else '',
                m.producto.ubicacion.estante if m.producto.ubicacion else ''
            )
        )

        return render(request, 'todo/picking_ruta.html', {
            'ruta': ruta
        })

    # Si hay errores, volvemos al form
    return render(request, 'todo/crear_picking.html', {
        'formset': formset
    })

def programar_despacho(request):
    if request.method == 'GET':
        mov_ids = request.GET.getlist('movimientos')
        if not mov_ids:
            # Si no vienen movimientos, volvemos a crear picking
            return redirect('crear_picking')

        ruta = Movimiento.objects.filter(pk__in=mov_ids)
        proveedores = Proveedor.objects.all()
        return render(request, 'todo/programar_despacho.html', {
            'ruta': ruta,
            'movimientos_ids': mov_ids,
            'proveedores': proveedores,
        })

    # POST: confirmación de despacho
    mov_ids = request.POST.getlist('movimientos')
    ruta = Movimiento.objects.filter(pk__in=mov_ids)
    proveedor = get_object_or_404(Proveedor, pk=request.POST['proveedor'])
    fecha = request.POST['fecha']
    hora  = request.POST['hora']

    return render(request, 'todo/despacho_confirmado.html', {
        'ruta': ruta,
        'proveedor': proveedor,
        'fecha': fecha,
        'hora': hora,
    })

@login_required
def crear_devolucion(request):
    if request.method == 'GET':
        formset = DevolucionFormSet()
        for form in formset:
            form.fields['producto'].queryset = Todo.objects.filter(user=request.user)
        return render(request, 'todo/crear_devolucion.html', {
            'formset': formset,
            'devoluciones': 'active',
        })

    formset = DevolucionFormSet(request.POST)
    for form in formset:
        form.fields['producto'].queryset = Todo.objects.filter(user=request.user)

    if formset.is_valid():
        movimientos = []
        for form in formset:
            prod   = form.cleaned_data['producto']
            qty    = form.cleaned_data['cantidad']
            defect = form.cleaned_data['defectuoso']

            if defect:
                # Registro como salida (sale del inventario)
                mov = Movimiento.objects.create(
                    producto=prod, tipo='salida', cantidad=qty
                )
                # reasignamos sólo la ubicación a "Inspección"
                insp, _ = Ubicacion.objects.get_or_create(
                    pasillo='XX', estante='XX',
                    defaults={'descripcion':'Area de inspeccion'}
                )
                prod.ubicacion = insp
                prod.save()
            else:
                # Registro como entrada (regresa al inventario)
                mov = Movimiento.objects.create(
                    producto=prod, tipo='entrada', cantidad=qty
                )
                

            movimientos.append(mov)

        return render(request, 'todo/devolucion_confirmada.html', {
            'movimientos': movimientos,
        })

    return render(request, 'todo/crear_devolucion.html', {
        'formset': formset,
        'devoluciones': 'active',
        'error': 'Corrige los errores en el formulario.'
    })

@login_required
def reporte_movimientos(request):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'todo/reporte_movimientos.html', {
        'movimientos': movimientos
    })

@login_required
def reporte_movimientos_pdf(request):
    # Genera un Response PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="movimientos.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    y = 750
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Reporte de Movimientos")
    y -= 30
    p.setFont("Helvetica", 10)
    for m in Movimiento.objects.all().order_by('fecha'):
        line = f"{m.fecha.strftime('%Y-%m-%d %H:%M')}  |  {m.get_tipo_display():7}  |  {m.producto.title:20}  |  {m.cantidad}"
        p.drawString(40, y, line)
        y -= 15
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    return response

@login_required
def reporte_productos(request):
    productos = Todo.objects.all().order_by('title')
    return render(request, 'todo/reporte_productos.html', {
        'productos': productos
    })

@login_required
def reporte_productos_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    y = 750
    p.setFont("Helvetica-Bold", 14)
    p.drawString(220, y, "Reporte de Productos")
    y -= 30
    p.setFont("Helvetica", 10)
    for prod in Todo.objects.all().order_by('title'):
        line = f"{prod.title:20}  |  Stock: {prod.stock:5}  |  Ubicacion: {prod.ubicacion or 'None'}"
        p.drawString(40, y, line)
        y -= 15
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    return response