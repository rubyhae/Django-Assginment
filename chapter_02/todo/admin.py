from django.contrib import admin

from todo.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'info','is_done','start_date','end_date')
    list_filter = ('is_done',)
    search_fields = ('title',)
    ordering = ('-start_date',)
    fieldsets = (
        ('Todo Info',{'fields' : ('title','info', 'is_done')}),
        ('Data Range',{'fields' : ('start_date', 'end_date')}),
    )