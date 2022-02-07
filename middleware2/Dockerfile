# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

WORKDIR /app

ENV FLASK_APP=meterologyApp2.py

ENV FLASK_ENV=development

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["flask", "run", "--host", "0.0.0.0","--port","5002"]