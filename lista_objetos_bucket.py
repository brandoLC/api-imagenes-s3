import boto3
import json

def lambda_handler(event, context):
    """
    Lista objetos de un bucket específico
    """
    try:
        # Parsear el body si viene como string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        nombre_bucket = body.get('bucket')
        prefijo = body.get('prefijo', '')  # Para filtrar por directorio
        
        if not nombre_bucket:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Falta el parámetro bucket'
                })
            }
        
        s3 = boto3.client('s3')
        
        # Listar objetos
        kwargs = {'Bucket': nombre_bucket}
        if prefijo:
            kwargs['Prefix'] = prefijo
        
        response = s3.list_objects_v2(**kwargs)
        
        objetos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                # Construir URL pública
                objeto_url = f"https://{nombre_bucket}.s3.amazonaws.com/{obj['Key']}"
                
                objetos.append({
                    'key': obj['Key'],
                    'tamaño': obj['Size'],
                    'ultima_modificacion': obj['LastModified'].isoformat(),
                    'etag': obj['ETag'],
                    'url_publica': objeto_url
                })
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'bucket': nombre_bucket,
                'prefijo': prefijo,
                'objetos': objetos,
                'total': len(objetos)
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
                'mensaje': 'Error al listar objetos del bucket'
            })
        }
