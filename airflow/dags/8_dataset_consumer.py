# Imports
from airflow import DAG, Dataset
from airflow.utils.dates import days_ago
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

#  The consumer dag has schedule information presented as a dataset, instead of time-based scheduling details.
# And this dag will trigger automatically, whenever the producer dag or task completes successfully.
# As soon as producer dag is successful, it’s automatically triggered the consumer dag
# You can find more information about all datasets in your Airflow by checking the Datasets tab. 
# This includes details about when the dataset trigger was activated at different times
# You can also navigate to the 'Browse' section, and select dag dependencies', 
# to visualize all cross-dag dependencies in your Airflow environment 
# 

# Define the DAG
dag = DAG(
    'data_consumer_dag',
    default_args={'start_date': days_ago(1)},
    schedule=[Dataset("s3://etl-data/oms/xrate.json")], # on aurait pu dépendre de plusieurs dataset ici, séparés par des virgules

#   We usually code cron-based (or time based) schedule_interval as below:
#   schedule_interval="0 23 * * *",
)

# Define the Task
load_table = SnowflakeOperator(
    task_id='data_consumer_task',
    sql='./8_xrate_sf.sql',
    snowflake_conn_id='snowflake_conn',
    dag=dag
)