FROM python:3.8

# Install cURL
RUN apt-get -y -qq update && \
  apt-get install -y -qq curl less && \
  apt-get clean

# Install jq
RUN curl -o /usr/local/bin/jq http://stedolan.github.io/jq/download/linux64/jq && \
  chmod +x /usr/local/bin/jq

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "src/main.py"]
