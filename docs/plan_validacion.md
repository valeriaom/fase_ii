# Documento de validación y pruebas | Fase II

## Alcance
Las pruebas verifican integridad funcional y robustez técnica del MVP, no validez comercial del modelo. El artefacto se entrena con datos sintéticos reproducibles.

## Evidencia disponible
El notebook ejecutado por la estudiante reportó 13 pruebas aprobadas en TestClient y evaluación sobre 800 registros sintéticos. Métricas: ROC-AUC 0.733214, PR-AUC 0.266867, precisión 0.215753, recall 0.663158 y F1 0.325581. Son resultados de un experimento académico, no datos bancarios.

## Casos y resultados esperados
| ID | Prueba | Resultado esperado | Evidencia |
| --- | --- | --- | --- |
| API-01 | GET /health con artefacto disponible | HTTP 200, model_loaded=true | TestClient |
| API-02 | GET /metadata | HTTP 200 y 5 variables | TestClient |
| API-03 | POST /predict entrada válida | HTTP 200 y probabilidad entre 0 y 1 | TestClient |
| API-04 | Misma entrada repetida | Respuesta determinista | TestClient |
| VAL-01 | antiguedad_meses=-1 | HTTP 422 | TestClient |
| VAL-02 | saldo_promedio=-2 | HTTP 422 | TestClient |
| VAL-03 | variacion_dispersion=1.1 | HTTP 422 | TestClient |
| VAL-04 | num_productos=0 | HTTP 422 | TestClient |
| VAL-05 | actividad_reciente=2 | HTTP 422 | TestClient |
| VAL-06 | Campo desconocido | HTTP 422 | TestClient |
| VAL-07 | Tipo inválido | HTTP 422 | TestClient |
| VAL-08 | Campo obligatorio ausente | HTTP 422 | TestClient |
| LIM-01 | Valores extremos válidos | HTTP 200 | TestClient |
| UI-01 | GET / | HTTP 200 con formulario | TestClient |
| CTR-01 | Construcción docker build | Exit code 0 | Por comprobar en CI/local |
| CTR-02 | Contenedor iniciado | Puerto 8080 accesible | Por comprobar local |
| E2E-01 | Envío desde navegador | Respuesta visible coherente | Por comprobar en navegador |
| CLD-01 | Cloud Run protegido | Solo identidades autorizadas | No desplegado |

Nota: algunas verificaciones se agrupan en pruebas parametrizadas; el total de 13 corresponde a los casos recolectados por pytest, no a la cantidad de filas de esta matriz.

## Criterios de aceptación
El modelo debe cargarse sin errores; el contrato JSON debe validar las entradas; los endpoints deben responder de manera consistente y el contenedor debe iniciarse con instrucciones reproducibles. Toda excepción debe declararse como pendiente o fallida con evidencia.

## Interpretación académica
La precisión relativamente baja implica numerosas alertas incorrectas en el conjunto sintético. Los falsos negativos representan salidas no detectadas. No se debe optimizar la solución para clientes reales sin una evaluación sobre datos pertinentes, políticas de privacidad y supervisión humana.
