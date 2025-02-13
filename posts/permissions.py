from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPostAuthor(BasePermission):
    """
    Custom permission to allow only the post author or an admin to delete the post.
    """

    def has_object_permission(self, request, view, obj):
       
        if request.method in SAFE_METHODS:
            return True

        
        return obj.author == request.user or request.user.is_staff

