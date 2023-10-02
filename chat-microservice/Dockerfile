# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Copy the Pipfile and Pipfile.lock into the container at /app
COPY Pipfile Pipfile.lock /app/

# Install pipenv to manage dependencies
RUN pip install pipenv

# Install project dependencies using Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that your FastAPI application will run on (e.g., 9000)
EXPOSE 9000

# Define an environment variable for FastAPI to run in production mode
ENV UVICORN_CMD="uvicorn app.main:app --host 0.0.0.0 --port 9000"

# Start FastAPI when the container launches
CMD ["pipenv", "run", "sh", "-c", "$UVICORN_CMD"]
