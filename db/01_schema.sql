-- =====================================================
-- Création des schémas du projet Technova ML API
-- =====================================================

-- Schéma pour les données brutes (RAW)
CREATE SCHEMA IF NOT EXISTS raw;

-- Schéma pour les données nettoyées / intermédiaires
CREATE SCHEMA IF NOT EXISTS staging;

-- Schéma pour les données finales utilisées par le modèle
CREATE SCHEMA IF NOT EXISTS mart;

-- Schéma pour l’audit et la traçabilité (API, prédictions)
CREATE SCHEMA IF NOT EXISTS audit;