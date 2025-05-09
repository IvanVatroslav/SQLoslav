FROM python:3.9-slim

WORKDIR /app

# Install dependencies for health check and PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .

# Upgrade pip
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org pip --upgrade

# Install all dependencies from requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/downloads
RUN chmod +x /app/scripts/healthcheck.sh

# Create startup script
RUN echo '#!/bin/bash\n\
# Wait for database to be ready\n\
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c "\q"; do\n\
  echo "Waiting for database to be ready..."\n\
  sleep 2\n\
done\n\
\n\
# Initialize database\n\
echo "Initializing database..."\n\
for script in database/init/*.sql; do\n\
  echo "Executing $script..."\n\
  PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -f "$script"\n\
done\n\
\n\
# Start the application\n\
echo "Starting application..."\n\
python main.py' > /app/start.sh

RUN chmod +x /app/start.sh

# Install the application as a package
RUN pip install -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data
ENV DOWNLOAD_DIR=/app/downloads

# Expose the port the app runs on
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD /app/scripts/healthcheck.sh

# Command to run the application
CMD ["/app/start.sh"] 