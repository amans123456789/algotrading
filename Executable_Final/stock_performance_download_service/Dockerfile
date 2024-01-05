# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

RUN echo "Debugging: Installing dependencies from requirements.txt"
# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# # Create a directory for CSV files inside the container
# RUN mkdir /app/Stock_Performance_Document2

# Copy the FastAPI application code into the container at /app
COPY . /app/

# Expose port 80 for the FastAPI application
EXPOSE 8000

# RUN chmod a+x entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]

# Define the command to run the application when the container starts
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# CMD ["uvicorn", "service:app", "--reload"]

