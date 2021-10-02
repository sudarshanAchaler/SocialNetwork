from django.contrib import admin
from .models import Profile, Post, Comment

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','fullName','gender']
admin.site.register(Profile,ProfileAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display=['author', 'created_on', 'body']
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=['author', 'created_on']
admin.site.register(Comment, CommentAdmin)