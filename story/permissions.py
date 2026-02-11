from rest_framework import permissions

class IsAuthorOrStoryCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or obj.story.created_by == request.user 