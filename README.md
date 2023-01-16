# EpicEvent API

***
This project is part of the python developer course on [Openclassrooms](http:/openclassrooms.com).

The goal is to create an API for a consulting company that allow users to:

- Create and update a client database
- Create and manage contracts and events realted to those clients.



***

* **[Setup](#Setup)**
  * [Virtual environment creation](#Create-a-virtual-environment)
  * [Database creation](#Create-the-database)
* **[Usage](#Usage)**
* **[API endpoints documentation](#Postman-Endpoints-documentation)**


## **Setup**

***

</br>
A Python installation is required.

Assuming a git installation, clone the repository using:

    $git clone git clone https://github.com/Chfrlt/P12_epicevent

</br>

### **Create a virtual environment**

</br>
> Following instructions are the ones recommanded for python 3.6 or greater. If your python installation is an earlier version, please consult the associated documentation.

Create a virtual environnement using:

    $python -m venv <env_name>

To activate it:

* On Windows:

        $env_name/Script/activate

* On Linux/Mac:

        $source env_name/bin/activate

Install the python dependencies using:

    $pip install -r requirements.txt

</br>

### **Create the database**

</br>

Install [PostgreSQL](https://www.postgresql.org/download).
Follow the [documentation](https://www.postgresql.org/) to run the server.

Create the database structure using:

    $python manage.py migrate    

## **Usage**

***

Launch the app using:

    $python manage.py runserver

To access the admin site:

> http://127.0.0.1:8000/admin

To create a superuser:
> python manage.py create superuser

## **Postman Endpoints documentation**

***

You can find a list of the endpoints & the associated documentation at this adress:

**[Link to the postman documentation](https://documenter.getpostman.com/view/23276936/2s8ZDU547U)**
