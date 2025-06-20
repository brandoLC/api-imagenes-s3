# 🚀 API Imágenes S3 Farmacia - Ejemplos de Uso

## Base URL

```
https://j2yptao3bf.execute-api.us-east-1.amazonaws.com/dev
```

## 1. 🏗️ Crear Bucket Farmacia

**POST** `/s3/crear-bucket-farmacia`

```json
{
  "message": "Crear bucket específico para farmacia"
}
```

**Respuesta Esperada:**

```json
{
  "mensaje": "Bucket para farmacia creado exitosamente",
  "bucket_creado": "farmacia-imagenes-brandolc18",
  "bucket_url": "https://farmacia-imagenes-brandolc18.s3.amazonaws.com",
  "directorios_creados": ["productos/", "medicamentos/", "promociones/"]
}
```

---

## 2. ⭐ Subir Imagen Farmacia (PRINCIPAL)

**POST** `/s3/subir-imagen-farmacia`

### Para probar con imagen real:

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "categoria": "productos",
  "nombre_archivo": "paracetamol.jpg",
  "contenido_archivo": "AQUI_VA_TU_IMAGEN_EN_BASE64"
}
```

### Para prueba rápida (imagen mínima):

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "categoria": "productos",
  "nombre_archivo": "test.jpg",
  "contenido_archivo": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A"
}
```

**⚡ Respuesta IMPORTANTE (URL para tu API de productos):**

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

**💡 La URL `imagen_url` es la que guardas en tu base de datos de productos!**

---

## 3. 📋 Listar Buckets

**GET** `/s3/lista-buckets`

Sin body, solo GET request.

---

## 4. 📂 Listar Objetos del Bucket

**POST** `/s3/bucket/lista-objetos`

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "prefijo": "productos/"
}
```

**Respuesta:**

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "prefijo": "productos/",
  "objetos": [
    {
      "key": "productos/20250620_143022_a1b2c3d4.jpg",
      "tamaño": 45632,
      "ultima_modificacion": "2025-06-20T14:30:22.000Z",
      "etag": "\"abc123def456\"",
      "url_publica": "https://farmacia-imagenes-brandolc18.s3.amazonaws.com/productos/20250620_143022_a1b2c3d4.jpg"
    }
  ],
  "total": 1
}
```

---

## 5. 📁 Crear Directorio

**POST** `/s3/crear-directorio`

```json
{
  "bucket": "farmacia-imagenes-brandolc18",
  "directorio": "nuevos-productos"
}
```

---

## 🎯 Categorías Disponibles:

- `productos` - Productos farmacéuticos generales
- `medicamentos` - Medicamentos específicos
- `promociones` - Imágenes promocionales

## 🔄 Flujo para tu Ecommerce:

1. **Subir imagen** → Recibir `imagen_url`
2. **Guardar URL** en base de datos de productos
3. **Mostrar imagen** usando la URL en frontend

## 🌐 Convertir imagen a Base64:

```javascript
// En JavaScript (frontend)
const convertToBase64 = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      // Remover "data:image/jpeg;base64," del inicio
      const base64 = reader.result.split(",")[1];
      resolve(base64);
    };
    reader.readAsDataURL(file);
  });
};
```
