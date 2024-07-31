from airflow import DAG
from importlib import import_module

import pendulum
import os 
import yaml 


def parse_date_parameters(dag_parameters):

    date_columns_list = [
        "start_date",
        "end_date",
        "retry_delay",
        "max_retry_delay",
        "sla",
        "execution_timeout",
        "dagrun_timeout"
    ]

    for param, value in dag_parameters.items():
        if param in date_columns_list:
            dag_parameters[param] = pendulum.parse(value, exact=True, strict=False)

            if isinstance(dag_parameters[param], pendulum.Time):
                dag_parameters[param] = pendulum.duration(
                    hours=dag_parameters[param].hour,
                    minutes=dag_parameters[param].minute,
                    seconds=dag_parameters[param].second
                )

    return dag_parameters


def create_tasks_flow_execution(dag_yaml):
    execution_parameter = dag_yaml.get("execution")
    if isinstance(execution_parameter, str):
        exec(execution_parameter)
    elif isinstance(execution_parameter, (list, tuple, set)):
        for command in execution_parameter:
            exec(command)


def create_task(task_name, task_config, dag, dag_id):

    operator = task_config["operator"]

    module = import_module(f"dagfactory.operators.{operator}Operator")
    class_name = f"Build{operator.capitalize()}Operator"
    class_operator = getattr(module, class_name)
    instance_operator = class_operator(task_name, task_config, dag, dag_id)

    task = instance_operator.create_tasks()

    return task


def create_dag(dag_yaml):
    
    dag_parameters                  = dag_yaml["dag"]
    dag_parameters                  = parse_date_parameters(dag_parameters)
    dag_parameters["default_args"]  = parse_date_parameters(dag_parameters["default_args"])
    dag_parameters["catchup"]       = dag_parameters.get("catchup", False)
    dag_parameters["description"]   = dag_parameters.get("description")
    dag_parameters["tags"]          = dag_parameters.get("tags", "no-tags")

    if "retries" not in dag_parameters["default_args"]:
        dag_parameters["default_args"]["retries"] = 0

    dag_id = dag_parameters["dag_id"]
    dag = DAG(**dag_parameters)

    task_mapper = {}

    for task_name, task_config in dag_yaml["tasks"].items():
        task = create_task(task_name, task_config, dag, dag_id)
        task_mapper[task.task_id] = task

    for task_name, operator in task_mapper.items():
        globals()["operator"] = operator
        exec(f"{task_name} = operator", globals())

    create_tasks_flow_execution(dag_yaml)

    return dag


def main():

    dags_directory_path = os.getenv("AIRFLOW__CORE__DAGS_FOLDER")

    for dag_folder in os.scandir(dags_directory_path):
        
        if dag_folder.is_dir():
            dag_yaml_path = os.path.join(dags_directory_path, dag_folder, "dag.yaml")

            if os.path.exists(dag_yaml_path) and os.path.isfile(dag_yaml_path):
                read_mode = "r"
                with open(dag_yaml_path, read_mode) as file:
                    dag_yaml = yaml.safe_load(file)
                    
                    dag_instance = create_dag(dag_yaml)

                    if dag_instance:
                        globals()[dag_folder] = dag_instance


main()