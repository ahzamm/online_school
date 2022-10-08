FROM python:3.9-alpine3.13
ENV PYTHONUNBUFFERED=1
WORKDIR /online_school_project
COPY . .
COPY .git .
RUN pip install -r requirements.txt && rm requirements.txt
