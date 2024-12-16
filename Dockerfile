# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download YOLOv3 weights and configuration files
RUN curl -o yolov3.weights https://pjreddie.com/media/files/yolov3.weights
RUN curl -o yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
RUN curl -o coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
