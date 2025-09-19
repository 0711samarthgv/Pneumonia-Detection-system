from django.contrib import admin
from .models import ChestXRayImage

@admin.register(ChestXRayImage)
class ChestXRayImageAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'prediction', 
        'confidence_score', 
        'pneumonia_type', 
        'uploaded_at', 
        'analysis_date'
    ]
    list_filter = [
        'prediction', 
        'pneumonia_type', 
        'uploaded_at', 
        'analysis_date'
    ]
    search_fields = ['title', 'notes']
    readonly_fields = ['uploaded_at', 'analysis_date', 'processing_time']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'image', 'uploaded_at')
        }),
        ('Analysis Results', {
            'fields': ('prediction', 'confidence_score', 'pneumonia_type', 'analysis_date', 'processing_time')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
