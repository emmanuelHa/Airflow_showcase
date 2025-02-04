from airflow import DAG, Dataset
from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator
from airflow.utils.dates import days_ago
from airflow.models import Variable

# Data aware Scheduling: Airflow enables execution of dags based on the availability of files or datasets
# Used for example for Producer-Consumer Use cases
# With that you can easily implement Cross Dag dependencies
# Cross Dag dependencies: if your dags don't depend on files, you can create a dependency between dags defining a dummy dataset
# data set operate without using worker slots so it is more efficient. A key distinction with sensors or triggers
 

dag = DAG(
    "data_producer_dag",
    default_args={"start_date": days_ago(1)},
    schedule_interval="0 23 * * *",
)

http_to_s3_task = HttpToS3Operator(
    task_id="data_producer_task",
    endpoint=Variable.get("web_api_key"),
    s3_bucket="etl-data",
    s3_key="oms/xrate.json",
    aws_conn_id="aws_conn",
    http_conn_id=None,
    replace=True,
    dag=dag,
    outlets=[Dataset("s3://etl-data/oms/xrate.json")]
)