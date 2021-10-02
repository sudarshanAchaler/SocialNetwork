from django import forms
from .models import Post, Profile, Comment
from django.core import validators

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:
        model=Post
        fields=['body', 'image']

        widgets={
            'body':forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }

class ProfileForm(forms.ModelForm):
    profilePicture_num=forms.IntegerField(validators=[validators.MaxValueValidator(10),validators.MinValueValidator(1)], widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model=Profile
        fields=['fullName', 'gender', 'birthDate', 'location', 'bio', 'profilePicture_num']

        widgets={
            'fullName':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'birthDate':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'profilePicture_num':forms.NumberInput(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']

        widgets={
            'comment': forms.Textarea(attrs={'class':'form-control', 'rows':'2', 'placeholder':'Post your reply'}),
        }
