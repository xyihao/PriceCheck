from django.contrib import admin
from models import Sources
# Register your models here.

class SourceAdmin(admin.ModelAdmin):
	list_display=('name','site','url','qtype','period_type','period_num','last_update')
	ordering=('site','name',)

admin.site.register(Sources,SourceAdmin)
	
