FROM python:3.7-alpine

WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 3000

CMD [ "python", "-m", "app" ]