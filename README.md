# Pneumonia Detection System

An AI-powered web application for detecting pneumonia from chest X-ray images using deep learning. Built with Django and TensorFlow.

## Features

- **AI-Powered Analysis**: Upload chest X-ray images and get instant AI analysis
- **Multiple Prediction Types**: Detect normal cases, bacterial pneumonia, and viral pneumonia
- **Confidence Scoring**: Get confidence levels for each prediction
- **Image Gallery**: Browse and filter all analyzed images
- **Admin Interface**: Manage images and results through Django admin
- **Responsive Design**: Modern, mobile-friendly interface
- **API Support**: RESTful API for programmatic access

## Technology Stack

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5, Font Awesome
- **AI/ML**: TensorFlow, OpenCV, NumPy
- **Database**: SQLite (default), supports PostgreSQL/MySQL
- **Image Processing**: Pillow (PIL)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PneumoniaDetection
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage

### Uploading Images

1. Navigate to the upload page
2. Drag and drop or select a chest X-ray image
3. Add optional title and notes
4. Click "Analyze Image" to process
5. View results with confidence scores

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

**Maximum file size**: 10MB

### Viewing Results

- **Home Page**: Overview with statistics and recent analyses
- **Gallery**: Browse all analyzed images with filtering options
- **Detail View**: Comprehensive information about each analysis
- **Results Page**: Detailed analysis results with confidence scores

## AI Model

The current implementation includes a placeholder analysis function that simulates AI predictions. To integrate a real deep learning model:

1. Train your model using TensorFlow/Keras
2. Save the model file
3. Replace the `analyze_chest_xray()` function in `detection/views.py`
4. Update the model loading and prediction logic

### Example Model Integration

```python
import tensorflow as tf

def analyze_chest_xray(image_path):
    # Load pre-trained model
    model = tf.keras.models.load_model('path/to/your/model.h5')
    
    # Preprocess image
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = tf.expand_dims(img_array, 0)
    
    # Make prediction
    prediction = model.predict(img_array)
    
    # Process results
    confidence = float(prediction[0][0])
    result = 'pneumonia' if confidence > 0.5 else 'normal'
    
    return result, confidence, 'unknown'
```

## API Endpoints

### Analyze Image
- **URL**: `/api/analyze/`
- **Method**: POST
- **Body**: JSON with `image_path`
- **Response**: Prediction results with confidence scores

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration

The default configuration uses SQLite. For production, consider using PostgreSQL or MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Deployment

### Production Settings

1. Set `DEBUG = False` in settings.py
2. Configure a production database
3. Set up static file serving
4. Configure your web server (nginx, Apache)
5. Use a production WSGI server (Gunicorn, uWSGI)

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "pneumonia_detection.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Medical Disclaimer

**IMPORTANT**: This application is for educational and research purposes only. The AI analysis should not replace professional medical diagnosis, treatment, or advice. Always consult with qualified healthcare professionals for medical decisions.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Acknowledgments

- Chest X-ray datasets used for training
- Medical imaging research community
- Open source contributors
