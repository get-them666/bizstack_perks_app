"""Ingest repository documentation files into the local RAG corpus for VAPI persona training.
This script runs locally and writes to the corpus/ namespace used by api/utils/embeddings.py
"""
import os
from pathlib import Path
from api.utils.embeddings import ingest_texts

REPO_ROOT = Path(__file__).resolve().parents[1]
FILES_TO_INGEST = [
    'README.md',
    'PRIVACY_DISCLOSURE.md',
    'B2B_OUTREACH_EMAIL.md',
    'consult.html',
    'infrastructure.html',
]


def read_file(path: Path):
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return ''


def ingest_all():
    texts = []
    for fname in FILES_TO_INGEST:
        p = REPO_ROOT / fname
        if p.exists():
            content = read_file(p)
            texts.append(content)
    if texts:
        ingest_texts('repo_docs', texts)
        print(f'Ingested {len(texts)} documents into corpus/repo_docs.jsonl')
    else:
        print('No files found to ingest')

if __name__ == '__main__':
    ingest_all()
