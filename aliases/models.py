from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from djangoratings.fields import RatingField

from aliases.validators import AliasValidator

ALIAS_RATING_RANGE = 5
alias_validator = AliasValidator()

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
  content = models.CharField(max_length=2500, validators=[alias_validator])
  description = models.CharField(max_length=2500, blank=True)
  rating = RatingField(range=ALIAS_RATING_RANGE, can_change_vote=True)
  created_by = models.ForeignKey(User, editable=False)
  objects = AliasManager()
  tags = TaggableManager()

  def __unicode__(self):
    return self.content
