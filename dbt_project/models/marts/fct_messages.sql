{{ config(materialized='table') }}

SELECT
    m.message_id,
    m.channel_name AS channel_id,
    m.message_date AS date_id,
    m.message_text,
    m.message_length,
    m.has_image
FROM {{ ref('stg_telegram_messages') }} m
