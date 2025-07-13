{{ config(materialized='table') }}

SELECT DISTINCT
    channel_name AS channel_id,
    channel_name,
    NULL AS location
FROM {{ ref('stg_telegram_messages') }}
