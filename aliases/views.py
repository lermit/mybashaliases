from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages

from aliases.models import Alias

def index(request):
  aliases = Alias.objects.get_active()
  context = { 'aliases': aliases }
  return render(request, 'aliases/index.html', context)

class DetailView(generic.DetailView):
  model=Alias
  template_name = 'aliases/show.html'

  def get_queryset(self):
    return Alias.objects.get_active()

def comment(request, alias_id):
  alias = get_object_or_404(Alias, pk=alias_id)
  try:
    comment_content = request.POST['content']
  except KeyError:
    return render(request, 'aliases/show.html', {
      'alias': alias,
      'error_message': 'Comment is empty',
    })
  else:
    alias.comment_set.create(content=comment_content)
    messages.info(request, "Thank you. Your comment is awaiting moderation.")
    return HttpResponseRedirect(reverse( 'aliases:show', args=(alias.id,)))
