import boto3
import json
import base64
import uuid
from datetime import datetime

def lambda_handler(event, context):
    """
    Sube una imagen al bucket de farmacia y devuelve la URL pública
    """
    try:
        # Parsear el body si viene como string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Parámetros de entrada
        nombre_bucket = body.get('bucket', 'farmacia-imagenes-brandolc18')
        categoria = body.get('categoria', 'productos')  # productos, medicamentos, promociones
        nombre_archivo = body.get('nombre_archivo')
        contenido_archivo = body.get('contenido_archivo')  # Base64 encoded
        
        if not nombre_archivo or not contenido_archivo:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Faltan parámetros requeridos: nombre_archivo y contenido_archivo'
                })
            }
        
        # Generar nombre único para evitar colisiones
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        extension = nombre_archivo.split('.')[-1] if '.' in nombre_archivo else 'jpg'
        nombre_unico = f"{timestamp}_{unique_id}.{extension}"
        
        # Construir la key completa
        key = f"{categoria}/{nombre_unico}"
        
        # Proceso
        s3 = boto3.client('s3')
        
        # Decodificar el contenido del archivo desde base64
        try:
            contenido_decodificado = base64.b64decode(contenido_archivo)
        except Exception as decode_error:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
                },
                'body': json.dumps({
                    'error': f'Error al decodificar base64: {str(decode_error)}'
                })
            }
        
        # Determinar content type basado en la extensión
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'svg': 'image/svg+xml'
        }
        content_type = content_types.get(extension.lower(), 'image/jpeg')
        
        # Subir el archivo con ACL público
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=key,
            Body=contenido_decodificado,
            ContentType=content_type,
            ACL='public-read'  # Hace el archivo público
        )
        
        # Construir la URL pública
        imagen_url = f"https://{nombre_bucket}.s3.amazonaws.com/{key}"
        
        # Salida
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': json.dumps({
                'mensaje': f'Imagen subida exitosamente',
                'bucket': nombre_bucket,
                'categoria': categoria,
                'archivo_original': nombre_archivo,
                'archivo_subido': nombre_unico,
                'key': key,
                'imagen_url': imagen_url,  # Esta es la URL que necesitas para tu API de productos
                'etag': response['ETag'],
                'content_type': content_type,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': json.dumps({
                'error': str(e),
                'mensaje': 'Error al subir la imagen'
            })
        }
