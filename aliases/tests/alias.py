from django.test import TestCase
from django.core.urlresolvers import reverse

from aliases.models import Alias
from aliases.tests.base import create_alias

class AliasMethodTests(TestCase):

  def test_get_active_result(self):
    """
    get_active() should return only active aliases
    """
    alias1 = create_alias( 'll="ls -l"',active=False)
    alias2 = create_alias('lll="ls -l|less"')
    self.assertEqual(Alias.objects.get_active().count(), 1)
    self.assertEqual(Alias.objects.get_active()[0], alias2)

  def test_active_default_value(self):
    """
    The active field default value should be False.
    """
    alias = Alias.objects.create(
      content='ll="ls -l"',
      description='Extended output for ls',
    )
    self.assertFalse(alias.active)

class AliasViewTest(TestCase):
  def test_index_view_with_no_alias(self):
    """
    If no alias exist, an appropriate message should be displayed.
    """
    response = self.client.get(reverse('aliases:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No alias")
    self.assertQuerysetEqual(response.context['aliases'], [])

  def test_index_view_with_an_alias(self):
    """
    Valide alias should be displayed.
    """
    alias = create_alias("ll='ls -l'")

    response = self.client.get(reverse('aliases:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['aliases'], ["<Alias: ll='ls -l'>"])

  def test_index_view_with_an_inactive_alias(self):
    """
    Only valide alias should be displayed.
    """
    alias = create_alias("ll='ls -l'",active=False)

    response = self.client.get(reverse('aliases:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['aliases'], [])

  def test_show_view_without_alias(self):
    """
    No alias means 404
    """
    response = self.client.get(reverse('aliases:show', args=(123,)))
    self.assertEqual(response.status_code, 404)

  def test_show_view_on_inactive_alias(self):
    """
    Requesting an inactive alias means 404
    """
    alias = create_alias("ll='ls -l'", active=False)

    response = self.client.get(reverse('aliases:show', args=(alias.id,)))
    self.assertEqual(response.status_code, 404)
