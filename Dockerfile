FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Install Python libraries + system tools
RUN apt-get update && apt-get install -y iputils-ping procps lsof curl && \
    pip install --no-cache-dir -r /app/requirements.txt


CMD ["bash"]

