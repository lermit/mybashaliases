from django.contrib import admin
from aliases.models import Alias

class AliasAdmin(admin.ModelAdmin):
  list_display = ('content', 'active', 'created_at', 'created_by')
  search_fields = ['content']
  list_filter = ('active','created_at', 'created_by')

  def save_model(self, request, obj, form, change):
    if obj.created_by_id == None:
      obj.created_by = request.user
    obj.save()

admin.site.register(Alias, AliasAdmin)
