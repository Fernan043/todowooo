from django.forms import ModelForm
from django.forms.models import inlineformset_factory 
from .models import Todo,Ubicacion
from .models import OrdenEntrada, DetalleOrdenEntrada


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