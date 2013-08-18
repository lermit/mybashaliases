from random import sample

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

class ActivableManager(object):
  def get_active(self):
    return self.all().filter(active=True)

class RandomObjectManager(object):
  """
  Manager Mixin to implement get_random() in your models.
  You can override get_objects to tune the queriset

  To use, define your class:

  class MyManager(models.Manager, RandomObjectManager):
      DEFAULT_NUMBER = 5 # I can change that

      def get_objects(self):
          return self.filter(active=True) # Only active models plz

  class MyModel(models.Model):
      active = models.BooleanField()
      objects = MyManager()

  Now you can do:
  MyModel.objects.get_random()

  """

  DEFAULT_NUMBER = 3

  def get_objects(self):
    return self.all()

  def get_random(self, number=DEFAULT_NUMBER):
    """
    Returns a set of random objects
    """
    ids = self.get_objects().values_list('id', flat=True)
    amount = min(len(ids), number)
    picked_ids = sample(ids, amount)
    return self.filter(id__in=picked_ids)
  

class AliasManager(models.Manager, ActivableManager, RandomObjectManager):
  def get_objects(self):
    return self.get_active()

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
