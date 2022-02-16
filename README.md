# Website

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Access Admin Panel](#Access-admin-panel)

## General info
Simple e-commerce website created with D-jango.

![1](https://user-images.githubusercontent.com/72651157/154280414-3c4bb09e-3a01-49bf-9e9e-fc32701f9e83.png)
![2](https://user-images.githubusercontent.com/72651157/154280487-6b45c510-d426-4630-a9b3-42d52c0acc08.png)


## Technologies
Project is created with:
* Boostrap: 4.5
* Python: 3.9
* Django: 3.1.3

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
