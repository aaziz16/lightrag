# Use an official Python image as a base
# FROM python:3.10-slim
FROM python:3 
# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r /app/requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "main_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
