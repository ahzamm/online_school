FROM python:3.9-alpine3.13
WORKDIR /online_school
COPY . .
RUN pip install -r requirements.txt && rm requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]