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
        "genre": "homme",
        "revenu_mensuel": 3000,
        "statut_marital": "célibataire",
        "departement": "sales",
        "poste": "sales executive",
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
        "domaine_etude": "life sciences",
        "frequence_deplacement": "travel_rarely",

        # champs BRUTS nécessaires au calcul
        "annees_sous_responsable_actuel": 3,
        "annees_dans_le_poste_actuel": 2,
        "note_evaluation_actuelle": 4,
        "note_evaluation_precedente": 3,
        }

    r = client.post("/predict", json=payload)
    assert r.status_code == 200, r.text