# **`ONLINE SCHOOL`** <img alt="Project stage: Development" src="https://img.shields.io/badge/Project%20Stage-Development-yellowgreen.svg" />

[![.github/workflows/checks.yml](https://github.com/AhzamAhmed6/online_school/actions/workflows/checks.yml/badge.svg)](https://github.com/AhzamAhmed6/online_school/actions/workflows/checks.yml) ![size](https://img.shields.io/github/languages/code-size/ahzamahmed6/online_school)


---

### **Introduction**
Welcome to the online school project! This project was developed using Python and the [Django](https://github.com/django/django) framework, with the [Django Rest Framework](https://github.com/encode/django-rest-framework) utilized for web API creation. The project employs a monolithic design approach and utilizes SQLite as the database system, which is the default database for Django.


### **User Roles**
The system accommodates three types of user accounts: administrator, teacher, and student.

### **Project Structure**
The online school project is comprised of two main components: the "Accounts" app, responsible for managing user-related functions such as authentication and authorization, and the "Classes" app, which manages class-related functions such as courses and classes.

### **API Endpoints**
The project features over 25 API endpoints, which are documented using the [Swagger](https://github.com/marcgibbons/django-rest-swagger) package.

### **Testing**
The codebase undergoes thorough testing using the Pytest package to ensure high quality and minimize the likelihood of errors.

### **Final Thoughts**
I hope you find the online school project useful and easy to use. If you have any questions or feedback, please don't hesitate to reach out. Thank you for choosing the online school project!

---

### **Code Coverage**
View the code coverage report [here](https://ahzamahmed6.github.io/code_cov/)

---

### **Getting Started**

You have the option to download and run the official [docker image](https://hub.docker.com/repository/docker/ahzam6/online_school) for the project, or follow the manual setup guidelines provided below:


#### **Requirements**

- python >= 3.6


#### **Steps to run the project manually:**

1. Clone the project to your local machine

2. Create a virtual environment using the [virtualenv](https://pypi.org/project/virtualenv/) package
    ```sh
    virtualenv .venv
    ```

3. Activate the virtual environment:
    ```sh
    source ./.venv/bin/activate
    ```

4. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5. Comment out the following [line](https://github.com/AhzamAhmed6/online_school/blob/d8c6c25112b14ff88e39ad88256c50245a75c193/online_school/accounts/models/student_models.py#L51) in the code.


6. Run the following commands in the root directory of the project:
    ```sh
    python3 src/manage.py makemigrations accounts
    python3 src/manage.py makemigrations classes
    python3 src/manage.py migrate
    ```

7. Uncomment the previously commented line in the code and then run these commands.
    ```sh
    python3 src/manage.py makemigrations accounts
    python3 src/manage.py migrate
    ```

8. To start the server, run:

    ```sh
    python3 src/manage.py runserver
    ```

- for api documentation, visit url http://localhost:8000/swagger/



### **Models Overview**

![alt text](https://github.com/AhzamAhmed6/online_school/blob/actions/models.png?raw=true)

---