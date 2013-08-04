from django.forms import ModelForm, Form

from aliases.models import Alias

class SubmitForm(ModelForm):
  class Meta:
    model = Alias
    fields = ('content', 'description')
