from django import forms

from aliases.models import Alias, ALIAS_RATING_RANGE

class SubmitForm(forms.ModelForm):
  class Meta:
    model = Alias
    fields = ('content', 'description')
    labels = {
      'content': 'Alias',
    }
    help_texts = {
      'content': "First part of a valid alias must be any character execpt the equal sign (=) or space ( ) directly follow by an equal sign (=). Second part should be the command. If command contain space it must be single or double quote surrounded.",
    }

class AliasRatingForm(forms.Form):

  def __init__(self, alias, *args, **kwargs):
    super(AliasRatingForm, self).__init__(*args, **kwargs)
    self.prefix = alias.id

  rate  = forms.ChoiceField(
            choices=((str(x), x) for x in range(1,ALIAS_RATING_RANGE+1)),
            widget=forms.RadioSelect)

