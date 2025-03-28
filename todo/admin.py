from django.contrib import admin
from .models import Todo
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields= ('created',)


#esto hace que cuando ingresamos a admin se vea el objeto añadido en este caso "Todo"
admin.site.register(Todo,TodoAdmin)