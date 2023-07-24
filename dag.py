from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pyspark.sql import SparkSession

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG instance
dag = DAG(
    'mysql_to_hive_etl',
    default_args=default_args,
    schedule_interval=timedelta(hours=6),  # Adjust the schedule interval as needed
    catchup=False  # Set to False to skip backfilling for past intervals
)

# Define a function to execute the provided Python code
def execute_mysql_to_hive_etl():
    spark = SparkSession.builder.appName("Read from MySQL").config("spark.sql.warehouse.dir","/user/hive/warehouse").enableHiveSupport().getOrCreate()

    jdbcHostname = "savvients-classroom.cefqqlyrxn3k.us-west-2.rds.amazonaws.com"
    jdbcPort = 3306
    jdbcDatabase = "practical_exercise"
    jdbcUsername = "sav_proj"
    jdbcPassword = "authenticate"
    jdbcUrl = "jdbc:mysql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)

    connectionProperties = {
        "user": jdbcUsername,
        "password": jdbcPassword,
        "driver": "com.mysql.jdbc.Driver"
    }
    
    # Reading data from MySQL table 'user'
    df = spark.read.jdbc(url=jdbcUrl, table="user", properties=connectionProperties)
    df.write.mode("overwrite").saveAsTable("MANOJ.us")
    
    # Reading data from MySQL table 'activitylog'
    df2 = spark.read.jdbc(url=jdbcUrl, table="activitylog", properties=connectionProperties)
    df2.write.mode("overwrite").saveAsTable("MANOJ.ac")
    
    # Perform other operations and queries as per your requirements.
    
    spark.stop()

# Create a PythonOperator to execute the ETL job
etl_task = PythonOperator(
    task_id='execute_mysql_to_hive_etl',
    python_callable=execute_mysql_to_hive_etl,
    dag=dag
)

# Set task dependencies if needed.
# For example:
# task_2 = SomeOtherOperator(task_id='task_2', ...)
# etl_task >> task_2

# Continue adding other tasks and their dependencies as required.

# done