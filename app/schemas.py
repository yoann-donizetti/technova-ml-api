from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=0)
    genre: str
    revenu_mensuel: int = Field(..., ge=0)
    statut_marital: str
    departement: str
    poste: str
    nombre_experiences_precedentes: int = Field(..., ge=0)
    annees_dans_l_entreprise: int = Field(..., ge=0)

    satisfaction_employee_environnement: int = Field(..., ge=0)
    satisfaction_employee_nature_travail: int = Field(..., ge=0)
    satisfaction_employee_equipe: int = Field(..., ge=0)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=0)

    heure_supplementaires: bool

    augmentation_salaire_precedente: int = Field(..., ge=0)
    nombre_participation_pee: int = Field(..., ge=0)
    nb_formations_suivies: int = Field(..., ge=0)
    distance_domicile_travail: int = Field(..., ge=0)

    niveau_education: int = Field(..., ge=0)
    domaine_etude: str
    frequence_deplacement: str

    ratio_manager_anciennete: float
    mobilite_relative: float
    evolution_performance: int
    pression_stagnation: float


class PredictionResponse(BaseModel):
    proba: float
    prediction: int
    threshold: float