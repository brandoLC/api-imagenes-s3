import boto3
import json

def lambda_handler(event, context):
    """
    Crea un bucket específico para imágenes de farmacia con configuración pública
    """
    try:
        # Parsear el body si viene como string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Nombre fijo del bucket para farmacia
        nombre_bucket = "farmacia-imagenes-brandolc18"
        
        # Proceso
        s3 = boto3.client('s3')
        
        try:
            # Crear el bucket
            response = s3.create_bucket(Bucket=nombre_bucket)
            
            # PRIMERO: Desbloquear acceso público (necesario antes de aplicar política)
            s3.put_public_access_block(
                Bucket=nombre_bucket,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,        # Bloquear ACLs
                    'IgnorePublicAcls': True,       # Ignorar ACLs
                    'BlockPublicPolicy': False,     # Permitir políticas públicas
                    'RestrictPublicBuckets': False  # No restringir buckets públicos
                }
            )
            
            # SEGUNDO: Configurar política del bucket para lectura pública
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{nombre_bucket}/*"
                    }
                ]
            }
            
            # TERCERO: Aplicar la política del bucket
            s3.put_bucket_policy(
                Bucket=nombre_bucket,
                Policy=json.dumps(bucket_policy)
            )
            
            # Crear directorios base
            directorios_base = ['productos/', 'medicamentos/', 'promociones/']
            for directorio in directorios_base:
                s3.put_object(Bucket=nombre_bucket, Key=directorio)
            
            bucket_url = f"https://{nombre_bucket}.s3.amazonaws.com"
            
        except s3.exceptions.BucketAlreadyOwnedByYou:
            bucket_url = f"https://{nombre_bucket}.s3.amazonaws.com"
        except Exception as bucket_error:
            # Si el bucket ya existe pero no es nuestro, usar un nombre único
            import time
            timestamp = str(int(time.time()))
            nombre_bucket = f"farmacia-imagenes-brandolc18-{timestamp}"
            
            response = s3.create_bucket(Bucket=nombre_bucket)
            bucket_url = f"https://{nombre_bucket}.s3.amazonaws.com"
        
        # Salida
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': json.dumps({
                'mensaje': f'Bucket para farmacia creado exitosamente',
                'bucket_creado': nombre_bucket,
                'bucket_url': bucket_url,
                'directorios_creados': ['productos/', 'medicamentos/', 'promociones/']
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
                'mensaje': 'Error al crear el bucket para farmacia'
            })
        }
