from django.forms import ModelForm
from django.forms.models import inlineformset_factory 
from django.forms import modelformset_factory
from .models import Todo,Ubicacion
from .models import OrdenEntrada, DetalleOrdenEntrada
from .models import Movimiento

# esto basicamente funciona para crear un tipo de formulario
#jalando la informacion de un obejeto presente en base de datos
# se debe importar en este caso es Todo
# para despues ser llamado en views.py para su uso y funcionalidad
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields =['title','memo','important','ubicacion']
    
class UbicacionForm(ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['pasillo', 'estante', 'descripcion']

class OrdenEntradaForm(ModelForm):
    class Meta:
        model = OrdenEntrada
        fields = ['proveedor', 'descripcion']

DetalleOrdenFormSet = inlineformset_factory(
    OrdenEntrada,
    DetalleOrdenEntrada,
    fields=['producto', 'cantidad'],
    extra=1,
    can_delete=False
)

class MovimientoSalidaForm(ModelForm):
    class Meta:
        model  = Movimiento
        fields = ['producto', 'cantidad']
        # No se  incluye 'tipo' ni 'fecha' ya que  tipo lo fijaremos a 'salida' en la vista

MovimientoSalidaFormSet = modelformset_factory(
    Movimiento,
    form=MovimientoSalidaForm,
    extra=1,
    can_delete=False
)