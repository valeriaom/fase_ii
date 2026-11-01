# Fase II | Portabilidad de nómina (MVP académico)

Prototipo de inferencia para analizar riesgo **sintético** de salida por portabilidad de nómina. No utiliza información de clientes reales y **no está validado para decisiones comerciales**.

## Requisitos

Python 3.11; Docker Desktop para ejecución de contenedor.

## Reproducción

```bash
python -m pip install -r requirements.txt
python -m training.pipeline
python -m pytest -q
uvicorn app.main:api --host 127.0.0.1 --port 8080
```

Interfaz: http://localhost:8080/ ; OpenAPI: http://localhost:8080/docs

## Contenedor

```bash
docker build -t portabilidad-demo:1.0 .
docker run --rm -p 8080:8080 portabilidad-demo:1.0
curl http://localhost:8080/health
```

## Estado de verificación

El entrenamiento y las pruebas de FastAPI se ejecutaron en el notebook. La construcción/ejecución Docker y el despliegue Cloud Run requieren validación adicional; no se consideran realizados solo por la presencia del Dockerfile.

## Arquitectura

Frontend HTML y JavaScript → FastAPI (`/health`, `/metadata`, `/predict`) → pipeline scikit-learn serializado. Datos y etiquetas sintéticos con semilla 42; selección por PR-AUC de validación; test separado. Los artefactos `joblib` deben proceder únicamente de fuentes confiables.

## Despliegue propuesto

Construir imagen, cargar en Google Artifact Registry y desplegar en Cloud Run con autenticación habilitada. Configurar IAM y comprobar endpoints antes de habilitar acceso. Consultar `docs/estado_validacion.md`.
