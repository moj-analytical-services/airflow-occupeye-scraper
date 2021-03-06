from .transform_data import (
    get_surveys_df,
    get_sensor_dimension_df,
    get_survey_fact_df,
)
from dataengineeringutils import s3
import logging

logger = logging.getLogger(__name__)


def surveys_to_s3(surveys):
    df = get_surveys_df(surveys)
    bucket = "alpha-dag-occupeye"
    path = f"raw_data_v5/surveys/data.csv"
    df.to_csv("myfile.csv", index=False)
    s3.upload_file_to_s3_from_path("myfile.csv", bucket, path)
    s3.upload_file_to_s3_from_path(
        "myfile.csv", "alpha-app-occupeye-automation", path
    )


def sensor_dimension_to_s3(sensor_dimension):
    if sensor_dimension is None:
        logger.info("No dimension data found for this sensor")
        return None
    surveyid = sensor_dimension[0]["SurveyID"]
    df = get_sensor_dimension_df(sensor_dimension)
    bucket = "alpha-dag-occupeye"
    path = f"raw_data_v5/sensors/survey_id={surveyid}/data.csv"
    df.to_csv("myfile.csv", index=False)
    s3.upload_file_to_s3_from_path("myfile.csv", bucket, path)
    s3.upload_file_to_s3_from_path(
        "myfile.csv", "alpha-app-occupeye-automation", path
    )


def survey_fact_to_s3(survey_facts, survey, date_string):
    if survey_facts is None:
        logger.info("No fact data found for this survey")
        return None

    df_survey_fact = get_survey_fact_df(survey_facts)

    # Note compression arg only used when first arg is filename
    # pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
    df_survey_fact.to_csv(
        "temp_df_for_upload.csv.gz", index=False, compression="gzip"
    )
    bucket = "alpha-dag-occupeye"
    path = (
        f"raw_data_v5/sensor_observations/"
        f"survey_id={survey['SurveyID']}/{date_string}.csv.gz"
    )
    s3.upload_file_to_s3_from_path("temp_df_for_upload.csv.gz", bucket, path)
    s3.upload_file_to_s3_from_path(
        "temp_df_for_upload.csv.gz", "alpha-app-occupeye-automation", path
    )
