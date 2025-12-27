
import pytest

# Payload valide pour /predict
PAYLOAD_OK = {
  "age": 41,
  "genre": "homme",
  "revenu_mensuel": 3993,
  "statut_marital": "célibataire",
  "departement": "commercial",
  "poste": "cadre commercial",
  "nombre_experiences_precedentes": 2,
  "annees_dans_l_entreprise": 5,
  "satisfaction_employee_environnement": 4,
  "satisfaction_employee_nature_travail": 1,
  "satisfaction_employee_equipe": 1,
  "satisfaction_employee_equilibre_pro_perso": 1,
  "heure_supplementaires": True,
  "augmentation_salaire_precedente": 11,
  "nombre_participation_pee": 0,
  "nb_formations_suivies": 0,
  "distance_domicile_travail": 1,
  "niveau_education": 2,
  "domaine_etude": "infra & cloud",
  "frequence_deplacement": "occasionnel",
  "annees_sous_responsable_actuel": 0,
  "annees_dans_le_poste_actuel": 0,
  "note_evaluation_actuelle": 0,
  "note_evaluation_precedente": 0,
  "annees_depuis_la_derniere_promotion": 0
}


# -------------------------------------------------------------------
# Utilitaire : injecter un état minimal dans l'app (pas de HF / pas de DB)
# -------------------------------------------------------------------
def _inject_dummy_state():
    from app.main import app

    class DummyModel:
        def predict_proba(self, X):
            return [[0.2, 0.8]]  # proba classe 1

    app.state.model = DummyModel()
    app.state.threshold = 0.292
    app.state.engine = None


# =========================
# /predict (POST)
# =========================
def test_post_predict_unauthorized_without_api_key(client):
    r = client.post("/predict", json=PAYLOAD_OK)
    assert r.status_code == 401


def test_post_predict_unauthorized_with_wrong_api_key(client):
    r = client.post(
        "/predict",
        json=PAYLOAD_OK,
        headers={"X-API-Key": "WRONG"},
    )
    assert r.status_code == 401


def test_post_predict_ok_with_api_key(client, auth_headers):
    _inject_dummy_state()

    r = client.post("/predict", json=PAYLOAD_OK, headers=auth_headers)
    assert r.status_code == 200, r.text

    body = r.json()
    assert body["threshold"] == 0.292
    assert body["prediction"] in (0, 1)
    assert "proba" in body


# =========================
# /predict/{id} (GET)
# =========================
def test_get_predict_by_id_unauthorized_without_api_key(client):
    r = client.get("/predict/7")
    assert r.status_code == 401


def test_get_predict_by_id_unauthorized_with_wrong_api_key(client):
    r = client.get("/predict/7", headers={"X-API-Key": "WRONG"})
    assert r.status_code == 401


def test_get_predict_by_id_ok_with_api_key(client, auth_headers, monkeypatch):
    _inject_dummy_state()

    # IMPORTANT : patcher là où la fonction est importée (app.main)
    import app.main as main_module

    def fake_run_predict_by_id(*, id_employee, model, threshold, engine):
        return 0.55, 1, {"id_employee": id_employee}

    monkeypatch.setattr(main_module, "run_predict_by_id", fake_run_predict_by_id)

    r = client.get("/predict/7", headers=auth_headers)
    assert r.status_code == 200, r.text

    body = r.json()
    assert body["threshold"] == 0.292
    assert body["prediction"] in (0, 1)
    assert "proba" in body