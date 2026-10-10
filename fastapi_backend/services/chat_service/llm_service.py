"""Service d'intégration avec Ollama (local) avec fallback synthétique."""

import os
from typing import List, Dict, Any, Optional
import ollama

class LLMService:
    """Wrapper pour les appels à l'API locale Ollama (Nom conservé pour compatibilité)."""

    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.3, max_tokens: int = 500) -> str:
        """Envoie les messages à Ollama ou génère une synthèse locale de secours."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            )
            return response['message']['content'].strip()
        except Exception as e:
            print(f"[Ollama] Erreur lors de l'appel : {e}")
            
            # Fallback local
            sys_prompt = ""
            for m in messages:
                if m["role"] == "system":
                    sys_prompt = m["content"]

            if "CONTEXTE DOCUMENTAIRE OFFICIEL :" in sys_prompt:
                ctx = sys_prompt.split("CONTEXTE DOCUMENTAIRE OFFICIEL :")[1].strip()
                lines = [l.strip() for l in ctx.split("\n") if l.strip() and not l.startswith("Source:")]
                text_block = " ".join(lines)
                if len(text_block) > 450:
                    text_block = text_block[:450] + "..."
                return f"Voici les informations officielles de l'écosystème YellowBank concernant votre question :\n\n{text_block}"

            return (
                "Voici les éléments officiels extraits de nos guides certifiés pour vous répondre. "
                "Vous pouvez également solliciter votre conseiller humain depuis votre profil."
            )

llm_service_instance = LLMService()
