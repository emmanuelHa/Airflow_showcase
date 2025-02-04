# Showcase of few functionalities of Airflow

## Introduction 
In this project, you will go through some concepts:
- how to install and run airflow on your machine,
- DAGs, Operators, Tasks, Providers,
- Variables and Connections,
- Sensors,
- Deferrable Operators & Triggers,
- Xcom | How to Pass data between tasks,
- Hooks vs Operators,
- Datasets and data-aware scheduling | Cross-DAG Dependencies,
- Trigger Rules, Conditional Branching, Setup Teardown, Latest Only, Depends On Past,
- Airflow Taskflow API | Airflow Decorators


## Technology Used
Airflow without astronomer

## How to test ?
- To run those examples you will need a docker engine like Docker Desktop to run docker containers through docker compose.
- If you use VScode as an IDE, you can just right click on docker-compose.yml file and select "compose up"
- Wait for the containers to be up
- Go through the logs of the webserver container and search for "password" to login in the login page of airflow.   
The user is 'admin' and the password is automatically generated
- Go to: http://localhost:8080/login

Enter admin/the generated password from the logs
- You should be good to go :=)

## Notes:
The metadata database was not changed. It is SQLite. 
It is only for dev purpose!
Don't forget to compose down once done.

