from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from administration.models import Log
from communication.models import Announcement, Message

from .forms import LoginForm, SignUpForm
from .models import AdvancedUser, OfficeSync, UserCustomInterface

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "pages/authentication/signup.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        AdvancedUser.objects.create(user=self.object)
        UserCustomInterface.objects.create(user=self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        return context


def sign_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()

        office_sync = OfficeSync.objects.first()
        context = {
            "form": form,
            "officesync": office_sync,
        }

        return render(request, "pages/authentication/login.html", context)

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Erfolgreich angemeldet!")
                return redirect("home")

        office_sync = OfficeSync.objects.first()
        context = {
            "form": form,
            "officesync": office_sync,
        }

        messages.error(request, f"Benutzername oder Passwort ist falsch.")
        return render(request, "pages/authentication/login.html", context)


@login_required
def custom_logout(request):
    logout(request)
    return redirect("home")


class HomeView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/root/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "officesync"
        ] = OfficeSync.objects.first()  # Hole das erste OfficeSync-Objekt
        context["unread_announcements_count"] = self.get_unread_announcements().count()
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


class PrivacyView(generic.ListView):
    model = User
    template_name = "pages/laws/privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "officesync"
        ] = OfficeSync.objects.first()  # Hole das erste OfficeSync-Objekt
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.advanced.privacy = True
            request.user.advanced.save()

        Log.objects.create(
            user=request.user,
            action="READ",
            message=f"@{request.user} hat die Datenschutzerklärung zugestimmt.",
        )

        if request.user.advanced.terms:
            if request.user.advanced.copyright:
                return redirect("home")
            return redirect("copyright")
        if request.user.advanced.copyright:
            return redirect("home")
        return redirect("terms")


class TermsView(generic.ListView):
    model = User
    template_name = "pages/laws/terms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "officesync"
        ] = OfficeSync.objects.first()  # Hole das erste OfficeSync-Objekt
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.advanced.terms = True
            request.user.advanced.save()

        Log.objects.create(
            user=request.user,
            action="READ",
            message=f"@{request.user} hat die Nutzungsbedingungen zugestimmt.",
        )

        if request.user.advanced.copyright:
            return redirect("home")
        return redirect("copyright")


class CopyrightView(generic.ListView):
    model = User
    template_name = "pages/laws/copyright.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "officesync"
        ] = OfficeSync.objects.first()  # Hole das erste OfficeSync-Objekt
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.advanced.copyright = True
            request.user.advanced.save()

        Log.objects.create(
            user=request.user,
            action="READ",
            message=f"@{request.user} hat die Urheberrechtsreglement zugestimmt.",
        )

        return redirect("home")
