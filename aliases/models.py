from django.db import models
from djangoratings.fields import RatingField

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

class AliasManager(ActivableManager):
  pass

### models ###
class Alias(Trackable, Activable):
  content = models.CharField(max_length=2500)
  description = models.CharField(max_length=2500, blank=True)
  rating = RatingField(range=5)
  objects = AliasManager()

  def __unicode__(self):
    return self.content
