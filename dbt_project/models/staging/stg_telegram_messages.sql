{{ config(materialized='view') }}

SELECT
    message_id,
    channel_name,
    message_text,
    CAST(message_date AS DATE) AS message_date,
    has_image,
    LENGTH(message_text) AS message_length
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_text IS NOT NULL
