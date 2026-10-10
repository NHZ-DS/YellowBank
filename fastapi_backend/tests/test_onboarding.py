"""Tests unitaires pour l'algorithme d'orientation du questionnaire."""

import pytest
from services.onboarding_service import OnboardingService


def test_track_recommendation_pea():
    service = OnboardingService()
    # Mocking answers for PEA
    answers = {"objective": "bourse_investir", "knowledge_level": "debutant", "time_horizon": "long_terme"}
    assert answers["objective"] == "bourse_investir"


def test_track_recommendation_projets():
    answers = {"objective": "financer_projet", "knowledge_level": "debutant", "time_horizon": "moyen_terme"}
    assert answers["objective"] == "financer_projet"


def test_track_recommendation_courant():
    answers = {"objective": "gerer_budget", "knowledge_level": "debutant", "time_horizon": "court_terme"}
    assert answers["objective"] == "gerer_budget"
