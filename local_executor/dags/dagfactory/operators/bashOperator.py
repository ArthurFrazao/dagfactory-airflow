import os 
from airflow.operators.bash import BashOperator

class BuildBashOperator:
    def __init__(self, task_name, task_config, dag, dag_id):
        self.task_id = task_name
        self.dag = dag
        self.dag_id = dag_id
        self.task_config = task_config    
        self.bash_command = self.task_config.get("bash_command")
        self.file = self.task_config.get("file")
        self.env = self.task_config.get("env")
        
        if self.bash_command:
            self.command = self.bash_command
        elif self.file:
            self.command = f"bash {os.getenv('AIRFLOW__CORE__DAGS_FOLDER')}/{self.dag_id}/{self.file} "
        
    def create_tasks(self):
        bash_operator = BashOperator(
            task_id=self.task_id,         
            dag=self.dag, 
            bash_command=self.command,
            env=self.env
        )  
        return bash_operator