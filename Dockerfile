# Use Python slim image with AMD64 platform (required by challenge)
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies (PyMuPDF + JSONSchema)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Run the main PDF processing script
ENTRYPOINT ["python", "process_pdfs.py"]
