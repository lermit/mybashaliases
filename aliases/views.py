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

class SubmitView(generic.FormView):
  """Submit a new bash aliases for validation
  """
  form_class = SubmitForm
  template_name = 'aliases/submit.html'

  def get_success_url(self):
    return reverse("aliases:submit")

  def form_valid(self, form):
    """Save the new aliases.
    """
    alias = form.save(commit=False)
    alias.created_by = self.request.user
    alias.save()
    messages.success(
      self.request,
      "Your alias as been submited. It'll be display as soon as a moderator validate him. Thank you !")
    return super(SubmitView, self).form_valid(form)

class RateView(generic.View):
  form_class = AliasRatingForm

  def get(self, request, *args, **kwargs):
    return HttpResponseNotFound()

  def post(self, request, pk, *args, **kwargs):
    alias = get_object_or_404(Alias, pk=pk)
    rating_form = AliasRatingForm(alias, request.POST)
    if rating_form.is_valid():
      alias.rating.add(
        score=rating_form.cleaned_data['rate'],
        user=request.user,
        ip_address=request.META['REMOTE_ADDR'])
      messages.success(request,
        "Your rate has been save ! Thank you !")
    else:
      messages.error(request,
        "An error occured")
    return redirect('aliases:index')
