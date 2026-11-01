import pytest
from fastapi.testclient import TestClient
from app.main import api

client=TestClient(api)
BASE={'antiguedad_meses':48,'saldo_promedio':32000,'variacion_dispersion':-.15,'num_productos':4,'actividad_reciente':1}

def test_health():
    response=client.get('/health')
    assert response.status_code==200
    assert response.json()['model_loaded'] is True

def test_metadata():
    response=client.get('/metadata')
    assert response.status_code==200
    assert len(response.json()['features'])==5

def test_predict_deterministic():
    a=client.post('/predict',json=BASE)
    b=client.post('/predict',json=BASE)
    assert a.status_code==200 and a.json()==b.json()
    assert 0<=a.json()['probabilidad_salida']<=1

@pytest.mark.parametrize('changes',[{'antiguedad_meses':-1},{'saldo_promedio':-2},{'variacion_dispersion':1.1},{'num_productos':0},{'actividad_reciente':2},{'campo_extrano':1},{'antiguedad_meses':'desconocida'}])
def test_invalid_input(changes):
    assert client.post('/predict',json=BASE|changes).status_code==422

def test_missing_field():
    data=BASE.copy()
    data.pop('num_productos')
    assert client.post('/predict',json=data).status_code==422

def test_extreme_valid_values():
    for data in ({'antiguedad_meses':0,'saldo_promedio':0,'variacion_dispersion':-1,'num_productos':1,'actividad_reciente':0},
                 {'antiguedad_meses':180,'saldo_promedio':1_000_000,'variacion_dispersion':1,'num_productos':15,'actividad_reciente':1}):
        assert client.post('/predict',json=data).status_code==200

def test_frontend():
    assert 'Evaluar escenario' in client.get('/').text
