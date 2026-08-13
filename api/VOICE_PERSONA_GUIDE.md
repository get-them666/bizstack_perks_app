# VOICE_PERSONA_GUIDE.md

This document describes how to prepare and train a voice + assistant persona for BizStack Perks
using the VAPI stack. The goal is to create a voice assistant that speaks knowledgeably about:
- BizStack Perks product features (leads ingestion, underwriting, card monetization)
- Loan underwriting criteria and processes
- Card/perk monetization flows and affiliate tracking
- Company voice: professional, concise, business-first, helpful

Steps to produce a well-trained voice persona

1) Gather knowledge corpus
   - README, PRIVACY_DISCLOSURE.md, B2B_OUTREACH_EMAIL.md, consult.html, infrastructure.html, index.html
   - Any internal playbooks or underwriting rules (CSV or Markdown). Prefer concise bullet rules.
   - Example lead submission templates and sample dialogs the bot should handle.

2) Prepare training artifacts
   - Text snippets: extract the most important 500-2000 tokens of product facts and underwriting rules.
   - Dialog pairs: 50-200 sample Q/A pairs that represent the bot's expected conversations.
   - Optional voice samples: 5-20 high-quality audio samples if you intend to create a custom TTS voice.

3) Persona prompt design (prompt engineering)
   - Create a short persona descriptor (2-3 sentences) that describes tone, domain expertise, and constraints.
   - Use a retrieval-augmented generation (RAG) approach: store the corpus as embeddings and fetch relevant snippets
     at request time instead of trying to fine-tune a single model with all facts.

4) Implementation options
   - Lightweight: Keep using prompt engineering + RAG with the VAPI runtime. No heavy fine-tuning needed.
     - Store embeddings (e.g., in SQLite or vector DB) and at request time fetch top-k facts and include them in the prompt.
     - This is fast, legal-friendly, and easy to iterate on.
   - Full voice fine-tune: Upload curated audio transcripts and request a TTS provider to create a custom voice.
     - This may require more time, credits, and provider support.

5) Integrate into code
   - Add an api/vapi_wrapper.py (done) to centralize client usage.
   - Add a small service to ingest corpus files, create embeddings (or link to a vector DB), and create persona profiles.
   - Expose endpoints: /vapi/assistant (chat-like), /vapi/stream (SSE for telephony), /vapi/train-persona (admin-only).

6) Safety, compliance, and monitoring
   - Add disclaimers for underwriting advice (not financial advice) and capture consent for lead sharing.
   - Log all voice interactions (with user consent) for iterative improvement and debugging.
   - Keep PII removal/obfuscation in logs to comply with privacy rules.

7) Testing and iteration
   - Create a test harness that sends 100 representative prompts and records responses.
   - Review answers for hallucinations and factual accuracy; iterate on prompt templates and corpus.
   - Optionally hire a domain SME to review responses and edit the corpus.

What I can do next (if you say proceed)
- Implement a minimal persona pipeline: ingest product docs, create embeddings, and add RAG retrieval used by the VAPI streaming endpoint.
- Add admin endpoints to upload corpus, create persona, and test voice responses.
- Wire sample SSE streaming endpoint (FastAPI) that integrates with VAPI streaming and uses the persona prompt.

Data & secrets I will need from you
- VAPI_API_KEY and any project/voice IDs (never commit secrets in repo). Add these to host env vars.
- A corpus or pointer to where documents live (you can upload to repo or provide links). If sensitive, provide over secure channel.
- If you want a custom voice, upload audio samples or provide access to existing recordings.

