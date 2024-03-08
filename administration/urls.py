from django.urls import path

from .views import (
    AppLogoUpdateView,
    AppNameUpdateView,
    LogsAdministrationView,
    LogsCloudView,
    LogsCommunicationView,
    LogsDispositionView,
    LogsManagementView,
    LogsView,
    RoleCreateView,
    RoleDeleteView,
    RoleDetailView,
    RoleManageDetailView,
    RolePermissionsUpdateView,
    RolesView,
    RoleUpdateView,
    RoleUsersView,
    SignatureView,
    SystemView,
    UpdateSignatureView,
    UsersView,
)

urlpatterns = [
    path("", SystemView.as_view(), name="system"),
    path("app/rename/<int:pk>", AppNameUpdateView.as_view(), name="system_app_rename"),
    path(
        "app/logo/<int:pk>/update",
        AppLogoUpdateView.as_view(),
        name="system_app_logo_update",
    ),
    path("roles/", RolesView.as_view(), name="roles"),
    path("roles/create", RoleCreateView.as_view(), name="roles_create"),
    path("roles/<slug:name>", RoleDetailView.as_view(), name="role"),
    path("roles/<slug:name>/users/add", RoleUsersView.as_view(), name="role_users"),
    path(
        "roles/<slug:name>/manage", RoleManageDetailView.as_view(), name="role_manage"
    ),
    path(
        "roles/<slug:name>/manage/update", RoleUpdateView.as_view(), name="role_update"
    ),
    path(
        "roles/<slug:name>/manage/delete", RoleDeleteView.as_view(), name="role_delete"
    ),
    path(
        "roles/<slug:name>/manage/permissions",
        RolePermissionsUpdateView.as_view(),
        name="role_permission",
    ),
    path("users/", UsersView.as_view(), name="users"),
    path("logs/", LogsView.as_view(), name="logs"),
    path(
        "logs/administration",
        LogsAdministrationView.as_view(),
        name="logs_administration",
    ),
    path(
        "logs/communication",
        LogsCommunicationView.as_view(),
        name="logs_communication",
    ),
    path(
        "logs/management",
        LogsManagementView.as_view(),
        name="logs_management",
    ),
    path(
        "logs/disposition",
        LogsDispositionView.as_view(),
        name="logs_disposition",
    ),
    path(
        "logs/cloud",
        LogsCloudView.as_view(),
        name="logs_cloud",
    ),
    path("signature", SignatureView.as_view(), name="signature"),
    path("signature/<int:pk>", UpdateSignatureView.as_view(), name="signature_update"),
]
