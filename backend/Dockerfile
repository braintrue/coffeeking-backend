# Dockerfile for the CoffeeKing backend service.

# Use an official lightweight Python image.
FROM python:3.11-slim AS base

# Create and set the working directory.
WORKDIR /app

# Copy the application code into the container.
COPY . /app

# Install production dependencies.  The requirements file specifies
# FastAPI, Uvicorn, SQLAlchemy and other libraries used by the project.
RUN pip install --no-cache-dir --upgrade pip \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Expose the port that the FastAPI application will listen on.
EXPOSE 8000

# Run the application using Uvicorn.  The ``--host`` flag makes the
# service externally visible in the Docker environment.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]