from django.contrib import admin
from aliases.models import Alias

class AliasAdmin(admin.ModelAdmin):
  list_display = ('content', 'active', 'created_at')
  search_fields = ['content']
  list_filter = ('active','created_at')

admin.site.register(Alias, AliasAdmin)
