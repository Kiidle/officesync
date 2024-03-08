from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from administration.models import Log
from authentication.models import OfficeSync
from communication.models import Announcement, Message, Signature

User = get_user_model()


# Create your views here.
class AnnouncementsView(LoginRequiredMixin, generic.ListView):
    model = Announcement
    fields = ["title"]
    template_name = "pages/announcements/announcements.html"
    context_object_name = "announcements"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["unread_announcements"] = self.get_unread_announcements()
            context["read_announcements"] = self.get_read_announcements()
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )

        return context

    def get_unread_announcements(self):
        return self.model.objects.exclude(read_by=self.request.user)

    def get_read_announcements(self):
        return self.model.objects.filter(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class CreateAnnouncementsView(LoginRequiredMixin, generic.CreateView):
    model = Announcement
    fields = ["title", "content"]
    template_name = "pages/announcements/create.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.created_at = timezone.now()
        response = super().form_valid(form)

        Log.objects.create(
            user=self.request.user,
            action="CREATE",
            category="COMMUNICATION",
            content_object=self.object,
            message=f'@{self.request.user} hat eine Ankündigung "{self.object.title}" veröffentlicht.',
        )

        return response

    def get_success_url(self):
        return reverse_lazy("announcements")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
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
        return self.model.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class AnnouncementView(LoginRequiredMixin, generic.DetailView):
    model = Announcement
    fields = ["title"]
    template_name = "pages/announcements/announcement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["signature"] = Signature.objects.first()
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["show_read_button"] = not self.has_been_read_by(self.request.user)
        return context

    def has_been_read_by(self, user):
        announcement = self.get_object()
        return announcement.read_by.filter(id=user.id).exists()

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return Message.objects.filter(receiver=self.request.user, receiver_read=False)

    def post(self, request, *args, **kwargs):
        announcement = self.get_object()
        announcement.read_by.add(request.user)
        announcement.save()
        return redirect(reverse("announcement", kwargs={"pk": announcement.pk}))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class InboxView(LoginRequiredMixin, generic.ListView):
    model = Message
    fields = ["title"]
    template_name = "pages/inbox/inbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(
            receiver=self.request.user, receiver_read=False
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_message_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
        return context

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return self.get_queryset().filter(receiver_read=False)

    def get_read_messages(self):
        return self.get_queryset().filter(receiver_read=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class InboxMessageView(LoginRequiredMixin, generic.DetailView):
    model = Message
    fields = ["title"]
    template_name = "pages/inbox/message.html"

    def get_queryset(self):
        return Message.objects.filter(
            receiver=self.request.user, receiver_read=False
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["signature"] = Signature.objects.first()
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
        return context

    def post(self, request, *args, **kwargs):
        message = self.get_object()
        message.receiver_read = True
        message.save()
        return redirect(reverse("archive_message", kwargs={"pk": message.pk}))

    def get_unread_announcements(self):
        return Announcement.objects.exclude(read_by=self.request.user)

    def get_unread_messages(self):
        return self.get_queryset().filter(receiver_read=False)

    def get_read_messages(self):
        return self.get_queryset().filter(receiver_read=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

        return super().dispatch(request, *args, **kwargs)


class SelectUserView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/inbox/select.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = User.objects.all()

        search_query = self.request.GET.get("search", "")

        if search_query:
            search_terms = search_query.split()
            q_objects = Q()
            for term in search_terms:
                q_objects |= (
                    Q(first_name__icontains=term)
                    | Q(last_name__icontains=term)
                    | Q(username__icontains=term)
                )
            queryset = queryset.filter(q_objects)

        # Sortierung der Benutzer ähnlich wie in Beispiel 1
        queryset = queryset.annotate(
            role_name_order=Case(
                When(advanced__role__name__isnull=True, then=Value("ZZZZZZZZ")),
                default=F("advanced__role__name"),
                output_field=CharField(),
            )
        ).order_by(
            Lower("role_name_order"),
            Lower("first_name"),
            Lower("last_name"),
            Lower("username"),
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
            context["unread_announcements_count"] = (
                self.get_unread_announcements().count()
            )
            context["unread_messages_count"] = self.get_unread_messages().count()
            context["unread_count"] = (
                context["unread_announcements_count"] + context["unread_messages_count"]
            )
            context["search_query"] = self.request.GET.get("search", "")
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


class CreateMessageView(LoginRequiredMixin, generic.CreateView):
    model = Message
    fields = ["title", "content"]
    template_name = "pages/inbox/create.html"

    def form_valid(self, form):
        receiver_pk = self.kwargs.get("pk")
        receiver = get_object_or_404(User, pk=receiver_pk)

        form.instance.receiver = receiver

        form.instance.sender = self.request.user
        form.instance.created_at = timezone.now()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("inbox")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
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


class OutboxView(LoginRequiredMixin, generic.ListView):
    model = Message
    fields = ["title"]
    template_name = "pages/outbox/outbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
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


class OutboxMessageView(LoginRequiredMixin, generic.DetailView):
    model = Message
    fields = ["title"]
    template_name = "pages/outbox/message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["signature"] = Signature.objects.first()
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
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


class ArchiveView(LoginRequiredMixin, generic.ListView):
    model = Message
    fields = ["title"]
    template_name = "pages/archive/archive.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(
            receiver=self.request.user, receiver_read=True
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
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


class ArchiveMessageView(LoginRequiredMixin, generic.DetailView):
    model = Message
    fields = ["title"]
    template_name = "pages/archive/message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["signature"] = Signature.objects.first()
            context["unread_messages"] = self.get_unread_messages()
            context["read_messages"] = self.get_read_messages()
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
