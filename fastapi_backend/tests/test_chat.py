"""Tests unitaires pour l'agent de veille marché et le chat."""

from services.chat_service.agents.market_agent import market_agent_instance
from services.chat_service.agents.faq_agent import faq_agent_instance


def test_market_agent_briefing():
    briefing = market_agent_instance.get_briefing("tech")
    assert "sector" in briefing
    assert "ambiance" in briefing
    assert "disclaimer" in briefing
    # Vérification du garde-fou réglementaire MiFID II
    assert "Ne constitue pas un conseil" in briefing["disclaimer"]


def test_faq_agent_detection():
    assert faq_agent_instance.can_handle("comment faire opposition sur ma carte") is True
    assert faq_agent_instance.can_handle("quel temps fait-il") is False
