import boto3
import json

def lambda_handler(event, context):
    """
    Crea directorios (carpetas) en un bucket
    """
    try:
        # Parsear el body si viene como string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        nombre_bucket = body.get('bucket')
        nombre_directorio = body.get('directorio')
        
        if not nombre_bucket or not nombre_directorio:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Faltan parámetros requeridos: bucket y directorio'
                })
            }
        
        # Asegurar que termine con /
        if not nombre_directorio.endswith('/'):
            nombre_directorio += '/'
        
        s3 = boto3.client('s3')
        
        # Crear directorio (folder) poniendo un objeto vacío
        s3.put_object(Bucket=nombre_bucket, Key=nombre_directorio)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'mensaje': f'Directorio {nombre_directorio} creado exitosamente en bucket {nombre_bucket}',
                'bucket': nombre_bucket,
                'directorio_creado': nombre_directorio
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': str(e),
                'mensaje': 'Error al crear el directorio'
            })
        }
