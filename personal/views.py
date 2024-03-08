from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from authentication.models import AdvancedUser, OfficeSync, Salary
from communication.models import Announcement, Message
from personal.models import Note

User = get_user_model()


# Create your views here.
class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AdvancedUser
    fields = [
        "biographie",
        "discord_username",
        "epicgames_username",
        "facebook_username",
        "instagram_username",
        "linkedin_username",
        "pinterest_username",
        "playstation_username",
        "reddit_username",
        "snapchat_username",
        "steam_username",
        "threads_username",
        "tiktok_username",
        "twitter_username",
        "xbox_username",
        "xing_username",
        "youtube_username",
    ]
    template_name = "pages/profile/profile_form.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class PersonalView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/personal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class MetaView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/personal/meta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class AdressView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/personal/adress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class HealthView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/personal/health.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class CriminalView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/personal/criminal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class WorkView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/work.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class SalaryView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/work/salary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def post(self, request, *args, **kwargs):
        salary_id = request.POST.get("salary_id")
        salary = get_object_or_404(Salary, id=salary_id)
        salary.confirmation = True
        salary.save()
        return redirect(reverse("salary"))

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class AbsenceView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/work/absence.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class PerformanceView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/work/performance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class ReprimantView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/profile/work/reprimant.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["unconfirmed_salaries_count"] = self.get_unconfirmed_salaries()
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def get_unconfirmed_salaries(self):
        return self.request.user.salaries.filter(confirmation=False).count()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class NotesView(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = "pages/notes/index.html"
    context_object_name = "notes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Note
    fields = ["title", "content", "color"]
    template_name = "pages/notes/update.html"

    def get_success_url(self):
        return reverse_lazy("notes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def get_read_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)
