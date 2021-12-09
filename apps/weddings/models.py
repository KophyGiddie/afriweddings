from django.db import models
from django.conf import settings
from utils import constants
import uuid


# Create your models here.
class Wedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='weddings',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='partner_wedding',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    partner_first_name = models.CharField(max_length=200, blank=True, null=True)
    partner_last_name = models.CharField(max_length=200, blank=True, null=True)
    schedule = models.CharField(max_length=200, blank=True, null=True)
    partner_email = models.CharField(max_length=200, blank=True, null=True)
    partner_role = models.CharField(max_length=200, blank=True, null=True)
    public_url = models.CharField(max_length=200, blank=True, null=True)
    partner_last_name = models.CharField(max_length=200, blank=True, null=True)
    budget = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    partner_picture = models.FileField(upload_to=constants.PROFILE_PIC_DIR, blank=True, null=True)
    couple_picture = models.FileField(upload_to=constants.PROFILE_PIC_DIR, blank=True, null=True)
    currency = models.CharField(blank=True, null=True, max_length=128, default="GHS")
    country = models.CharField(blank=True, null=True, max_length=128, default="Ghana")
    partner_accepted_invite = models.BooleanField(default=False)
    city = models.CharField(blank=True, null=True, max_length=128)
    venue = models.CharField(blank=True, max_length=1028, null=True)
    expected_guests = models.IntegerField(default=0)
    invited_guests = models.IntegerField(default=0)
    confirmed_guests = models.IntegerField(default=0)
    pending_guests = models.IntegerField(default=0)
    guests_cancelled = models.IntegerField(default=0)
    checklist_completed = models.IntegerField(default=0)
    total_checklist = models.IntegerField(default=0)
    wedding_date = models.DateField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    start_time = models.CharField(max_length=200, blank=True, null=True)
    end_time = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    hashtag = models.CharField(blank=True, max_length=1028, null=True)
    our_story = models.TextField(blank=True, max_length=9028, null=True)
    video_url = models.CharField(max_length=200, blank=True, null=True)
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='wedding_admins',
        blank=True
    )

    def get_partner_picture(self):
        if self.partner_picture:
            myimage = self.partner_picture.url
        else:
            myimage = ''
        return myimage

    def get_couple_picture(self):
        if self.couple_picture:
            myimage = self.couple_picture.url
        else:
            myimage = ''
        return myimage

    class Meta:
        verbose_name_plural = 'Weddings'
        ordering = ('wedding_date', )

    def __str__(self):
        return '%s - %s' % (self.partner_first_name, self.partner_role)


class WeddingMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='media',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='media',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to=constants.PROFILE_PIC_DIR,
                              blank=True,
                              null=True,
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wedding Media'
        ordering = ('-created_at',)

    def get_image(self):
        if self.image:
            myimage = self.image.url
        else:
            myimage = ''
        return myimage


class WeddingRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='roles',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_default = models.BooleanField(default=False)
    role = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_roles',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Wedding Roles'
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.role)


class WeddingTeam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    description = models.CharField(max_length=1000, blank=True, null=True)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='team',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    role = models.ForeignKey(
        WeddingRole,
        related_name='teams',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    picture = models.ImageField(upload_to=constants.PROFILE_PIC_DIR,
                                blank=True,
                                null=True,
                                )

    display_on_wedding_page = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class WallPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='wallpost',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='wallpost',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    post = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to=constants.WALLPOST_PIC_DIR,
                              blank=True,
                              null=True,
                              )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wall Post'
        ordering = ('-created_at',)

    def get_image(self):
        if self.image:
            myimage = self.image.url
        else:
            myimage = ''
        return myimage

    def __str__(self):
        return '%s' % (self.post)


class WeddingFAQ(models.Model):
    """
    Model for wedding page faqs

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='faqs',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question = models.CharField(max_length=2000, blank=True, null=True)
    answer = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='faqs',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % (self.question)

    class Meta:
        verbose_name_plural = 'FAQs'
        ordering = ('id',)


class WeddingScheduleEvent(models.Model):
    """
    Model for wedding page schedule events

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wedding = models.ForeignKey(
        Wedding,
        related_name='schedule_events',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=2000, blank=True, null=True)
    venue = models.CharField(max_length=2000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='schedule_events',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name_plural = 'Wedding Schedule Event'
        ordering = ('id',)


class WeddingSchedule(models.Model):
    """
    Model for wedding page schedule

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        WeddingScheduleEvent,
        related_name='wedding_schedule',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    time = models.CharField(max_length=2000, blank=True, null=True)
    activity = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='wedding_schedule',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % (self.activity)

    class Meta:
        verbose_name_plural = 'Wedding Schedule'
        ordering = ('id',)
