from django.forms import ModelForm
from .models import Todo


# esto basicamente funciona para crear un tipo de formulario
#jalando la informacion de un obejeto presente en base de datos
# se debe importar en este caso es Todo
# para despues ser llamado en views.py para su uso y funcionalidad
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields =['title','memo','important']
    
