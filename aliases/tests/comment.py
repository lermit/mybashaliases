from django.test import TestCase
from django.core.urlresolvers import reverse

from aliases.models import Alias, Comment
from aliases.tests.base import create_alias, Messages

class CommentTest(TestCase, Messages):
  def test_show_view_with_no_comment(self):
    """
    Requesting an alias with no comment
    """
    alias = create_alias("ll='ls -l'")

    response = self.client.get(reverse('aliases:show', args=(alias.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No comment")

  def test_show_view_with_comment(self):
    """
    Requesting an alias with comment
    """
    alias = create_alias("ll='ls -l'", comments=[{"content":"My funny comment"}])

    response = self.client.get(reverse('aliases:show', args=(alias.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "My funny comment")

  def test_show_post_comment(self):
    """
    Try to post a comment
    """
    alias = create_alias("ll='ls -l'")

    response = self.client.post(reverse('aliases:comment', args=(alias.id,)), { 'content': 'This is my comment' })
    self.assertRedirects(response, reverse('aliases:show', args=(alias.id,)))
    response = self.client.get(reverse('aliases:show', args=(alias.id,)))
    with self.messages_request() as request:
      self.assertMessageCount(request, 1)
      self.assertMessageInRequest(request, "Thank you. Your comment is awaiting moderation.")
    self.assertContains(response, "No comment")

  def test_show_post_comment_with_validation(self):
    """
    Try to post a comment. After validation it should be display
    """
    # First. Post a comment
    alias = create_alias("ll='ls -l'")
    response = self.client.post(reverse('aliases:comment', args=(alias.id,)), { 'content': 'This is my comment' }, follow=True)
    # Second. Active the comment
    comment = alias.comment_set.all()[0]
    comment.active = True
    comment.save()
    # Third. Test :)
    self.assertContains(response, "This is my comment")
