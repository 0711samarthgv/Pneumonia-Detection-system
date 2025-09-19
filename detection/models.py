from django.db import models
from django.utils import timezone

class ChestXRayImage(models.Model):
    """Model for storing chest X-ray images and their analysis results"""
    
    # Choices for prediction results
    PREDICTION_CHOICES = [
        ('normal', 'Normal'),
        ('pneumonia', 'Pneumonia'),
        ('pending', 'Pending Analysis'),
    ]
    
    # Choices for pneumonia types
    PNEUMONIA_TYPE_CHOICES = [
        ('bacterial', 'Bacterial Pneumonia'),
        ('viral', 'Viral Pneumonia'),
        ('unknown', 'Unknown'),
    ]
    
    # Basic fields
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='chest_xrays/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # Prediction results
    prediction = models.CharField(
        max_length=20, 
        choices=PREDICTION_CHOICES, 
        default='pending'
    )
    confidence_score = models.FloatField(null=True, blank=True)
    pneumonia_type = models.CharField(
        max_length=20,
        choices=PNEUMONIA_TYPE_CHOICES,
        default='unknown'
    )
    
    # Analysis metadata
    analysis_date = models.DateTimeField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    # Additional notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Chest X-Ray Image'
        verbose_name_plural = 'Chest X-Ray Images'
    
    def __str__(self):
        return f"{self.title or 'Untitled'} - {self.prediction} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
    
    def get_prediction_display_color(self):
        """Return CSS color class based on prediction"""
        if self.prediction == 'normal':
            return 'text-success'
        elif self.prediction == 'pneumonia':
            return 'text-danger'
        else:
            return 'text-warning'
    
    def get_confidence_percentage(self):
        """Return confidence score as percentage"""
        if self.confidence_score is not None:
            return f"{self.confidence_score * 100:.1f}%"
        return "N/A"
