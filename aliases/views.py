from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from haystack.forms import SearchForm

from taggit.models import Tag, TaggedItem

from aliases.models import Alias
from aliases.forms import SubmitForm, AliasRatingForm

class GenericBaseViewMixin(object):
  search_form = SearchForm()

  def get_search_form(self, **kwargs):
    """Add the search form to view
    """
    return self.search_form

class IndexView(generic.ListView):
  model = Alias
  template_name = 'aliases/index.html'

class AllView(generic.ListView, GenericBaseViewMixin):
  """Display all aliases
  """
  model = Alias
  template_name = 'aliases/index.html'
  queryset = Alias.objects.get_active()
  paginate_by = 10

  def get_context_data(self, **kwargs):
    """Append a 'rating_form' attribute in each Alias
    """
    context = super(AllView, self).get_context_data(**kwargs)
    context.update( {'search_form': self.get_search_form()} )
    for alias in context['object_list']:
      alias.rating_form = AliasRatingForm(alias=alias)
    return context

class TaggedView(AllView):
  """Display aliases with specified tag
  """
  def get_queryset(self):
    """Retreive aliases with specified tag
    """
    tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
    queryset = super(TaggedView, self).get_queryset()
    queryset = queryset.filter(
      pk__in=TaggedItem.objects.filter(
        tag=tag,
        content_type=ContentType.objects.get_for_model(self.model))
      .values_list("object_id", flat=True))
    return queryset

class RandomView(AllView):
  """Display a set of random aliases
  """

  def get_queryset(self):
    """Return 3 random aliases
    """
    return Alias.objects.get_random()

class TopView(AllView):
  """Display top rated aliases
  """

  def get_queryset(self):
    """Retreive top 10 ratted aliases
    """
    queryset = super(AllView, self).get_queryset()
    return queryset.extra(select={
      'score': '((100/%s*rating_score/(rating_votes+%s))+100)/2' % (
        Alias.rating.range,
        Alias.rating.weight)}).order_by('-score')[:10]

class DetailView(generic.DetailView):
  model=Alias
  slug_field = 'slug'
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

from haystack.views import SearchView
class AliasSearchView(SearchView):
  def extra_context(self):
    return { 'object_list': self.results }

