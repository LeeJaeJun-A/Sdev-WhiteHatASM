# Use the official Python image as a parent image
FROM python:3.10.8

# Set the working directory inside the container
WORKDIR /app

COPY . /app/backend

WORKDIR /app/backend

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy the entire application into the container


ENV PYTHONPATH=/app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
