# generated by fastapi-codegen:
#   filename:  smg_api.yaml
#   timestamp: 2024-07-22T07:59:18+00:00

from __future__ import annotations

from fastapi import FastAPI, Path

from .models import Sentence, SentenceWithCypher

app = FastAPI(
    title='SMG GM Data Team - Data Engineer Python API Exercise',
    description='This is a simple REST API containing two endpoints. This API allows you to get a sentence with the encrypted version of it (with rot13), but also add new sentences in the existing store.',
    version='1.0.0',
)


@app.post('/sentences/', response_model=SentenceWithCypher, tags=['sentence'])
def post_sentences_(body: Sentence) -> SentenceWithCypher:
    """
    Add a new sentence to the store
    """
    pass


@app.get(
    '/sentences/{sentenceId}', response_model=SentenceWithCypher, tags=['sentence']
)
def get_sentences_sentence_id(
    sentence_id: int = Path(..., alias='sentenceId')
) -> SentenceWithCypher:
    """
    Get a sentence and its encrypted version
    """
    pass
