FROM python:3.11.4

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["main.py"]