from functools import lru_cache
from pathlib import Path
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, ConfigDict

BASE=Path(__file__).resolve().parents[1]
MODEL_DIR=BASE/'model'
api=FastAPI(title='MVP de portabilidad de nomina | Demostracion academica',version='1.0.0')

class Features(BaseModel):
    model_config=ConfigDict(extra='forbid')
    antiguedad_meses:int=Field(ge=0,le=180)
    saldo_promedio:float=Field(ge=0,le=1_000_000)
    variacion_dispersion:float=Field(ge=-1,le=1)
    num_productos:int=Field(ge=1,le=15)
    actividad_reciente:int=Field(ge=0,le=1)

@lru_cache
def artifacts():
    try:
        model=joblib.load(MODEL_DIR/'model.joblib')  # Artefacto de origen controlado
        meta=json.loads((MODEL_DIR/'model_metadata.json').read_text(encoding='utf-8'))
    except (OSError,ValueError,ImportError) as ex:
        raise RuntimeError('Artefactos no disponibles; ejecutar entrenamiento') from ex
    return model,meta

@api.get('/',include_in_schema=False)
def index():
    return FileResponse(BASE/'app'/'static'/'index.html')

@api.get('/health')
def health():
    try: _,meta=artifacts()
    except RuntimeError:
        raise HTTPException(status_code=503,detail='Modelo no disponible')
    return {'status':'ok','model_loaded':True,'model_version':meta['model_version']}

@api.get('/metadata')
def metadata():
    try: _,meta=artifacts()
    except RuntimeError:
        raise HTTPException(status_code=503,detail='Modelo no disponible')
    return {'model_version':meta['model_version'],'model_name':meta['model_name'],'features':meta['features'],
            'threshold':meta['threshold'],'scope':meta['scope']}

@api.post('/predict')
def predict(payload:Features):
    try: model,meta=artifacts()
    except RuntimeError:
        raise HTTPException(status_code=503,detail='Modelo no disponible')
    X=pd.DataFrame([payload.model_dump()],columns=meta['features'])
    probability=float(model.predict_proba(X)[0,1])
    level='alto' if probability>=.65 else 'medio' if probability>=.35 else 'bajo'
    return {'probabilidad_salida':round(probability,6),'nivel_riesgo':level,'requiere_revision':level!='bajo',
            'model_version':meta['model_version'],'aviso':'Estimacion sintetica demostrativa; no utilizar para decisiones sobre clientes'}
