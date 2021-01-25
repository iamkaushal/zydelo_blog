from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User

PUBLISH_CHOICES = (
		('draft', 'Draft'),
		('publish', 'Publish'),
	)


class Post(models.Model):
	'''Model for blog posts'''

	id = models.BigAutoField(primary_key=True)
	author = models.ForeignKey(User,related_name='post', on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	image = models.ImageField(upload_to='post_images', blank=True)
	title = models.CharField(max_length=255, verbose_name='Blog Title')
	content = models.TextField(null=True, blank=True)
	publish = models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='publish')
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	likes = models.IntegerField(default=0)


	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'
		# unique_together = [('title', 'content')]

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
