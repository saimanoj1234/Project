#!/usr/bin/env python
# coding: utf-8

# What is Airflow?
## Used to schedule , monitor workflows and data pipelines
# What is Airflow Scheduler?
## The Scheduler always checks on your tasks and starts new ones when needed, based on their order and schedules.
# What is Airflow Webserver?
## The Webserver is like a window into Airflow’s world. It’s a website that makes it easy for you to see and manage your DAGs. With the Webserver, you can check on your tasks, start them manually, and even fix problems in your pipelines.


# In[ ]:


from airflow import DAG

from airflow.operators.dummy_operator import  DummyOperator
from airflow.operators.bash import  BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
def my():
    print("hi manoj")
    
# DAG OBJECT
with DAG(dag_id = "hello_world_dag",start_date = datetime(2023,1,1),
    schedule_interval="@hourly",catchup=False) as dag:
        task1 = DummyOperator(task_id = "start")
        task2 = BashOperator(task_id ="bashtask",bash_command = " echo hello world")
        task3 = PythonOperator(task_id ="pythontask",python_callable = my )
        task4 = DummyOperator(task_id = "end")

        
# Set up task dependencies
task1 >> task2 >> task3 >> task4

