"""Tests unitaires pour le moteur de gamification et les jalons."""

from services.gamification_service import DEFAULT_MISSIONS


def test_default_missions_exist():
    assert len(DEFAULT_MISSIONS) >= 6
    tracks = {m["track"] for m in DEFAULT_MISSIONS}
    assert "courant" in tracks
    assert "pea" in tracks
    assert "projets" in tracks
