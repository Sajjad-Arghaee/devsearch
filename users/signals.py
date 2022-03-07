from django.db.models.signals import post_delete, post_save
from .models import User, Profile
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user = instance,
            username = instance.username,
            email = instance.email,
            name = instance.first_name
        )

        subject = 'Welcome to DevSearch Website'
        message = f'Glad to see you, {profile.name}'
        # send_mail(
        #     subject, 
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

# post_save.connect(createProfile, sender=User)
