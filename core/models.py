from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.utils import timezone
import uuid

# Create your models here.



class Profile(models.Model):
    GenderChoice = [('others', 'Others'),('male', 'Male'),('female' ,'Female')] 
    default_pic_mapping = { 1: 'avatar01.jpg', 2: 'avatar02.jpg', 3: 'avatar03.jpg', 4:'avatar04.jpg', 5:'avatar05.jpg', 6:'avatar06.jpg', 7:'avatar11.jpg', 8:'avatar12.jpg', 9:'avatar13.jpg', 10:'avatar14.jpg' }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=50, default="FirstName LastName")
    gender = models.CharField(max_length=10,choices=GenderChoice, default='male')
    birthDate = models.CharField(max_length=50, help_text="Enter Date in 1 January 2000 format.", default="3 July 2021")
    location = models.CharField(max_length=30, default="India")
    bio = models.TextField(max_length=500, default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum deserunt cum consectetur ratione quisquam accusamus ipsum, voluptates repellendus obcaecati? Minima?")
    profilePicture_num = models.IntegerField(default=1)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    verified = models.BooleanField(default=False)
    last_auth_token = models.CharField( max_length=100, blank=True, null=True)
    

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            temp=Profile.objects.create(user=instance)
            temp.followers.add(instance)
            temp.following.add(instance)
            temp.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_profile_pic_url(self):
        return static('images/avatars/{}'.format(self.default_pic_mapping[self.profilePicture_num]))

    def __str__(self):
        return self.user.username

    def get_auth_token(self):
        token=uuid.uuid4()
        self.last_auth_token=token
        self.save()
        return token
        

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='uploads/post_photos/',   blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.body

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)