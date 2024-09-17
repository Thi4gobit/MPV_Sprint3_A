FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y tzdata
ENV TZ=America/Sao_Paulo

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
