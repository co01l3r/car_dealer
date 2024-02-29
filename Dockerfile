FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt to the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8000 available for the app
EXPOSE 8000

# Run the app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "car_dealer.wsgi:application"]