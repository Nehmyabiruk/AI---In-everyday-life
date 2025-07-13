{{ config(materialized='table') }}

SELECT
    message_date AS date_id,
    message_date AS date,
    EXTRACT(DOW FROM message_date) AS day_of_week,
    EXTRACT(MONTH FROM message_date) AS month
FROM {{ ref('stg_telegram_messages') }}
