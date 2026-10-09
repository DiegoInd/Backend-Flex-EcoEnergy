from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAPIAdminOrReadOnlyOperator(BasePermission):
    """
    Administrador API: CRUD completo.
    Operador API: solo lectura.
    Usuario sin rol API: acceso denegado.
    """

    message = "No tienes permisos para realizar esta operación."

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Administrador API: acceso completo
        if user.groups.filter(name="api_admin").exists():
            return True

        # Operador API: solo GET, HEAD y OPTIONS
        if user.groups.filter(name="api_operador").exists():
            return request.method in SAFE_METHODS

        # Usuarios sin rol API: acceso denegado
        return False