from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from authentication.models import AdvancedUser, OfficeSync
from communication.models import Announcement, Message

from .models import CustomPermission, Log, Role

User = get_user_model()


class SystemView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/system.html"

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logo_config_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.config.logo"
        ).exists()

    def has_app_config_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.config.app"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = (
            OfficeSync.objects.first()
        )  # Hole das erste OfficeSync-Objekt
        if self.request.user.is_authenticated:
            context["has_logo_config_permission"] = self.has_logo_config_permission(
                self.request.user
            )
            context["has_app_config_permission"] = self.has_app_config_permission(
                self.request.user
            )
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class AppNameUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = OfficeSync
    fields = ["app"]
    template_name = "pages/form_app.html"

    def get_success_url(self):
        return reverse_lazy("system")

    def form_valid(self, form):
        Log.objects.create(
            user=self.request.user,
            action="UPDATE",
            category="ADMINISTRATION",
            message=f"{self.request.user} nannte die Webanwendung um ({self.object.app}).",
        )

        return super().form_valid(form)

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_app_config_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.config.app"
        ).exists()

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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_app_config_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class AppLogoUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = OfficeSync
    fields = ["logo"]
    template_name = "pages/form_app.html"

    def get_success_url(self):
        return reverse_lazy("system")

    def form_valid(self, form):
        Log.objects.create(
            user=self.request.user,
            action="UPDATE",
            category="ADMINISTRATION",
            message=f"{self.request.user} änderte das Logo der Webanwendung.",
        )

        return super().form_valid(form)

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logo_config_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.config.logo"
        ).exists()

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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logo_config_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RolesView(LoginRequiredMixin, generic.ListView):
    model = Role
    fields = ["name"]
    template_name = "pages/roles/index.html"
    context_object_name = "roles"

    def get_queryset(self):
        return Role.objects.all()

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_create_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.create"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_create_role_permission"] = self.has_create_role_permission(
                self.request.user
            )
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RoleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Role
    fields = ["name", "color"]
    template_name = "pages/roles/form_index.html"

    def get_success_url(self):
        return reverse_lazy("roles")

    def form_valid(self, form):
        response = super().form_valid(form)

        Log.objects.create(
            user=self.request.user,
            action="CREATE",
            category="ADMINISTRATION",
            content_object=self.object,
            message=f"@{self.request.user} hat die Rolle {self.object} erstellt.",
        )

        return response

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_create_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.create"
        ).exists()

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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_create_role_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RoleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Role
    fields = ["name", "color"]
    template_name = "pages/roles/role.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        name = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(name=name)
        obj = get_object_or_404(queryset)
        return obj

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_rename_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.rename"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_rename_role_permission"] = self.has_rename_role_permission(
                self.request.user
            )
            context["users"] = User.objects.filter(
                advanced__role__name=self.kwargs.get(self.slug_url_kwarg)
            )
            context["permissions_system"] = CustomPermission.objects.filter(
                permission__contains="system"
            )
            context["permissions_disposition"] = CustomPermission.objects.filter(
                permission__contains="disposition"
            )
            context["permissions_management"] = CustomPermission.objects.filter(
                permission__contains="management"
            )
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RoleManageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Role
    fields = ["name", "color"]
    template_name = "pages/roles/role_manage.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        name = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(name=name)
        obj = get_object_or_404(queryset)
        return obj

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_rename_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.rename"
        ).exists()

    def has_perm_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.perm"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_rename_role_permission"] = self.has_rename_role_permission(
                self.request.user
            )
            context["has_perm_role_permission"] = self.has_perm_role_permission(
                self.request.user
            )
            context["permissions_system"] = CustomPermission.objects.filter(
                permission__contains="system"
            ).order_by("permission")
            context["permissions_disposition"] = CustomPermission.objects.filter(
                permission__contains="disposition"
            ).order_by("permission")
            context["permissions_management"] = CustomPermission.objects.filter(
                permission__contains="management"
            ).order_by("permission")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RoleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Role
    fields = ["name", "color"]
    template_name = "pages/roles/form_role.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_success_url(self):
        return reverse_lazy("role", kwargs={"name": self.object.name})

    def form_valid(self, form):
        old_role_name = self.get_object().name
        old_role_color = self.get_object().color
        response = super().form_valid(form)
        new_role_name = self.object.name
        new_role_color = self.object.color

        messages = []

        if old_role_color != new_role_color:
            messages.append(f"@{self.request.user} färbte '{old_role_name}' um.")

        if old_role_name != new_role_name:
            messages.append(
                f"@{self.request.user} nannte '{old_role_name}' auf '{new_role_name}' um."
            )

        for message in messages:
            Log.objects.create(
                user=self.request.user,
                action="UPDATE",
                category="ADMINISTRATION",
                content_object=self.object,
                message=message,
            )

        return response

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        name = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(name=name)
        obj = get_object_or_404(queryset)
        return obj

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_rename_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.rename"
        ).exists()

    def has_delete_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.delete"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_delete_role_permission"] = self.has_delete_role_permission(
                self.request.user
            )
            context["permissions_system"] = CustomPermission.objects.filter(
                permission__contains="system"
            )
            context["permissions_disposition"] = CustomPermission.objects.filter(
                permission__contains="disposition"
            )
            context["permissions_management"] = CustomPermission.objects.filter(
                permission__contains="management"
            )
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_rename_role_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RoleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Role
    template_name = "pages/roles/delete_role.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_success_url(self):
        return reverse_lazy("roles")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        name = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(name=name)
        obj = get_object_or_404(queryset)
        return obj

    def get(self, request, name):
        role = get_object_or_404(Role, name=name)
        return render(request, self.template_name, {"role": role})

    def post(self, request, name):
        role = get_object_or_404(Role, name=name)
        old_role_name = role.name

        # Create the log entry
        Log.objects.create(
            user=request.user,
            action="DELETE",
            category="ADMINISTRATION",
            content_object=role,
            message=f"{request.user} hat '{old_role_name}' gelöscht.",
        )

        role.delete()  # Löschen Sie die Rolle nach Erstellung des Log-Eintrags

        messages.success(request, f"{old_role_name} wurde erfolgreich gelöscht.")
        return HttpResponseRedirect(reverse_lazy("roles"))

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_delete_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.delete"
        ).exists()

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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_delete_role_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RolePermissionsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Role
    fields = []
    template_name = "pages/roles/form_management_permission.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_success_url(self):
        return reverse_lazy("role_manage", kwargs={"name": self.object.name})

    def form_valid(self, form):
        old_role_name = self.object.name
        selected_permission_ids = self.request.POST.getlist("selected_permissions")

        # Speichern der alten Berechtigungen der Rolle
        old_permissions = list(self.object.permissions.all())

        self.object.permissions.clear()

        for permission_id in selected_permission_ids:
            permission = CustomPermission.objects.get(id=permission_id)
            self.object.permissions.add(permission)

        new_permissions = list(self.object.permissions.all())

        permissions_changed = old_permissions != new_permissions

        response = super().form_valid(form)

        if permissions_changed:
            Log.objects.create(
                user=self.request.user,
                action="UPDATE",
                category="ADMINISTRATION",
                content_object=self.object,
                message=f"{self.request.user} hat bei '{old_role_name}' die Rechte angepasst.",
            )

        return response

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_rename_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.rename"
        ).exists()

    def has_perm_role_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.roles.perm"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_rename_role_permission"] = self.has_rename_role_permission(
                self.request.user
            )
            context["permissions_system"] = CustomPermission.objects.filter(
                permission__contains="system"
            ).order_by("permission")
            context["permissions_disposition"] = CustomPermission.objects.filter(
                permission__contains="disposition"
            ).order_by("permission")
            context["permissions_management"] = CustomPermission.objects.filter(
                permission__contains="management"
            ).order_by("permission")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_perm_role_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class RoleUsersView(LoginRequiredMixin, generic.UpdateView):
    model = Role
    fields = []
    template_name = "pages/roles/form_role_user.html"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_success_url(self):
        return reverse_lazy("role", kwargs={"name": self.object.name})

    def form_valid(self, form):
        current_assigned_users = set(self.object.users.values_list("id", flat=True))

        selected_user_ids = set(map(int, self.request.POST.getlist("selected_users")))

        users_to_remove = current_assigned_users - selected_user_ids
        standard_role = Role.objects.get(name="Standard")

        self.object.users.clear()

        for user_id in selected_user_ids:
            user = User.objects.get(id=user_id)
            advanced_user = AdvancedUser.objects.get(user=user)
            self.object.users.add(advanced_user)

        for user_id in users_to_remove:
            user = User.objects.get(id=user_id)
            advanced_user = AdvancedUser.objects.get(user=user)
            advanced_user.role = standard_role
            advanced_user.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["users"] = User.objects.all()
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

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

            if not self.has_administration_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class UsersView(LoginRequiredMixin, generic.ListView):
    model = User
    fields = ["first_name", "last_name", "username"]
    template_name = "pages/users/index.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = User.objects.all()

        # Filter aus dem GET-Parameter holen
        search_query = self.request.GET.get("search", "")
        role_query = self.request.GET.get("role", "")

        if search_query:
            # Teilen des Suchbegriffs in einzelne Worte
            search_terms = search_query.split()

            # Erstellen einer Q-Objekt für jedes Wort
            q_objects = Q()

            for term in search_terms:
                q_objects |= (
                    Q(first_name__icontains=term)
                    | Q(last_name__icontains=term)
                    | Q(username__icontains=term)
                )

            # Anwenden der Filter auf die Query
            queryset = queryset.filter(q_objects)

        if role_query:
            # Filtern nach der Rolle
            queryset = queryset.filter(advanced__role__id=role_query)

        # Sortierung anpassen
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

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_users_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.users.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["roles"] = Role.objects.all()
            context["search_query"] = self.request.GET.get("search", "")
            context["role_query"] = self.request.GET.get("role", "")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_users_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LogsView(LoginRequiredMixin, generic.ListView):
    model = Log
    fields = []
    template_name = "pages/logs.html"

    def get_queryset(self):
        return Log.objects.filter(category="SYSTEM")

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logs_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.logs.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["logs"] = Log.objects.filter(category="SYSTEM")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logs_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LogsAdministrationView(LoginRequiredMixin, generic.ListView):
    model = Log
    fields = []
    template_name = "pages/logs.html"

    def get_queryset(self):
        return Log.objects.filter(category="ADMINISTRATION")

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logs_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.logs.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["logs"] = Log.objects.filter(category="ADMINISTRATION")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logs_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LogsCommunicationView(LoginRequiredMixin, generic.ListView):
    model = Log
    fields = []
    template_name = "pages/logs.html"

    def get_queryset(self):
        return Log.objects.filter(category="COMMUNICATION")

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logs_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.logs.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["logs"] = Log.objects.filter(category="COMMUNICATION")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logs_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LogsManagementView(LoginRequiredMixin, generic.ListView):
    model = Log
    fields = []
    template_name = "pages/logs.html"

    def get_queryset(self):
        return Log.objects.filter(category="MANAGEMENT")

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logs_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.logs.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["logs"] = Log.objects.filter(category="MANAGEMENT")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logs_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LogsDispositionView(LoginRequiredMixin, generic.ListView):
    model = Log
    fields = []
    template_name = "pages/logs.html"

    def get_queryset(self):
        return Log.objects.filter(category="DISPOSITION")

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logs_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.logs.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["logs"] = Log.objects.filter(category="DISPOSITION")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logs_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LogsCloudView(LoginRequiredMixin, generic.ListView):
    model = Log
    fields = []
    template_name = "pages/logs.html"

    def get_queryset(self):
        return Log.objects.filter(category="CLOUD")

    def has_administration_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.access"
        ).exists()

    def has_logs_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="system.logs.access"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["logs"] = Log.objects.filter(category="CLOUD")
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

            if not self.has_administration_access(request.user):
                return redirect("denied")

            if not self.has_logs_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)
