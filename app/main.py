from __future__ import annotations

from fastapi import FastAPI, Path

from app.models import Sentence, SentenceWithCypher

import codecs

app = FastAPI(
    title='SMG GM Data Team - Data Engineer Python API Exercise',
    description='This is a simple REST API containing two endpoints. This API allows you to get a sentence with the encrypted version of it (with rot13), but also add new sentences in the existing store.',
    version='1.0.0',
)


@app.post('/sentences/', response_model=SentenceWithCypher, tags=['sentence'])
async def post_sentences_(body: Sentence) -> SentenceWithCypher:
    """
    Add a new sentence to the store
    """
    pass


def encode(sentence: str, encoding = 'rot13') -> str:
    """ Function to apply sentence encryption.

    Args:
        sentence (str): the input str to encode using the ROT13.
        encoding (str, optional): Defaults to 'rot13' known as a Caesar cipher.

    Returns:
        str: the encoded string. 
    """
    return codecs.encode(sentence, encoding)


@app.get(
    '/sentences/{sentenceId}', response_model=SentenceWithCypher, tags=['sentence']
)
async def get_sentences_sentence_id(
    sentence_id: int = Path(..., alias='sentenceId')
) -> SentenceWithCypher:
    """
    Get a sentence and its encrypted version
    """

    # get sentence from BigQuery using ID

    # apply encypher rot13 to the sentence

    pass


@app.get("/", tags=['root'])
async def read_main():
    return {"msg": "Hello SMG"}