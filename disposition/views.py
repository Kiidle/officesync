from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from administration.models import Log
from authentication.models import OfficeSync
from communication.models import Announcement, Message
from disposition.models import Station, Tour, Vehicle

# Create your views here.


class ToursView(LoginRequiredMixin, generic.ListView):
    model = Tour
    fields = ["name"]
    template_name = "pages/tours/index.html"

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

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

            if not self.has_disposition_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LocationsView(LoginRequiredMixin, generic.ListView):
    model = Station
    fields = ["name"]
    template_name = "pages/stations/index.html"
    context_object_name = "stations"

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_create_location_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.location.create"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_create_location_permission"] = (
                self.has_create_location_permission(self.request.user)
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class CreateLocationView(LoginRequiredMixin, generic.CreateView):
    model = Station
    fields = [
        "name",
        "contactmail",
        "contactphone",
        "capacity",
        "country",
        "state",
        "location",
        "street",
    ]
    template_name = "pages/stations/form.html"

    def get_success_url(self):
        return reverse_lazy("stations")

    def form_valid(self, form):
        response = super().form_valid(form)

        Log.objects.create(
            user=self.request.user,
            action="CREATE",
            category="DISPOSITION",
            content_object=self.object,
            message=f"@{self.request.user} hat den Standort {self.object.name} erstellt.",
        )

        return response

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_create_location_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.location.create"
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

            if not self.has_create_location_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class LocationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Station
    fields = [
        "name",
        "contactmail",
        "contactphone",
        "capacity",
        "country",
        "state",
        "location",
        "street",
    ]
    template_name = "pages/stations/station.html"

    def has_update_location_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.location.update"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_update_location_permission"] = (
                self.has_update_location_permission(self.request.user)
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

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.advanced.privacy:
                return redirect("privacy")

            if not request.user.advanced.terms:
                return redirect("terms")

            if not request.user.advanced.copyright:
                return redirect("copyright")

            if not self.has_disposition_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class UpdateLocationView(LoginRequiredMixin, generic.UpdateView):
    model = Station
    fields = [
        "name",
        "contactmail",
        "contactphone",
        "capacity",
        "country",
        "state",
        "location",
        "street",
    ]
    template_name = "pages/stations/form.html"

    def get_success_url(self):
        return reverse_lazy("stations")

    def form_valid(self, form):
        response = super().form_valid(form)

        Log.objects.create(
            user=self.request.user,
            action="UPDATE",
            category="DISPOSITION",
            content_object=self.object,
            message=f"@{self.request.user} hat den Standort {self.object.name} verändert.",
        )

        return response

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_update_location_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.location.update"
        ).exists()

    def has_delete_location_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.location.delete"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_delete_location_permission"] = (
                self.has_delete_location_permission(self.request.user)
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

            if not self.has_update_location_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class StationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Vehicle
    template_name = "pages/stations/delete.html"

    def get_success_url(self):
        return reverse_lazy("stations")

    def get(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        return render(request, self.template_name, {"station": station})

    def post(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        old_station_name = station.name

        # Create the log entry
        Log.objects.create(
            user=request.user,
            action="DELETE",
            category="DISPOSITION",
            content_object=station,
            message=f"{request.user} hat den Standort '{old_station_name}' gelöscht.",
        )

        station.delete()  # Löschen Sie die Rolle nach Erstellung des Log-Eintrags

        messages.success(request, f"{old_station_name} wurde erfolgreich gelöscht.")
        return HttpResponseRedirect(reverse_lazy("stations"))

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_delete_location_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.location.delete"
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

            if not self.has_delete_location_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class VehiclesView(LoginRequiredMixin, generic.ListView):
    model = Vehicle
    fields = ["name"]
    template_name = "pages/vehicles/index.html"
    context_object_name = "vehicles"

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_create_vehicle_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.vehicle.create"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_create_vehicle_permission"] = (
                self.has_create_vehicle_permission(self.request.user)
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class CreateVehicleView(LoginRequiredMixin, generic.CreateView):
    model = Vehicle
    fields = [
        "license_plate",
        "name",
        "type",
        "model",
        "manufacturer",
        "year_of_manufacturer",
        "vin",
        "power_engine",
        "capacity",
        "fuel_type",
        "fuel_consumption",
        "insurance",
        "condition",
    ]
    template_name = "pages/vehicles/form.html"

    def get_success_url(self):
        return reverse_lazy("vehicles")

    def form_valid(self, form):
        response = super().form_valid(form)

        Log.objects.create(
            user=self.request.user,
            action="CREATE",
            category="DISPOSITION",
            content_object=self.object,
            message=f"@{self.request.user} hat das Fahrzeug {self.object.license_plate} erstellt.",
        )

        return response

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_create_vehicle_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.vehicle.create"
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

            if not self.has_create_vehicle_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class VehicleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Vehicle
    fields = [
        "license_plate",
        "name",
        "type",
        "model",
        "manufacturer",
        "year_of_manufacturer",
        "vin",
        "power_engine",
        "capacity",
        "fuel_type",
        "fuel_consumption",
        "insurance",
        "condition",
    ]
    template_name = "pages/vehicles/vehicle.html"

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_update_vehicle_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.vehicle.update"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_update_vehicle_permission"] = (
                self.has_update_vehicle_permission(self.request.user)
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class UpdateVehicleView(LoginRequiredMixin, generic.UpdateView):
    model = Vehicle
    fields = [
        "license_plate",
        "name",
        "type",
        "model",
        "manufacturer",
        "year_of_manufacturer",
        "vin",
        "power_engine",
        "capacity",
        "fuel_type",
        "fuel_consumption",
        "insurance",
    ]
    template_name = "pages/vehicles/form.html"

    def get_success_url(self):
        return reverse_lazy("vehicles")

    def form_valid(self, form):
        response = super().form_valid(form)

        Log.objects.create(
            user=self.request.user,
            action="CREATE",
            category="DISPOSITION",
            content_object=self.object,
            message=f"@{self.request.user} hat das Fahrzeug {self.object.license_plate} erstellt.",
        )

        return response

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_update_vehicle_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.vehicle.update"
        ).exists()

    def has_delete_vehicle_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.vehicle.delete"
        ).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["officesync"] = OfficeSync.objects.first()
        if self.request.user.is_authenticated:
            context["has_delete_vehicle_permission"] = (
                self.has_delete_vehicle_permission(self.request.user)
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

            if not self.has_update_vehicle_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)


class VehicleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Vehicle
    template_name = "pages/vehicles/delete.html"

    def get_success_url(self):
        return reverse_lazy("vehicles")

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        return render(request, self.template_name, {"vehicle": vehicle})

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        old_vehicle_name = vehicle.license_plate

        # Create the log entry
        Log.objects.create(
            user=request.user,
            action="DELETE",
            category="DISPOSITION",
            content_object=vehicle,
            message=f"{request.user} hat das Fahrzeug '{old_vehicle_name}' gelöscht.",
        )

        vehicle.delete()  # Löschen Sie die Rolle nach Erstellung des Log-Eintrags

        messages.success(request, f"{old_vehicle_name} wurde erfolgreich gelöscht.")
        return HttpResponseRedirect(reverse_lazy("vehicles"))

    def has_disposition_access(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.access"
        ).exists()

    def has_delete_vehicle_permission(self, user):
        return user.advanced.role.permissions.filter(
            permission="disposition.vehicle.delete"
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

            if not self.has_disposition_access(request.user):
                return redirect("denied")

            if not self.has_delete_vehicle_permission(request.user):
                return redirect("denied")

        return super().dispatch(request, *args, **kwargs)
