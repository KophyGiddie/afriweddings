from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import constants
from rest_framework.authtoken.models import Token


class AFUserManager(BaseUserManager):
    """
    User Base manager for the user model

    """
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have a email')

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class AFUser(AbstractBaseUser):
    """
    Model for Users
    This model overrides the default django user model for enhanced customisation instead of using a one to one mapping

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=100,
    )
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.FileField('Profile Pic',
                                        upload_to=constants.PROFILE_PIC_DIR,
                                        blank=True,
                                        null=True,
                                        )
    user_type = models.CharField(max_length=100, default='COUPLE')
    user_role = models.CharField(max_length=1000, blank=True, null=True)
    activation_token = models.CharField(max_length=1000, blank=True, null=True)
    email_initiation_date = models.DateTimeField(blank=True, null=True)
    country = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=1000, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    has_onboarded = models.BooleanField(default=False)
    has_multiple_weddings = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_wedding_admin = models.BooleanField(default=True)
    is_social_user = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    social_media_avatar = models.URLField(max_length=500, blank=True, null=True)
    social_platform = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    temporal_login_fails = models.IntegerField(default=0)
    wedding_id = models.CharField(max_length=500, blank=True, null=True)
    permanent_login_fails = models.IntegerField(default=0)

    objects = AFUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return '''{} {}'''.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def get_avatar_full(self):
        if self.profile_picture:
            myimage = self.profile_picture.url
        elif self.social_media_avatar:
            myimage = self.social_media_avatar
        else:
            myimage = ''
        return myimage

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-created_at', 'first_name',)
        verbose_name = _('AfriWedding User')
        verbose_name_plural = _('AfriWedding User')

    def update_last_login(self):
        self.lastlogin = timezone.now()
        self.save()


@receiver(post_save, sender=AFUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Model for Users
    This model overrides the default django user model for enhanced customisation instead of using a one to one mapping

    """
    if created:
        Token.objects.create(user=instance)


class StoredPass(models.Model):
    """
    Model for storing hashed passwords used by users.
    This is used to prevent users from using their last five passwords for maximum security as a standard practice

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hashed = models.CharField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(AFUser, related_name='my_hashes', on_delete=models.CASCADE)


class FailedLogin(models.Model):
    """
    Model for guest groups

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(AFUser, related_name='failed_login_attempts', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class UserActivity(models.Model):
    """
    Model for saving all user activities

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.CharField(max_length=1000, blank=True, null=True)
    action = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(AFUser, related_name='user_activities', on_delete=models.CASCADE)
    device = models.CharField(max_length=1000, blank=True, null=True)
    ip_address = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ('-id', )

    def __str__(self):
        return self.description
