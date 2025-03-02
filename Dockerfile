FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Create necessary directories
RUN mkdir -p /app/scripts
RUN mkdir -p /app/shares
RUN mkdir -p /app/templates

# Set permissions for the shares directory
RUN chmod 777 /app/shares

# Expose port
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]