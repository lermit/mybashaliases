from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages

from aliases.models import Alias
from aliases.forms import SubmitForm

def index(request):
  aliases = Alias.objects.get_active()
  context = { 'aliases': aliases }
  return render(request, 'aliases/index.html', context)

class DetailView(generic.DetailView):
  model=Alias
  template_name = 'aliases/show.html'

  def get_queryset(self):
    return Alias.objects.get_active()

def submit(request):
  """Submit a new bash aliases for validation
  """

  if request.method == 'POST':
    form = SubmitForm(request.POST)
    if form.is_valid():
      form.save()
      form = SubmitForm()
      messages.success(request, "Your alias as been submited. It'll be display as soon as a moderator validate him. Thank you !")
  else:
    form = SubmitForm()

  return render(request,
    'aliases/submit.html',
    { 'form': form })



