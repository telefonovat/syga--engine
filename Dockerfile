FROM python:3.8

WORKDIR /app

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main files
COPY ./src ./src

# Create necessery directories and files
RUN mkdir -p ./logs/algs
# touch ./io/input.json ./io/output.json

# Clear cache and logs
COPY ./bin/clear.sh ./bin/clear.sh
RUN ./bin/clear.sh && rm -rf ./bin

CMD ["python3", "src/main.py"]
