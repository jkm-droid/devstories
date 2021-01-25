from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Story
from .models import UserProfile, Comments


class WriteStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'image', 'body', 'tags', 'draft']

    def __init__(self, *args, **kwargs):
        super(WriteStoryForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'Write your story title'
        self.fields['title'].widget.attrs['class'] = 'form-control display-1'
        self.fields['title'].widget.attrs['rows'] = 2
        self.fields['title'].widget.attrs['columns'] = 15

        self.fields['body'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['placeholder'] = 'Write your story'
        self.fields['body'].widget.attrs['rows'] = 12
        self.fields['body'].widget.attrs['columns'] = 15

        self.fields['image'].widget.attrs['class'] = 'form-control'

        self.fields['tags'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].help_text = '<small>A comma-separated list of tags.</.small>'


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = '<small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ ' \
                                            'only.</small> '


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['status', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].help_text = '<small>Select one of the status. You can always change it in future</small>'

        self.fields['image'].widget.attrs['class'] = 'form-control'

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Write a short description about yourself'
        self.fields['description'].widget.attrs['rows'] = 4
        self.fields['description'].widget.attrs['columns'] = 15


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']
        exclude = ['username']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        # self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['username'].widget.attrs['placeholder'] = 'Write your name'

        self.fields['body'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['placeholder'] = 'Write your comment'
        self.fields['body'].widget.attrs['rows'] = 4
        self.fields['body'].widget.attrs['columns'] = 15


class ChangePassword(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter old password'

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter new password'
        self.fields['new_password1'].help_text = ''

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Enter new password again'
