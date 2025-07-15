from dagster import asset, define_asset_job, ScheduleDefinition, Definitions
import os

@asset
def scrape_telegram():
    os.system("python scripts/scrape_telegram.py")

@asset(deps=[scrape_telegram])
def load_to_postgres():
    os.system("python scripts/load_to_postgres.py")

@asset(deps=[scrape_telegram])
def process_images():
    os.system("python scripts/process_images.py")

@asset(deps=[load_to_postgres])
def run_dbt():
    os.system("dbt run --project-dir dbt_project")

@asset(deps=[run_dbt])
def start_api():
    os.system("uvicorn scripts.api:app --host 0.0.0.0 --port 8000")

pipeline_job = define_asset_job("kaim_pipeline", selection=["scrape_telegram", "load_to_postgres", "process_images", "run_dbt", "start_api"])
schedule = ScheduleDefinition(job=pipeline_job, cron_schedule="0 0 * * *")

defs = Definitions(assets=[scrape_telegram, load_to_postgres, process_images, run_dbt, start_api], schedules=[schedule])
