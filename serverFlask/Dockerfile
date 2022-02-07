# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

EXPOSE 20000

WORKDIR /app

ENV FLASK_APP=apiPoll.py

ENV FLASK_ENV=development

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0","--port","20000"]