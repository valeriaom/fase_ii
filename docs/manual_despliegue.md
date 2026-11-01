# Manual técnico de despliegue | Fase II

## 1. Propósito y alcance
MVP académico de clasificación sobre datos sintéticos para demostrar la integración de un modelo de aprendizaje automático, una API REST y un frontend. No procesa datos de clientes ni es apto para decisiones bancarias.

## 2. Requisitos
Docker Desktop o Docker Engine; para ejecución sin contenedor, Python 3.11 con pip. Entorno de desarrollo con acceso a internet para instalar dependencias. CPU suficiente para entrenar 4,000 observaciones sintéticas. El puerto de aplicación es 8080.

## 3. Arquitectura
El formulario en `app/static/index.html` envía JSON mediante HTTP POST a `/predict`. FastAPI valida tipos y rangos con Pydantic, invoca el Pipeline scikit-learn y entrega probabilidad estimada, nivel de riesgo y aviso de limitación. `GET /health` comprueba carga de modelo y `GET /metadata` documenta versión, características y umbral.

## 4. Ejecutar sin Docker
```bash
git clone https://github.com/valeriaom/fase_ii.git
cd fase_ii
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m training.pipeline
python -m pytest -q
uvicorn app.main:api --host 127.0.0.1 --port 8080
```

Abrir `http://localhost:8080/` o `http://localhost:8080/docs`. Las pruebas realizadas en notebook no sustituyen esta validación en equipo local.

## 5. Construir y ejecutar contenedor
```bash
docker build -t portabilidad-demo:1.0 .
docker run --rm -p 8080:8080 --name portabilidad-demo portabilidad-demo:1.0
```
El Dockerfile instala dependencias, entrena reproduciblemente el artefacto sintético durante el build y ejecuta Uvicorn como usuario no privilegiado.

En otra terminal:
```bash
curl -i http://localhost:8080/health
curl -i http://localhost:8080/metadata
curl -i -X POST http://localhost:8080/predict \
  -H 'Content-Type: application/json' \
  -d '{"antiguedad_meses":48,"saldo_promedio":32000,"variacion_dispersion":-0.15,"num_productos":4,"actividad_reciente":1}'
```
Documentar salida de comandos, estado HTTP y capturas de navegador sin fabricar evidencias.

## 6. Propuesta de despliegue en Google Cloud Run
Se requiere proyecto GCP autorizado, facturación configurada, permisos IAM y Google Cloud CLI. Habilitar las APIs de Cloud Run y Artifact Registry. Crear un repositorio Docker en Artifact Registry. Configurar `gcloud auth login`, `gcloud config set project PROJECT_ID` y `gcloud auth configure-docker REGION-docker.pkg.dev`. Etiquetar la imagen `REGION-docker.pkg.dev/PROJECT_ID/REPO/portabilidad-demo:1.0`, enviarla con `docker push` y ejecutar:
```bash
gcloud run deploy portabilidad-demo \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPO/portabilidad-demo:1.0 \
  --region REGION \
  --no-allow-unauthenticated
```
Sustituir los marcadores de ejemplo. Validar acceso de una identidad autorizada y endpoint de salud. Mantener el acceso restringido. Estos pasos son una estrategia propuesta, no constancia de despliegue.

## 7. Operación, fallas y reversión
Si `/health` devuelve 503, revisar la generación y ruta del artefacto. Si falla Docker build, verificar logs de pip, acceso a imágenes base y arquitectura. Si `/predict` devuelve 422, revisar el JSON respecto al esquema en `/docs`. Para reversión en nube, restaurar una revisión previamente validada en Cloud Run. No registrar datos sensibles en logs ni subir credenciales al repositorio.

## 8. Limitaciones
Las salidas y métricas describen un generador sintético. No existe evidencia de capacidad real de predicción de portabilidad de nómina. Docker local y nube deben evaluarse y registrarse explícitamente antes de declarar la solución validada.
