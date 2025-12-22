import os
from fastapi.testclient import TestClient
from app.main import app
import numpy as np

os.environ["TESTING"] = "1"
client = TestClient(app)




class DummyModel:
    def predict_proba(self, X):
        return np.array([[0.7, 0.3]])


def test_predict_ok():
    client.app.state.model = DummyModel()
    client.app.state.threshold = 0.292

    payload = {
        "age": 41,
        "genre": "Homme",
        "revenu_mensuel": 3000,
        "statut_marital": "Célibataire",
        "departement": "Sales",
        "poste": "Sales Executive",
        "nombre_experiences_precedentes": 2,
        "annees_dans_l_entreprise": 5,
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "heure_supplementaires": True,
        "augmentation_salaire_precedente": 12,
        "nombre_participation_pee": 2,
        "nb_formations_suivies": 1,
        "distance_domicile_travail": 10,
        "niveau_education": 3,
        "domaine_etude": "Life Sciences",
        "frequence_deplacement": "Travel_Rarely",
        "ratio_manager_anciennete": 0.5,
        "mobilite_relative": 0.2,
        "evolution_performance": 3,
        "pression_stagnation": 0.1
    }

    r = client.post("/predict", json=payload)
    assert r.status_code == 200, r.text