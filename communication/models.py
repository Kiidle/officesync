from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.


class Signature(models.Model):
    show_name = models.BooleanField(default=True, verbose_name=_("Name anzeigen"))
    show_role = models.BooleanField(default=True, verbose_name=_("Rollen anzeigen"))
    corporation = models.CharField(
        max_length=50, default=_("OfficeSync"), verbose_name=_("Unternehmen")
    )
    show_corporation = models.BooleanField(
        default=True, verbose_name=_("Unternehmen anzeigen")
    )
    logo = models.ImageField(
        upload_to="authentication/static/images/uploads/signature",
        null=True,
        blank=True,
        default="authentication/static/images/uploads/logo_default/officesync.png",
        verbose_name=_("Logo"),
    )
    show_logo = models.BooleanField(default=True, verbose_name=_("Logo anzeigen"))
    country = models.CharField(
        max_length=50, default=_("Schweiz"), verbose_name=_("Land")
    )
    show_country = models.BooleanField(default=True, verbose_name=_("Land anzeigen"))
    location = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Ort")
    )
    show_location = models.BooleanField(default=True, verbose_name=_("Ort anzeigen"))
    zip = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("PLZ"))
    show_zip = models.BooleanField(default=True, verbose_name=_("PLZ anzeigen"))
    street = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Strasse")
    )
    show_street = models.BooleanField(default=True, verbose_name=_("Strasse anzeigen"))
    housenumber = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Hausnummer")
    )
    show_housenumber = models.BooleanField(
        default=True, verbose_name=_("Hausnummer anzeigen")
    )
    url = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Webseite")
    )
    show_url = models.BooleanField(default=True, verbose_name=_("Webseite anzeigen"))

    def get_logo_url(self):
        if self.logo and hasattr(self.logo, "url"):
            return self.logo.url.replace("/authentication/", "/")
        else:
            return "/static/images/uploads/logo_default/officesync.png"


class Message(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="received_messages"
    )

    def __str__(self):
        return (
            f"Sender: {self.sender} | Empfänger: {self.receiver} | Titel: {self.title}"
        )


class Announcement(models.Model):
    title = models.CharField(max_length=40, verbose_name=_("Title"))
    content = models.TextField(max_length=3000, verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_announcement"
    )
    read_by = models.ManyToManyField(
        User, related_name="read_announcements", blank=True
    )

    def formatted_created_at(self):
        now = timezone.now()
        delta = now - self.created_at

        seconds = delta.total_seconds()
        minutes = int(seconds // 60)
        hours = int(minutes // 60)
        days = delta.days

        if seconds < 60:
            return _("Vor {seconds} Sekunden").format(seconds=int(seconds))
        elif minutes == 1:
            return _("Vor 1 Minute")
        elif 2 <= minutes < 60:
            return _("Vor {minutes} Minuten").format(minutes=minutes)
        elif hours == 1:
            return _("Vor 1 Stunde")
        elif 2 <= hours < 24:
            return _("Vor {hours} Stunden").format(hours=hours)
        elif days == 1:
            return _("Gestern um {time} Uhr").format(
                time=self.created_at.strftime("%H:%M")
            )
        elif 2 <= days < 7:
            return _("Vor {days} Tagen um {time} Uhr").format(
                days=days, time=self.created_at.strftime("%H:%M")
            )
        elif days == 7:
            return _("Vor 1 Woche um {time} Uhr").format(
                time=self.created_at.strftime("%H:%M")
            )
        else:
            return self.created_at.strftime("%d.%m.%Y %H:%M Uhr")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Sender: {self.sender} | Titel: {self.title}"


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    content = models.TextField(max_length=500, verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="received_messages"
    )
    receiver_read = models.BooleanField(default=False)

    def formatted_created_at(self):
        now = timezone.now()
        delta = now - self.created_at

        seconds = delta.total_seconds()
        minutes = int(seconds // 60)
        hours = int(minutes // 60)
        days = delta.days

        if seconds < 60:
            return _("Vor {seconds} Sekunden").format(seconds=int(seconds))
        elif minutes == 1:
            return _("Vor 1 Minute")
        elif 2 <= minutes < 60:
            return _("Vor {minutes} Minuten").format(minutes=minutes)
        elif hours == 1:
            return _("Vor 1 Stunde")
        elif 2 <= hours < 24:
            return _("Vor {hours} Stunden").format(hours=hours)
        elif days == 1:
            return _("Gestern um {time} Uhr").format(
                time=self.created_at.strftime("%H:%M")
            )
        elif 2 <= days < 7:
            return _("Vor {days} Tagen um {time} Uhr").format(
                days=days, time=self.created_at.strftime("%H:%M")
            )
        elif days == 7:
            return _("Vor 1 Woche um {time} Uhr").format(
                time=self.created_at.strftime("%H:%M")
            )
        else:
            return self.created_at.strftime("%d.%m.%Y %H:%M Uhr")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Sender: {self.sender} | Empfänger: {self.receiver} | Gelesen: {self.receiver_read} | Titel: {self.title}"
