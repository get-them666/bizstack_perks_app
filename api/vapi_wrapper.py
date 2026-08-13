"""
api/vapi_wrapper.py

Lightweight wrapper for the VAPI Python SDK used by BizStack Perks. This file provides
helper functions to initialize a VAPI client, create or register a voice persona, and
stream responses using a persona-aware prompt template.

IMPORTANT: This is a template that uses the `vapi` Python package. Replace the
placeholder calls with the correct SDK methods for your VAPI provider and do not
commit API keys — set them as environment variables on the host.
"""

import os
import asyncio
import logging

logger = logging.getLogger(__name__)

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_VOICE_ID = os.getenv("VAPI_VOICE_ID")  # optional: pre-created voice model id
VAPI_PROJECT_ID = os.getenv("VAPI_PROJECT_ID")

# Try importing the vapi SDK — if it's not installed this file remains a template.
try:
    import vapi
except Exception:
    vapi = None


class VapiClient:
    def __init__(self, api_key: str = None, project_id: str = None):
        self.api_key = api_key or VAPI_API_KEY
        self.project_id = project_id or VAPI_PROJECT_ID
        if vapi is None:
            logger.warning("vapi SDK not installed; wrapper will be a no-op until it's available.")
            self.client = None
        else:
            # Replace this with the SDK's client constructor
            self.client = vapi.Client(api_key=self.api_key, project_id=self.project_id)

    def is_ready(self) -> bool:
        return self.client is not None

    async def stream_response(self, prompt: str, persona_id: str = None):
        """
        Stream text chunks from the VAPI model. This yields dicts representing partial
        assistant deltas in the same spirit as streaming chat completions.

        The exact implementation depends on the vapi SDK. Keep this async to support
        FastAPI StreamingResponse or server-sent events in your telephony pipeline.
        """
        if not self.client:
            yield {"type": "error", "message": "VAPI client not configured"}
            return

        # Example pseudo-code: replace with actual SDK usage
        stream = self.client.stream_chat(prompt=prompt, voice_id=persona_id or VAPI_VOICE_ID)
        async for chunk in stream:
            # chunk shape depends on provider; normalize to a small dict
            yield {"type": "chunk", "text": chunk.get("text", "")}

    def register_persona(self, persona_name: str, persona_profile: dict):
        """
        Register or create a persona/voice profile on the VAPI service.
        persona_profile should include training text, persona description, and any
        voice modeling preferences (pitch, style, example utterances).

        NOTE: Many providers do not support full "fine-tuning" for voice in the SDK;
        instead you provide a persona prompt and optionally upload audio samples to
        create a custom voice. Consult your VAPI provider documentation.
        """
        if not self.client:
            raise RuntimeError("VAPI client not configured")

        # Pseudo-call, replace with provider method
        persona_id = self.client.create_persona(name=persona_name, profile=persona_profile)
        return persona_id


# Helper: construct persona-aware prompt that includes site docs and product facts
def build_persona_prompt(persona_short_desc: str, knowledge_snippets: list, user_prompt: str) -> str:
    header = f"You are BizStack Perks assistant. Persona: {persona_short_desc}\n"
    facts = "\n\n".join([f"FACT: {s}" for s in knowledge_snippets[:10]])
    template = (
        header
        + "Use the facts below to answer user questions succinctly and in business tone. \n"
        + facts
        + "\n\nUSER: "
        + user_prompt
    )
    return template


# If run standalone, show a small health check
if __name__ == "__main__":
    client = VapiClient()
    print("VAPI client ready?", client.is_ready())
