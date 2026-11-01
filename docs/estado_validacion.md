# Estado de validación: 1 de noviembre de 2026

- Entrenamiento sobre 4,000 casos sintéticos: ejecutado.
- Regresión logística: PR-AUC de validación 0.273785.
- Test sintético de 800 casos: ROC-AUC 0.733214; PR-AUC 0.266867; precision 0.215753; recall 0.663158; F1 0.325581.
- Pruebas FastAPI TestClient: 13/13 aprobadas en el entorno del notebook.
- Docker build/run: aún no comprobado; usar Docker Desktop o consultar GitHub Actions.
- Cloud Run: aún no desplegado; se documenta como estrategia.
- Limitación: datos sintéticos, no extrapolables a clientes reales.
