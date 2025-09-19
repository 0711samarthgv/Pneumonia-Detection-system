from django import forms
from .models import ChestXRayImage

class ChestXRayUploadForm(forms.ModelForm):
    """Form for uploading chest X-ray images"""
    
    class Meta:
        model = ChestXRayImage
        fields = ['title', 'image', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title for this image (optional)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any notes about this image (optional)'
            }),
        }
    
    def clean_image(self):
        """Validate uploaded image"""
        image = self.cleaned_data.get('image')
        
        if not image:
            raise forms.ValidationError('Please select an image to upload.')
        
        # Check file size (max 10MB)
        if image.size > 10 * 1024 * 1024:
            raise forms.ValidationError('Image file size must be less than 10MB.')
        
        # Check file extension
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        file_extension = image.name.lower()
        if not any(file_extension.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                'Please upload an image file (JPG, PNG, BMP, or TIFF).'
            )
        
        return image
    
    def clean_title(self):
        """Clean and validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
        return title
