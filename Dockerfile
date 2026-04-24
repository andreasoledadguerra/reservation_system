# 1. Base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Define the command that runs the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]