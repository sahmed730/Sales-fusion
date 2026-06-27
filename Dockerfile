# Base Image
FROM python:3.11-slim

# Set Working Directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports for Streamlit and FastAPI
EXPOSE 8501 8000

# Command to run both Streamlit and FastAPI using a wrapper or just default to Streamlit
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
