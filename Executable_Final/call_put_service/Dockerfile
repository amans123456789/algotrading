# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Copy the FastAPI application code into the container at /app
COPY . /app/

# Expose port 80 for the FastAPI application
EXPOSE 8000

# RUN chmod a+x entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]

# Define the command to run the application when the container starts
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# CMD ["uvicorn", "service:app", "--reload"]