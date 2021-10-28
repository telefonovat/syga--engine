FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
RUN mkdir -p ./logs/algs

COPY ./bin/clear.sh ./bin/clear.sh
RUN ./bin/clear.sh && rm -rf ./bin

CMD ["python3", "src/main.py"]
