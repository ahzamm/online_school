# **`ONLINE SCHOOL`** <img alt="Project stage: Development" src="https://img.shields.io/badge/Project%20Stage-Development-yellowgreen.svg" />

[![.github/workflows/checks.yml](https://github.com/AhzamAhmed6/online_school/actions/workflows/checks.yml/badge.svg)](https://github.com/AhzamAhmed6/online_school/actions/workflows/checks.yml) ![size](https://img.shields.io/github/languages/code-size/ahzamahmed6/online_school)

[**code coverage**](https://ahzamahmed6.github.io/code_cov/)

## Requirements

- python >= 3.6

## Steps to run Project

After cloning the project in to your local machine

- create virtual environment using [virtualenv](https://pypi.org/project/virtualenv/) package

```sh
virtualenv my_env
```

- activate virtual environment

```sh
source ./my_env/bin/activate
```

- install dependencies

```sh
pip install -r requirements.txt
```

- comment down [this line](https://github.com/AhzamAhmed6/online_school/blob/d8c6c25112b14ff88e39ad88256c50245a75c193/online_school/accounts/models/student_models.py#L51).
- run following commands in the root directory of project.

```sh
python3 online_school/manage.py makemigrations accounts
python3 online_school/manage.py makemigrations classes
python3 online_school/manage.py migrate
```

- uncomment [this line](https://github.com/AhzamAhmed6/online_school/blob/d8c6c25112b14ff88e39ad88256c50245a75c193/online_school/accounts/models/student_models.py#L51)

```sh
python3 online_school/manage.py makemigrations accounts
python3 online_school/manage.py migrate
```

- to runserver

```sh
python3 online_school/manage.py runserver
```

- for api documentation, visit url http://localhost:8000/swagger/
