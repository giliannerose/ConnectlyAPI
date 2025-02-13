from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPostAuthor(BasePermission):
    """
    Custom permission to allow only the post author or an admin to delete the post.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS for any authenticated user
        if request.method in SAFE_METHODS:
            return True

        # Allow deletion if the user is the author or an admin
        return obj.author == request.user or request.user.is_staff

