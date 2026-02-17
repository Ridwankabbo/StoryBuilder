from django.contrib import admin
from .models import Story, Sentence, StoriColaborationRequest
# Register your models here.


class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'display_contributors', 'version', 'last_update')
    
    search_fields = ('title', 'created_by__username')
    
    list_filter = ('version', 'created_at', 'last_update')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by').prefetch_related('contributors')
    
    @admin.display(description='Contributors')
    def display_contributors(self, obj):
        # Joins all contributor usernames into a single string separated by commas
        return ", ".join([user.username for user in obj.contributors.all()])

admin.site.register(Story, StoryAdmin)

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('story', 'author', 'order', 'added_at')

admin.site.register(Sentence, SentenceAdmin)


class StoriCollaborationRequestAdmin(admin.ModelAdmin):
    list_display = ('story', 'requester', 'request_status', 'requested_at', 'responced_at')

admin.site.register(StoriColaborationRequest, StoriCollaborationRequestAdmin)
