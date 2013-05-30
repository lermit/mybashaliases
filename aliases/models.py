from django.db import models

### ABSTRACT ###
class Trackable(models.Model):
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  class Meta:
    abstract = True

class Activable(models.Model):
  active = models.BooleanField(default=False)

  class Meta:
    abstract = True

class ActivableManager(models.Manager):
  def get_active(self):
    return super(ActivableManager, self).get_query_set().filter(active=True)


### Manager  ###
class CommentManager(ActivableManager):
  pass

class AliasManager(ActivableManager):
  pass

### models ###
class Alias(Trackable, Activable):
  content = models.CharField(max_length=2500)
  description = models.CharField(max_length=2500, blank=True)
  objects = AliasManager()

  def __unicode__(self):
    return self.content
  def _get_active_comment_set(self):
    return self.comment_set.filter(active=True)

  active_comment_set = property(_get_active_comment_set)


class Comment(Trackable, Activable):
  content = models.CharField(max_length=2500)
  alias = models.ForeignKey(Alias)
  objects = CommentManager()

  def __unicode__(self):
    return self.content
