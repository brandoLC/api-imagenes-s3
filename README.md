# API S3 para Farmacia - Gestión de Imágenes

Esta API está diseñada específicamente para gestionar imágenes de productos farmacéuticos en Amazon S3, proporcionando URLs públicas para su uso en aplicaciones de ecommerce.

## Características Principales

- ✅ **CORS habilitado** para cualquier origen
- ✅ **URLs públicas** automáticas al subir imágenes
- ✅ **Nombres únicos** para evitar colisiones
- ✅ **Categorización** automática de imágenes
- ✅ **Soporte múltiples formatos** de imagen

## Endpoints Disponibles

### 1. Crear Bucket para Farmacia

**POST** `/s3/crear-bucket-farmacia`

Crea un bucket específico para imágenes de farmacia con configuración pública.

```json
{
  "mensaje": "Bucket para farmacia creado exitosamente",
  "bucket_creado": "farmacia-imagenes-brandolc18",
  "bucket_url": "https://farmacia-imagenes-brandolc18.s3.amazonaws.com",
  "directorios_creados": ["productos/", "medicamentos/", "promociones/"]
}
```

### 2. Subir Imagen de Farmacia ⭐ **PRINCIPAL**

**POST** `/s3/subir-imagen-farmacia`

**Request:**

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "categoria": "productos",
  "nombre_archivo": "paracetamol.jpg",
  "contenido_archivo": "base64_encoded_image_data"
}
```

**Response:**

```json
{
  "mensaje": "Imagen subida exitosamente",
  "bucket": "farmacia-imagenes-brandolc18",
  "categoria": "productos",
  "archivo_original": "paracetamol.jpg",
  "archivo_subido": "20250620_143022_a1b2c3d4.jpg",
  "key": "productos/20250620_143022_a1b2c3d4.jpg",
  "imagen_url": "https://farmacia-imagenes-brandolc18.s3.amazonaws.com/productos/20250620_143022_a1b2c3d4.jpg",
  "etag": "\"abc123def456\"",
  "content_type": "image/jpeg",
  "timestamp": "20250620_143022"
}
```

### 3. Listar Buckets

**GET** `/s3/lista-buckets`

### 4. Listar Objetos del Bucket

**POST** `/s3/bucket/lista-objetos`

**Request:**

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "prefijo": "productos/"
}
```

### 5. Crear Directorio

**POST** `/s3/crear-directorio`

## Categorías Disponibles

- `productos/` - Imágenes de productos farmacéuticos generales
- `medicamentos/` - Imágenes de medicamentos específicos
- `promociones/` - Imágenes para promociones y ofertas

## Formato de Imagen Soportados

- JPG/JPEG
- PNG
- GIF
- WebP
- SVG

## Integración con API de Productos

### Ejemplo de uso en tu API de productos:

```javascript
// 1. Subir imagen a S3
const subirImagen = async (archivoImagen) => {
  const base64 = await convertirABase64(archivoImagen);

  const response = await fetch(
    "https://tu-api-s3.com/s3/subir-imagen-farmacia",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        categoria: "productos",
        nombre_archivo: archivoImagen.name,
        contenido_archivo: base64,
      }),
    }
  );

  const data = await response.json();
  return data.imagen_url; // Esta URL la guardas en tu base de datos
};

// 2. Crear producto con URL de imagen
const crearProducto = async (producto, archivoImagen) => {
  // Primero subir imagen
  const imagenUrl = await subirImagen(archivoImagen);

  // Luego crear producto con la URL
  const nuevoProducto = {
    ...producto,
    imagen: imagenUrl, // Campo imagen con URL de S3
  };

  await fetch("https://tu-api-productos.com/productos", {
    method: "POST",
    body: JSON.stringify(nuevoProducto),
  });
};
```

## Despliegue

```bash
# Instalar dependencias
npm install -g serverless
npm install

# Desplegar
serverless deploy
```

## Variables de Entorno

- `AWS_REGION`: us-east-1 (por defecto)
- Role IAM: `arn:aws:iam::248056481657:role/LabRole`

## Seguridad

- ✅ Bucket público solo para **lectura**
- ✅ Archivos públicos automáticamente
- ✅ CORS habilitado para todos los orígenes
- ✅ Nombres únicos con timestamp y UUID

---

**💡 Tip:** La URL que devuelve `imagen_url` es la que debes guardar en el campo imagen de tu API de productos farmacéuticos.
