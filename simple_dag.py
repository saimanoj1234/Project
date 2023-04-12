#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from airflow import DAG

from airflow.operators.dummy_operator import  DummyOperator
from airflow.operators.bash import  BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
def my():
    print("hi")
    
# DAG OBJECT
with DAG(dag_id = "hello_world_dag",start_date = datetime(2023,1,1),
    schedule_interval="@hourly",catchup=False) as dag:
        task1 = DummyOperator(task_id = "start")
        task2 = BashOperator(task_id ="bashtask",bash_command = " echo hello world")
        task3 = PythonOperator(task_id ="pythontask",python_callable = my )
        task4 = DummyOperator(task_id = "end")
task1 >> task2 >> task3 >> task4

