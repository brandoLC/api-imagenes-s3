import boto3
import json

def lambda_handler(event, context):
    """
    Lista todos los buckets de S3
    """
    try:
        s3 = boto3.client('s3')
        
        # Listar buckets
        response = s3.list_buckets()
        
        buckets = []
        for bucket in response['Buckets']:
            buckets.append({
                'nombre': bucket['Name'],
                'fecha_creacion': bucket['CreationDate'].isoformat()
            })
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({
                'buckets': buckets,
                'total': len(buckets)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({
                'error': str(e),
                'mensaje': 'Error al listar buckets'
            })
        }
