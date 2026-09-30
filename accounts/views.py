import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView

from .forms import OrganizationForm
from .models import Organization, PasswordResetCode


User = get_user_model()


def password_reset_request(request):
    mensaje = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        mensaje = (
            "Si el correo está registrado, recibirás un código "
            "de recuperación."
        )

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user:
            PasswordResetCode.objects.filter(
                user=user,
                used=False,
            ).update(used=True)

            code = f"{secrets.randbelow(1000000):06d}"

            PasswordResetCode.objects.create(
                user=user,
                code_hash=make_password(code),
                expires_at=timezone.now() + timedelta(seconds=120),
            )

            send_mail(
                subject="Código de recuperación - EcoEnergy",
                message=(
                    f"Tu código de recuperación es: {code}\n\n"
                    "Este código vence en 120 segundos.\n"
                    "Si no solicitaste este cambio, ignora este mensaje."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session["password_reset_user_id"] = user.id

            return redirect("password_reset_verify")

    return render(
        request,
        "accounts/password_reset_request.html",
        {"mensaje": mensaje},
    )


def password_reset_verify(request):
    error = None

    user_id = request.session.get("password_reset_user_id")

    if not user_id:
        return redirect("password_reset_request")

    reset_code = (
        PasswordResetCode.objects
        .filter(
            user_id=user_id,
            used=False,
        )
        .order_by("-created_at")
        .first()
    )

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        if not reset_code:
            error = "No existe un código de recuperación válido."

        elif timezone.now() > reset_code.expires_at:
            reset_code.used = True
            reset_code.save(update_fields=["used"])
            error = "El código ha expirado. Solicita uno nuevo."

        elif reset_code.failed_attempts >= 5:
            reset_code.used = True
            reset_code.save(update_fields=["used"])
            error = "Se alcanzó el máximo de intentos. Solicita un nuevo código."

        elif check_password(code, reset_code.code_hash):
            request.session["password_reset_verified"] = True
            request.session["password_reset_code_id"] = reset_code.id

            return redirect("password_reset_confirm")

        else:
           reset_code.failed_attempts += 1

        if reset_code.failed_attempts >= 5:
            reset_code.used = True
            error = "Se alcanzó el máximo de intentos. Solicita un nuevo código."
        else:
            error = "El código ingresado no es correcto."

        reset_code.save(
            update_fields=["failed_attempts", "used"]
        )

    return render(
        request,
        "accounts/password_reset_verify.html",
        {"error": error},
    )


def password_reset_confirm(request):
    error = None

    user_id = request.session.get("password_reset_user_id")
    verified = request.session.get("password_reset_verified")
    reset_code_id = request.session.get("password_reset_code_id")

    # No permitir entrar directamente sin verificar el código.
    if not user_id or not verified or not reset_code_id:
        return redirect("password_reset_request")

    user = User.objects.filter(
        id=user_id,
        is_active=True,
    ).first()

    reset_code = PasswordResetCode.objects.filter(
        id=reset_code_id,
        user_id=user_id,
        used=False,
    ).first()

    if not user or not reset_code:
        return redirect("password_reset_request")

    if request.method == "POST":
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if password1 != password2:
            error = "Las contraseñas no coinciden."

        elif len(password1) < 10:
            error = "La contraseña debe tener mínimo 10 caracteres."

        elif not any(c.isupper() for c in password1):
            error = "La contraseña debe incluir una letra mayúscula."

        elif not any(c.islower() for c in password1):
            error = "La contraseña debe incluir una letra minúscula."

        elif not any(c.isdigit() for c in password1):
            error = "La contraseña debe incluir un número."

        elif not any(not c.isalnum() for c in password1):
            error = "La contraseña debe incluir un carácter especial."

        else:
            try:
                validate_password(password1, user=user)

                # Django almacena la contraseña mediante hash.
                user.set_password(password1)
                user.save(update_fields=["password"])

                # El código no puede volver a utilizarse.
                reset_code.used = True
                reset_code.save(update_fields=["used"])

                # Eliminamos los datos temporales de recuperación.
                request.session.pop("password_reset_user_id", None)
                request.session.pop("password_reset_verified", None)
                request.session.pop("password_reset_code_id", None)

                return redirect("login")

            except ValidationError as e:
                error = " ".join(e.messages)

    return render(
        request,
        "accounts/password_reset_confirm.html",
        {"error": error},
    )

class OrganizationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Organization
    template_name = "accounts/organization_list.html"
    context_object_name = "organizations"
    permission_required = "accounts.view_organization"
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset().filter(deleted_at__isnull=True)

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            id=self.request.user.profile.organization_id
        )

class OrganizationCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Organization
    form_class = OrganizationForm
    template_name = "accounts/organization_form.html"
    permission_required = "accounts.add_organization"
    raise_exception = True
    success_url = reverse_lazy("organization_list")
    success_message = "Organización creada correctamente."

class OrganizationUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Organization
    form_class = OrganizationForm
    template_name = "accounts/organization_form.html"
    permission_required = "accounts.change_organization"
    raise_exception = True
    success_url = reverse_lazy("organization_list")
    success_message = "Organización actualizada correctamente."

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            deleted_at__isnull=True
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            id=self.request.user.profile.organization_id
        )

class OrganizationDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Organization
    fields = []
    permission_required = "accounts.delete_organization"
    raise_exception = True
    success_url = reverse_lazy("organization_list")

    def get_queryset(self):
        queryset = Organization.objects.filter(
            deleted_at__isnull=True
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            id=self.request.user.profile.organization_id
        )

    def post(self, request, *args, **kwargs):
        organization = self.get_object()
        organization.deleted_at = timezone.now()
        organization.save(update_fields=["deleted_at"])

        return redirect(self.success_url)