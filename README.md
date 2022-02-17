# Website

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Access Admin Panel](#Access-admin-panel)

## General info
Simple e-commerce website created with D-jango.

![1](https://user-images.githubusercontent.com/72651157/154443284-5777377c-2ddb-48e7-8f15-bdda17c3f72c.png)
![3](https://user-images.githubusercontent.com/72651157/154443288-44d6b32c-012c-40e9-971a-9caa704944ef.png)
![2](https://user-images.githubusercontent.com/72651157/154443286-52eb52b7-2c1d-45a7-8320-56106288ffd0.png)

## Technologies
Project is created with:
* Boostrap: 4.5
* Python: 3.9
* Django: 3.1.3!

## Setup
To run this project, install it locally using cmd/terminal:
(If you're using a mac, use python3 in the terminal)


1. Install python on your machine: https://www.python.org/

2. In cmd/terminal, check your pip version:
    ```python/python3 -m pip --version```

3. Upgrade your pip, if needed:
    ```python/python3 -m pip install -U pip```

4. To install django type:
    ```pip install django```
    
5. Move to the Project/website/ directory and run migrations to update the database: 
    ```python/python3 manage.py migrate```
    
5. Once you've done that, run the website locally, by typing this in:
    ```python/python3 manage.py runserver```

## Access Admin Panel
To access the admin panel, create a superuser in the console:
    ```python/python3 manage.py createsuperuser```

Admin page can be accesed on
    ```localhost:8000/admin```

Home page can be accesed on
    ```localhost:8000```
