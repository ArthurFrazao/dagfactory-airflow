# Deploy Apache Airflow using Docker Compose and Local Executor

## Quick Access
- [Requirements](#requirements)
- [Set Up Airflow](#set-up-airflow)
  - [Step 1: Create a Project Directory](#step-1-create-a-project-directory)
  - [Step 2: Download Docker Compose YAML File from official Apache Airflow repository on GitHub](#step-2-download-docker-compose-yaml-file-from-official-apache-airflow-repository-on-github)
  - [Step 3: Create the volumes folder that will be mounted inside the container](#step-3-create-the-volumes-folder-that-will-be-mounted-inside-the-container)
  - [Step 4: Create the files that will be used in Docker Compose](#step-4-create-the-files-that-will-be-used-in-docker-compose)
  - [Step 5: Edit Docker Compose file](#step-5-edit-docker-compose-file)
  - [Step 6: Edit Dockerfile](#step-6-edit-dockerfile)
  - [Step 7: Edit requirements file](#step-7-edit-requirements-file)
  - [Step 8: Set Up Airflow Init](#step-8-set-up-airflow-init)
  - [Step 9: Run Docker Compose](#step-9-run-docker-compose)
  - [Step 10: Access Airflow Web App](#step-10-access-airflow-web-app)
- [Dag Factory](#dag-factory)

## Requirements

* Install [Docker](https://www.docker.com/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

## Set Up Airflow

### Step 1: Create a Project Directory

Organize your project by creating a directory of your own. This step will help keep your files organized and easy to manage.

Replace `project_name` with your preference below

```bash
mkdir <project_name>
cd <project_name>
```

### Step 2: Download Docker Compose YAML File from official Apache Airflow repository on GitHub

Replace `version` with your preference below. **This project uses version 2.9.3**.

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/<version>/docker-compose.yaml'
```

Or

Go to the [direct link](https://github.com/apache/airflow/blob/main/docs/apache-airflow/howto/docker-compose/docker-compose.yaml) to the Apache Airflow repository on GitHub and download it manually, remembering to move the downloaded file into the `project_name` folder created in step 1.


### Step 3: Create the volumes folder that will be mounted inside the container

```bash
mkdir -p ./dags ./logs ./plugins ./config
```

### Step 4: Create the files that will be used in Docker Compose

```bash
touch Dockerfile requirements.txt .env
```

- `Dockerfile:`

This file is used to create a custom airflow image

- `requirements.txt`

This file is used to add new Python libraries to be used in Airflow.

- `.env`

This file is used to store sensitive airflow information.

### Step 5: Edit Environment Variable file

Run the following command:

- Run this command: `echo -e "AIRFLOW_UID=$(id -u)" > .env`

Some settings used in yaml as sensitive data can be stored in an `.env` file and used as environment variables in the Docker Compose file

In this project we will define the following variables:

- `POSTGRES_USER`

This variable specifies the user name of the Airflow metadata database administrator.

- `POSTGRES_PASSWORD`

This variable specifies the password of the airflow metadata database administrator

- `POSTGRES_DB`

This variable specifies the database name of the airflow metadata database

- `_AIRFLOW_WWW_USER_USERNAME`

This variable specifies the username for the administrator account to access the Airflow web interface.

- `_AIRFLOW_WWW_USER_PASSWORD`

This variable specifies the password for the administrator account used to access the Airflow web interface.

- `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`

This variable specifies how often (in seconds) the DAGs directory should be scanned for new files

- `AIRFLOW_PROJ_DIR`

This variable specifies the project directory for Airflow inside the container. It is set to the current directory (.)

- `AIRFLOW__CORE__EXECUTOR`

Specifies the executor as `LocalExecutor`

Customize the variables to your specific needs, but remember to modify the Docker Compose file.

### Step 6: Edit Dockerfile

```Dockerfile
FROM apache/airflow:<version>

ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt requirements.txt

USER airflow

RUN pip install -U -r requirements.txt

EXPOSE 8080

WORKDIR ${AIRFLOW_HOME}
```

### Step 7: Edit requirements file

In this project we will use the following libraries. Feel free to add any libraries you need

```requirements
apache-airflow-providers-mysql
```

### Step 8: Edit Docker Compose file

Make the following changes in `docker-compose-yaml`:

- Comment this line: `#image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:<version>}`
- Uncomment this line: `build: .`

It should look like this.

```yaml
#image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:<version>}
build: .
```

### Step 9: Set Up Airflow Init

Run the following command to start Apache Airflow instance:

```
sudo docker compose up airflow-init
```

### Step 10: Run Docker Compose

With the configuration in place, run the following command to start Apache Airflow using Docker Compose:

```
sudo docker compose up
```

This command starts the Airflow services. If you wish, you can run it in the background by adding the `-d` flag to the command. Wait a moment for the configuration to complete.

It should look like this.

```
sudo docker compose up -d
```

### Step 11: Access Airflow Web App

Once the containers are up and running, open your web browser and navigate to `http://localhost:8080`. You'll be greeted with the Apache Airflow login page. Log in to Apache Airflow with this account

Use the values of the following variables defined in the .env files

- Username: `<_AIRFLOW_WWW_USER_USERNAME>`

- Password: `<_AIRFLOW_WWW_USER_PASSWORD>`

## Dag Factory
