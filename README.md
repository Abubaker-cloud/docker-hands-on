# Docker Hands-On: Flask and MySQL

## Project Overview

This project demonstrates how to containerize a Python Flask application and run it alongside a MySQL database using Docker Compose.

It covers Docker images, containers, service communication, persistent storage, environment variables, health checks, and troubleshooting.

## Technologies Used

* Docker
* Docker Compose
* Python 3.12
* Flask
* Gunicorn
* MySQL 8.4
* Git and GitHub

## Project Architecture

The project contains two services:

* **app:** Runs the Flask application using Gunicorn.
* **db:** Runs the MySQL database.

Docker Compose manages both services and connects them through an internal network. The Flask application uses the service name `db` to connect to MySQL.

A named volume stores database files persistently.

## Project Structure

```text
docker-hands-on/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
├── README.md
└── app/
    ├── app.py
    └── requirements.txt
```

## Prerequisites

Install the following tools:

* Docker
* Docker Compose
* Git

## Environment Variables

Create a `.env` file in the project root directory:

```dotenv
DB_PASSWORD=ReplaceWithYourAppPassword
MYSQL_ROOT_PASSWORD=ReplaceWithYourRootPassword
```

Replace these example values with strong passwords before running the project.

**Security:** Never commit `.env` or real credentials to GitHub. Ensure `.env` is included in `.gitignore`.

## Build and Run

Build the application image and start the services:

```bash
docker compose up -d --build
```

## Check Service Status

```bash
docker compose ps
```

Wait until the MySQL service passes its health check.

## Access the Application

Open the following URL in your browser:

http://localhost:5000

The response depends on the Flask routes implemented in `app/app.py`.

## View Application Logs

Display application logs:

```bash
docker compose logs app
```

Follow application logs continuously:

```bash
docker compose logs -f app
```

Display database logs:

```bash
docker compose logs db
```

## Persistent Storage

MySQL data is stored in the named volume `mysql_data`, mounted at `/var/lib/mysql`.

List Docker volumes:

```bash
docker volume ls
```

Inspect the project volume:

```bash
docker volume inspect docker-learning_mysql_data
```

The named volume helps preserve database data when containers are removed and recreated.

**Warning:** Avoid `docker compose down -v` unless you intentionally want to delete the project's managed volumes and their stored data.

## Troubleshooting

### 1. Port Already in Use

If port `5000` is already in use, change the host port in `compose.yaml`:

```yaml
ports:
  - "5001:5000"
```

Recreate the services:

```bash
docker compose up -d --build
```

Access the application at:

http://localhost:5001

### 2. Application Cannot Connect to MySQL

Check the application and database logs:

```bash
docker compose logs app
docker compose logs db
docker compose ps
```

Verify the database hostname, credentials, and health status.

Use `db` as the database hostname within the Docker Compose network.

### 3. Code Changes Are Not Visible

Rebuild the application image and recreate the services:

```bash
docker compose up -d --build
```

### 4. Database Health Check Fails

Inspect the database logs and container health information:

```bash
docker compose logs db
docker inspect mysql-db
```

Check the MySQL configuration, environment variables, and health check.

## Stop the Project

Stop and remove the project's containers and default network:

```bash
docker compose down
```

Named volumes are normally retained unless you explicitly request their removal.

## Skills Practiced

* Building Docker images using a Dockerfile
* Managing container lifecycles
* Orchestrating services with Docker Compose
* Configuring port mappings
* Using environment variables
* Container networking and service discovery
* Configuring MySQL health checks
* Managing persistent volumes
* Analyzing logs and troubleshooting issues
* Using Git for version control

## Author

Abubaker Abdallh

## Disclaimer

This is a hands-on learning project. Review security, configuration, and database connectivity before using it in production.

