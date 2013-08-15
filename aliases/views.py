from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages

from aliases.models import Alias
from aliases.forms import SubmitForm, AliasRatingForm

class IndexView(generic.ListView):
  model = Alias
  template_name = 'aliases/index.html'

  def get_queryset(self):
    """Return a queryset of all active aliases with the related rating form.

    Rating form can be access with the rating_form attribute.
    """
    aliases = Alias.objects.get_active()
    for alias in aliases:
      rating_form = AliasRatingForm(alias=alias)
      alias.rating_form = rating_form
    return aliases

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
      alias = form.save(commit=False)
      alias.created_by = request.user
      alias.save()
      form = SubmitForm()
      messages.success(request, "Your alias as been submited. It'll be display as soon as a moderator validate him. Thank you !")
  else:
    form = SubmitForm()

  return render(request,
    'aliases/submit.html',
    { 'form': form })


def rate(request, pk):
  """Rate an alias
  """
  # Only post request are allow
  if not request.method == 'POST':
    return HttpResponseNotFound()

  # Get alias
  alias = get_object_or_404(Alias, pk=pk)

  # Validate Form
  rating_form = AliasRatingForm(alias, request.POST)
  if rating_form.is_valid():
    alias.rating.add(score=rating_form.cleaned_data['rate'], user=request.user, ip_address=request.META['REMOTE_ADDR'])
    messages.success(request, "Your rate has been save ! Thank you !")
  else:
    messages.error(request, "An error occured")
  return redirect('aliases:index')

