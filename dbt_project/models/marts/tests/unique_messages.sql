SELECT
    message_id,
    channel_name,
    message_date,
    COUNT(*) AS count
FROM {{ ref('fct_messages') }}
GROUP BY message_id, channel_name, message_date
HAVING COUNT(*) > 1
