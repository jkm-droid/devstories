from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    STATUS = [
        ("BEGINNER", "Beginner"),
        ("INTERMEDIATE", "Intermediate"),
        ("PRO", "Pro"),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default="BEGINNER" )
    is_online = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField(blank=False, default="An interesting participator in Developer Stories")
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    is_profile = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "User Profiles"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def image_tag(self):
        if self.image:
            return format_html('<img style="width:30px; height:30px;" src="{}" />'.format(self.image.url))
        else:
            return 'No Image'

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


"""
    the story model
"""


class Story(models.Model):
    title = models.TextField(blank=False, null=False)
    slug = models.SlugField(unique=False, max_length=250)
    image = models.ImageField(upload_to='images/', blank=True)
    body = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    likes = models.IntegerField(default=0)
    smiles = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    is_saved = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True, auto_now=False)
    modified_on = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Stories'
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/portal/{self.slug}"

    def get_edit_absolute_url(self):
        return f"/portal/{self.id}/edit"

    def get_delete_absolute_url(self):
        return f"/portal/delete/{self.slug}"

    def save(self, *args, **kwargs):
        # take the stories title and
        # convert it to slug
        new_title = f"{self.title}{self.pk}"
        self.slug = slugify(new_title)

        super(Story, self).save(*args, **kwargs)

    def save_image(self, *args, **kwargs):
        # resize the story cover image before saving
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            recommended_size = (300, 300)
            img.resize(recommended_size)
            img.save(self.image.path)

    def image_tag(self):
        if self.image:
            return format_html('<img style="width:30px; height:30px;" src="{}" />'.format(self.image.url))
        else:
            return 'No Image'

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


"""
    the notification model to save a notifification every 
    time a new story is created
"""


class StoryNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="notification")


class SaveForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.story) + ':' + str(self.value)

    class Meta:
        unique_together = ('user', 'story', 'value')


class Smile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.story) + ':' + str(self.value)

    class Meta:
        unique_together = ('user', 'story', 'value')


class StoryViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.story) + ':' + str(self.value)

    class Meta:
        unique_together = ('user', 'story', 'value')


class Comments(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-created_on']
