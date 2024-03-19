# Use an official Python runtime as a parent image
FROM python:3.11.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requrirements to keep cache.
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 3001

# Run app.py when the container launches
CMD ["python", "app.py"]
#CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]