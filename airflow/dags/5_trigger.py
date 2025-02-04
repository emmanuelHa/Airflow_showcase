# if you have 100 sensors running concurrently you will require 100 worker slots 
# on the other hand trigger process operates in an asynchronous mode
# This means that a single lightweight trigger process can efficiently manage all 
# 100 sensors simultaneously without blocking each other 
# The task can or not occupy an available worker slot. You can check that looking at Admin/Pools.
# Instead a task can delegate to a trigger that you can cehck looking at Broswer/Triggers
# Not all sensors or operators are deferable
# SO USE DEFERABLE OPERATORS OR TRIGGERS!
# Verify the documentation of a specific operator to see if it has the deferable 
# parameter. See: https://registry.astronomer.io/providers/apache-airflow-providers-amazon/versions/9.0.0/modules/S3KeySensor

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator

dag = DAG(
    's3_to_snowflake_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False
)

# Wait for the file in S3
wait_for_file = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='etl-data',
    bucket_key='oms/employee_details.csv',
    aws_conn_id='aws_conn',
    poke_interval=60 * 10,
    mode="reschedule", # or poke by default # with reshedule mode worker slots are released and reallocated only 
    # when the sensor checks for the file availability, rather than holding the worker slot for the entire execution duration of the task
    timeout= 60 * 60 * 5,
    soft_fail=True,
    deferrable=True,
    dag=dag
)

# Parameter       | Default Value              #
# ---------------------------------------------#
# poke_interval   | 60 Seconds                 #
# mode            | poke                       #
# timeout         | 7 days (60 * 60 * 24 * 7)  #
# soft_fail       | False                      #

# Load the file from S3 to Snowflake
load_table = CopyFromExternalStageToSnowflakeOperator(
    task_id="load_s3_file_to_table",
    snowflake_conn_id="snowflake_conn",
    files=["employee_details.csv"],
    table="SLEEKMART_OMS.L1_LANDING.employee_details",
    stage='my_s3_stage',
    file_format="(type = 'CSV',field_delimiter = ',', skip_header = 1)",
    dag=dag
)

# Set the dependencies
wait_for_file >> load_table


# MOST POPULAR SENSORS ARE:
# SqlSensor
# DateTimeSensor
# HttpSensor
# ExternalTaskSensor
# BigQueryTableExistenceSensor
