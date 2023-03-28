FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3-pip

# copy the app folder into the container
COPY /app /app

# set the working directory to /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
