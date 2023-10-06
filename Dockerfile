# Use the official Python image as the base image
FROM python:3.11
# Set the working directory inside the container
WORKDIR /app
# Copy the requirements.txt file into the container
COPY requirements.txt .
# Setup Python Virtual Environment
RUN python -m venv /app/venv
# Activate the Virtual Environment and Install Dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt
# Copy the rest of the source code into the container
COPY src/ ./src
COPY cv.txt ./

# Expose the port on which the Uvicorn server will run
EXPOSE 8000
# Run the Uvicorn application 
CMD ["/app/venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]