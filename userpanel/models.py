from django.db import models
from django.contrib.auth import get_user_model


class Website(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    website_url = models.URLField()
    site_username = models.CharField(max_length=100)
    site_password = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website_url


class ReplacePhrase(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phrase = models.CharField(max_length=255)
    link = models.URLField()
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='website')

    def __str__(self):
        return self.user


class ContentWebsite(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='content_website')
    title = models.CharField(max_length=500, blank=False, null=False)
    content = models.TextField()
    post_id = models.IntegerField(blank=False, null=False)
    category = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    slug = models.CharField(blank=True, null=True, max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


