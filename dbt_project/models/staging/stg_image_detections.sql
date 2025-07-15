{{ config(materialized='view') }}

SELECT
    message_id,
    label AS product_label,
    confidence,
    box AS bounding_box
FROM {{ source('raw', 'image_detections') }}
WHERE confidence > 0.5
