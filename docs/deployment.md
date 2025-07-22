# Deployment Guide

This document outlines various options for deploying the Battle Results Flask application in different environments.

## Deployment Options

### 1. PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com/) is a platform-as-a-service specifically designed for Python applications, making it an excellent choice for Flask applications.

**Advantages:**
- Free tier available
- Specifically designed for Python web applications
- Easy setup with Git integration
- Built-in SQLite support

**Steps to deploy:**
1. Sign up for a PythonAnywhere account
2. Create a new web app and select Flask
3. Clone your repository
4. Set up your virtual environment and install dependencies
5. Configure WSGI file to point to your app
6. Set up environment variables in the .env file

### 2. Heroku

[Heroku](https://www.heroku.com/) is a cloud platform that supports multiple languages including Python.

**Advantages:**
- Simple Git-based deployment
- Free tier available (with limitations)
- Scalable if your application grows

**Steps to deploy:**
1. Sign up for a Heroku account
2. Install the Heroku CLI
3. Create a `Procfile` in your project root with:
   ```
   web: gunicorn app:app
   ```
4. Add `gunicorn` to your dependencies
5. Create a `requirements.txt` file:
   ```bash
   pipenv lock -r > requirements.txt
   ```
6. Create a new Heroku app:
   ```bash
   heroku create battle-results-app
   ```
7. Set environment variables:
   ```bash
   heroku config:set FLASK_SECRET_KEY=your_secret_key
   ```
8. Deploy the application:
   ```bash
   git push heroku master
   ```

### 3. AWS Elastic Beanstalk

[AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) is a service for deploying and scaling web applications.

**Advantages:**
- Highly scalable
- Supports auto-scaling
- Reliable infrastructure

**Steps to deploy:**
1. Sign up for an AWS account
2. Install the AWS CLI and EB CLI
3. Create a `.ebignore` file to exclude files
4. Create an `application.py` file (rename app.py to application.py)
5. Initialize Elastic Beanstalk application:
   ```bash
   eb init -p python-3.8 battle-results
   ```
6. Create an environment:
   ```bash
   eb create battle-results-env
   ```
7. Deploy the application:
   ```bash
   eb deploy
   ```

### 4. Docker Container

You can containerize your application using Docker for easy deployment across various platforms.

**Advantages:**
- Consistent environment across all deployments
- Easy scaling with container orchestration tools
- Isolation from the host system

**Steps to containerize:**
1. Create a `Dockerfile` in your project root:
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY Pipfile Pipfile.lock ./
   RUN pip install pipenv && pipenv install --system --deploy

   COPY . .

   ENV FLASK_APP=app.py
   ENV FLASK_RUN_HOST=0.0.0.0
   ENV FLASK_RUN_PORT=8080

   EXPOSE 8080

   CMD ["python", "app.py"]
   ```
2. Build the Docker image:
   ```bash
   docker build -t battle-results-flask .
   ```
3. Run the container:
   ```bash
   docker run -p 8080:8080 battle-results-flask
   ```

## Database Considerations

### SQLite in Production

While SQLite is great for development, it has limitations in production:
- Limited concurrent writes
- Not suitable for high-traffic applications

For production deployments with higher traffic, consider:
1. PostgreSQL
2. MySQL
3. Cloud database services like AWS RDS or Azure Database

## HTTPS Configuration

For production, ensure your application uses HTTPS:
- With PythonAnywhere: HTTPS is provided automatically
- With Heroku: HTTPS is provided automatically
- With AWS: Configure with AWS Certificate Manager
- With custom setup: Use Let's Encrypt for free SSL certificates

## Monitoring and Logging

For production deployments, consider setting up:
- Logging with tools like Sentry or LogDNA
- Performance monitoring with New Relic or Datadog
- Health checks to monitor application availability
