from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Message, Profile, Skill
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'fisrt_name': 'Name'
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )

class CustomProfileCreationForm(ModelForm):
    class Meta:
        model = Profile 
        fields = ['name', 'email', 'profile_image', 'username', 'short_intro',
                'bio', 'social_github', 'social_twitter', 'social_linkedin', 'social_website'
                ]

    def __init__(self, *args, **kwargs):
        super(CustomProfileCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )


class SkillForm(ModelForm):
    class Meta:
        model = Skill 
        fields = '__all__'
        exclude = ['owner']
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )


class MessageForm(ModelForm):
    class Meta:
        model = Message 
        fields = '__all__'
        exclude = ['sender', 'recipient']
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )