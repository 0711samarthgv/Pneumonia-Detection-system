from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.paginator import Paginator
import json
import time
import os
from PIL import Image
import numpy as np
from .models import ChestXRayImage
from .forms import ChestXRayUploadForm

def home(request):
    """Home page with upload form and recent analyses"""
    recent_analyses = ChestXRayImage.objects.all()[:5]
    
    context = {
        'recent_analyses': recent_analyses,
        'total_analyses': ChestXRayImage.objects.count(),
        'normal_count': ChestXRayImage.objects.filter(prediction='normal').count(),
        'pneumonia_count': ChestXRayImage.objects.filter(prediction='pneumonia').count(),
    }
    return render(request, 'detection/home.html', context)

def upload_image(request):
    """Handle image upload and analysis"""
    if request.method == 'POST':
        form = ChestXRayUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the image
            chest_xray = form.save(commit=False)
            chest_xray.save()
            
            # Perform analysis (simulated for now)
            start_time = time.time()
            prediction, confidence, pneumonia_type = analyze_chest_xray(chest_xray.image.path)
            processing_time = time.time() - start_time
            
            # Update the model with results
            chest_xray.prediction = prediction
            chest_xray.confidence_score = confidence
            chest_xray.pneumonia_type = pneumonia_type
            chest_xray.analysis_date = timezone.now()
            chest_xray.processing_time = processing_time
            chest_xray.save()
            
            messages.success(request, 'Image analyzed successfully!')
            return redirect('detection:result', pk=chest_xray.pk)
    else:
        form = ChestXRayUploadForm()
    
    return render(request, 'detection/upload.html', {'form': form})

def result(request, pk):
    """Display analysis results"""
    chest_xray = get_object_or_404(ChestXRayImage, pk=pk)
    return render(request, 'detection/result.html', {'chest_xray': chest_xray})

def gallery(request):
    """Display all analyzed images"""
    images = ChestXRayImage.objects.all()
    
    # Filtering
    prediction_filter = request.GET.get('prediction')
    if prediction_filter:
        images = images.filter(prediction=prediction_filter)
    
    # Pagination
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'prediction_filter': prediction_filter,
    }
    return render(request, 'detection/gallery.html', context)

def image_detail(request, pk):
    """Detailed view of a single image"""
    chest_xray = get_object_or_404(ChestXRayImage, pk=pk)
    return render(request, 'detection/image_detail.html', {'chest_xray': chest_xray})

@csrf_exempt
def api_analyze(request):
    """API endpoint for image analysis"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_path = data.get('image_path')
            
            if not image_path or not os.path.exists(image_path):
                return JsonResponse({'error': 'Image not found'}, status=404)
            
            # Perform analysis
            start_time = time.time()
            prediction, confidence, pneumonia_type = analyze_chest_xray(image_path)
            processing_time = time.time() - start_time
            
            return JsonResponse({
                'prediction': prediction,
                'confidence': confidence,
                'pneumonia_type': pneumonia_type,
                'processing_time': processing_time
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def analyze_chest_xray(image_path):
    """
    Analyze a chest X-ray image and return prediction results.
    This is a placeholder function - in a real implementation, you would:
    1. Load a pre-trained deep learning model
    2. Preprocess the image
    3. Run inference
    4. Return results
    """
    try:
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))  # Standard size for many models
        
        # Convert to numpy array and normalize
        img_array = np.array(img) / 255.0
        
        # Placeholder analysis logic
        # In reality, you would run this through your trained model
        import random
        random.seed(hash(image_path) % 1000)  # Deterministic for demo
        
        # Simulate model prediction
        if random.random() > 0.7:
            prediction = 'normal'
            confidence = random.uniform(0.7, 0.95)
            pneumonia_type = 'unknown'
        else:
            prediction = 'pneumonia'
            confidence = random.uniform(0.6, 0.9)
            pneumonia_type = random.choice(['bacterial', 'viral'])
        
        return prediction, confidence, pneumonia_type
        
    except Exception as e:
        # Return default values if analysis fails
        return 'pending', 0.0, 'unknown'
