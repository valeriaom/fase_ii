"""Modelo demostrativo con datos exclusivamente sintéticos."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED=42
FEATURES=['antiguedad_meses','saldo_promedio','variacion_dispersion','num_productos','actividad_reciente']

def synthetic_data(n=4000,seed=SEED):
    rng=np.random.default_rng(seed)
    X=pd.DataFrame({
        'antiguedad_meses':rng.integers(0,181,n),
        'saldo_promedio':np.round(rng.lognormal(9.3,.85,n),2),
        'variacion_dispersion':rng.uniform(-.9,.6,n).round(4),
        'num_productos':rng.integers(1,8,n),
        'actividad_reciente':rng.integers(0,2,n)})
    linear=(-.75-.006*X.antiguedad_meses-.000015*X.saldo_promedio
            -1.9*X.variacion_dispersion-.24*X.num_productos-.45*X.actividad_reciente)
    prob=1/(1+np.exp(-np.clip(linear,-30,30)))
    X['salida']=rng.binomial(1,prob)
    return X

def train(output_dir='model',n=4000,seed=SEED):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    df=synthetic_data(n,seed);X=df[FEATURES];y=df['salida']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,stratify=y,random_state=seed)
    pre=ColumnTransformer([('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),FEATURES)])
    candidates={
        'regresion_logistica':LogisticRegression(max_iter=1000,random_state=seed,class_weight='balanced'),
        'random_forest':RandomForestClassifier(n_estimators=150,min_samples_leaf=8,random_state=seed,n_jobs=-1,class_weight='balanced')}
    X_fit,X_val,y_fit,y_val=train_test_split(X_train,y_train,test_size=.25,stratify=y_train,random_state=seed)
    validations={}
    for name,est in candidates.items():
        pl=Pipeline([('preprocess',pre),('classifier',est)])
        pl.fit(X_fit,y_fit);prob=pl.predict_proba(X_val)[:,1]
        validations[name]={'pr_auc':float(average_precision_score(y_val,prob)),'roc_auc':float(roc_auc_score(y_val,prob))}
    selected=max(validations,key=lambda k:validations[k]['pr_auc'])
    model=Pipeline([('preprocess',pre),('classifier',candidates[selected])])
    model.fit(X_train,y_train);prob=model.predict_proba(X_test)[:,1]
    pred=(prob>=.5).astype(int)
    scores={'roc_auc':float(roc_auc_score(y_test,prob)),'pr_auc':float(average_precision_score(y_test,prob)),
            'precision':float(precision_score(y_test,pred,zero_division=0)),
            'recall':float(recall_score(y_test,pred,zero_division=0)),
            'f1':float(f1_score(y_test,pred,zero_division=0)),
            'confusion_matrix':confusion_matrix(y_test,pred).tolist()}
    meta={'model_version':'1.0.0-demo','model_name':selected,'features':FEATURES,'seed':seed,
          'synthetic_samples':n,'test_samples':len(y_test),'class_prevalence':float(y.mean()),
          'threshold':.5,'validation':validations,'test_metrics':scores,
          'scope':'demostracion tecnica: datos sinteticos; no es un modelo bancario validado'}
    joblib.dump(model,out/'model.joblib')
    (out/'model_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    return model,meta,df

if __name__=='__main__':
    _,meta,_=train()
    print(json.dumps(meta,ensure_ascii=False,indent=2))
