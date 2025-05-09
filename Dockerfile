FROM python:3.9-slim

WORKDIR /app

# Install dependencies for health check and PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .

# First run helps diagnose SSL issues
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org pip --upgrade

# Install packages one by one to better diagnose issues
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi==0.95.0
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org uvicorn==0.21.1
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org slack-sdk==3.21.3
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org python-dotenv==1.0.0
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org numpy==1.23.5
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas==1.5.3
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org sqlalchemy==2.0.9
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org cx-oracle==8.3.0
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org vertica-python==1.1.1
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org aiohttp==3.8.4
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org python-multipart==0.0.6
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org requests==2.28.2
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org apscheduler==3.10.1
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org psycopg2-binary==2.9.6
# Install pydantic 2.x first for compatibility with newer mistralai
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org "pydantic>=2.5.2"
# Explicitly install mistralai package with newest version
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org mistralai>=1.7.0

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
  if [[ "$script" != *"03_populate_date_dimension.sql"* ]]; then\n\
    echo "Executing $script..."\n\
    PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -f "$script"\n\
  else\n\
    echo "Skipping $script due to known issues"\n\
  fi\n\
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