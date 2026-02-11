"""Sample AWS Lambda handlers for OCR/CDS offload."""

def ocr_worker(event, context):
    return {"statusCode": 200, "body": "OCR worker placeholder"}


def cds_worker(event, context):
    return {"statusCode": 200, "body": "CDS worker placeholder"}
