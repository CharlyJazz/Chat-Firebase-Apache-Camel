# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipenv files into the container
COPY Pipfile Pipfile.lock /app/

# Install Pipenv and the project dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . /app/

# Define the command to run your application
CMD ["pipenv", "run", "python", "run.py"]
