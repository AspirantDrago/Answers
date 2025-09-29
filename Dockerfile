FROM python:3.10.18-alpine3.22

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python3", "main.py"]
