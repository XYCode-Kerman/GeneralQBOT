FROM python:3.8.16-buster

WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry install

ENV QCLOUD_SECRET_ID=
ENV QCLOUD_SECRET_KEY=
ENV OPENAI_KEY=
ENV DOCKER_MODE=True

CMD [ "poetry", "run", "python", "main.py" ]
