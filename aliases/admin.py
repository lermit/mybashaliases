from django.contrib import admin
from aliases.models import Alias

def make_active(modeladmin, request, queryset):
  queryset.update(active=True)
make_active.short_description = "Mark active selected item"

def make_unactive(modeladmin, request, queryset):
  queryset.update(active=False)
make_unactive.short_description = "Mark unactive selected item"

class AliasAdmin(admin.ModelAdmin):
  list_display = ('content', 'active', 'created_at', 'created_by')
  search_fields = ['content']
  list_filter = ('active','created_at', 'created_by')
  actions = [make_active, make_unactive]

  def save_model(self, request, obj, form, change):
    if obj.created_by_id == None:
      obj.created_by = request.user
    obj.save()

admin.site.register(Alias, AliasAdmin)
