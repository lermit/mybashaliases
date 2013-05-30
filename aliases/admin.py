from django.contrib import admin
from aliases.models import Alias, Comment

class CommentInline(admin.TabularInline):
  model = Comment
  extra = 0

class AliasAdmin(admin.ModelAdmin):
  inlines = [CommentInline]
  list_display = ('content', 'active', 'created_at')
  search_fields = ['content']
  list_filter = ('active','created_at')

admin.site.register(Alias, AliasAdmin)
