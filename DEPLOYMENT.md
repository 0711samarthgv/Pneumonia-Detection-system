# Deployment Guide for Pneumonia Detection Website

This guide provides multiple options for hosting your Django-based pneumonia detection website.

## Prerequisites

Before deploying, ensure you have:
- A domain name (optional but recommended)
- Git repository (GitHub, GitLab, or Bitbucket)
- Basic understanding of command line

## Option 1: Railway (Recommended for Beginners)

Railway is an excellent platform for Django applications with built-in database support.

### Steps:

1. **Prepare your repository:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect Django and deploy

3. **Configure environment variables:**
   - In Railway dashboard, go to Variables tab
   - Add: `SECRET_KEY=your-new-secret-key`
   - Add: `DEBUG=False`
   - Add: `ALLOWED_HOSTS=your-app-name.railway.app`

4. **Access your app:**
   - Railway will provide a URL like `https://your-app-name.railway.app`

## Option 2: Heroku

### Steps:

1. **Install Heroku CLI:**
   - Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Heroku app:**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Configure environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-new-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```

## Option 3: DigitalOcean App Platform

### Steps:

1. **Create app specification file:**
   Create `app.yaml`:
   ```yaml
   name: pneumonia-detection
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/your-repo
       branch: main
     run_command: gunicorn pneumonia_detection.wsgi:application --bind 0.0.0.0:8080
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: SECRET_KEY
       value: your-secret-key
     - key: DEBUG
       value: "False"
     - key: ALLOWED_HOSTS
       value: your-app-name.ondigitalocean.app
   ```

2. **Deploy:**
   - Go to DigitalOcean App Platform
   - Create new app from GitHub
   - Upload the app.yaml file
   - Deploy

## Option 4: AWS EC2 (Advanced)

### Steps:

1. **Launch EC2 instance:**
   - Choose Ubuntu 20.04 LTS
   - Select t3.medium or larger (for ML workloads)
   - Configure security group (ports 22, 80, 443)

2. **Connect and setup:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   sudo apt update
   sudo apt install python3-pip nginx git
   ```

3. **Deploy application:**
   ```bash
   git clone your-repo-url
   cd PneumoniaDetection
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. **Configure Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 pneumonia_detection.wsgi:application
   ```

5. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/pneumonia-detection
   ```
   Add the nginx configuration from the nginx.conf file

## Option 5: Docker Deployment (Any VPS)

### Steps:

1. **On your VPS:**
   ```bash
   git clone your-repo-url
   cd PneumoniaDetection
   docker-compose up -d
   ```

2. **Configure domain (optional):**
   - Point your domain to the VPS IP
   - Update nginx.conf with your domain name

## Option 6: Google Cloud Platform

### Steps:

1. **Create project in GCP Console**
2. **Enable Cloud Run API**
3. **Deploy using Cloud Build:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/pneumonia-detection
   gcloud run deploy --image gcr.io/PROJECT-ID/pneumonia-detection --platform managed
   ```

## Post-Deployment Steps

### 1. Create Superuser
```bash
# For Railway/Heroku
railway run python manage.py createsuperuser
# or
heroku run python manage.py createsuperuser
```

### 2. Configure Domain (Optional)
- Purchase domain from Namecheap, GoDaddy, etc.
- Point DNS to your hosting platform
- Update ALLOWED_HOSTS in environment variables

### 3. Set up SSL Certificate
Most platforms provide free SSL certificates automatically.

### 4. Monitor Performance
- Set up monitoring (Railway/Heroku have built-in monitoring)
- Monitor memory usage (ML models can be memory-intensive)

## Cost Estimates

- **Railway**: $5-20/month (free tier available)
- **Heroku**: $7-25/month (free tier discontinued)
- **DigitalOcean**: $5-12/month
- **AWS EC2**: $10-50/month (depending on instance size)
- **Google Cloud**: $5-30/month

## Troubleshooting

### Common Issues:

1. **Static files not loading:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database errors:**
   ```bash
   python manage.py migrate
   ```

3. **Memory issues with ML models:**
   - Use smaller model files
   - Implement model caching
   - Consider using a larger instance

4. **File upload size limits:**
   - Configure nginx client_max_body_size
   - Update Django FILE_UPLOAD_MAX_MEMORY_SIZE

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Set up proper CORS headers
- [ ] Implement rate limiting
- [ ] Regular security updates

## Performance Optimization

1. **Enable caching:**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. **Use CDN for static files**
3. **Optimize images before upload**
4. **Implement database indexing**

## Support

If you encounter issues:
1. Check platform-specific documentation
2. Review Django deployment checklist
3. Check application logs
4. Test locally with production settings

Remember: This is a medical application, so ensure compliance with healthcare regulations in your jurisdiction.
