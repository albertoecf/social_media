from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import misaka

from groups.models import  Group

from django.contrib.auth import get_user_model
User = get_user_model()


 class Post(models.Model):
     user = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
     created_at = models.DataTime(auto_now=True)
     message = models.TextField()
     message_html = models.TextField(editable=False)
     group = models.ForeignKey(Group, related_name='posts',null=True,blank=True, on_delete=models.CASCADE)

     def __str__(self):
         return self.message

     def save(self, *args, **kwargs):
         self.message_html = misaka.html(self.message)
         super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
        "app_posts:single",
        kwargs={
            'username'= self.user.username,
            "pk" = self.pk
        }
        )
    class Meta:
        ordering = ["name"]
        unique_together = ["user", "message"]