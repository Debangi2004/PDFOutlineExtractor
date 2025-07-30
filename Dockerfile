FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt

# Copy all files
COPY . .

# Set command
CMD ["python", "main.py"]
#ENTRYPOINT ["python", "main.py"]


