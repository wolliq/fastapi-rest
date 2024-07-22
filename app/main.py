from __future__ import annotations

from fastapi import FastAPI, HTTPException, Path

from app.models import Sentence, SentenceWithCypher

import os
import codecs
from dotenv import load_dotenv
from google.cloud import bigquery

from fastapi import Request
from fastapi.responses import JSONResponse
import logging
import pandas as pd


load_dotenv()

app = FastAPI(
    title='SMG GM Data Team - Data Engineer Python API Exercise',
    description="""This is a simple REST API containing two endpoints. 
    This API allows you to get a sentence with the encrypted version of it (with rot13), 
    but also add new sentences in the existing store.""",
    version='1.0.0',
)

# global handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, ex: Exception):
    logging.error(f"Unhandled exception: {ex}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

# client = bigquery.Client()

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")
TABLE_ID = os.environ.get("TABLE_ID")

TABLE_PATH = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"


@app.post('/sentences/', response_model=SentenceWithCypher, tags=['sentence'])
async def post_sentences_(body: Sentence) -> SentenceWithCypher:
    """ Create a new sentence in the store and return it with its encrypted version.

    Args:
        body (Sentence): instance of Sentence class containing data to insert.

    Returns:
        SentenceWithCypher: the corresponding sentence with cypher object.
    """
    if not int(body.id) and not str(body.text):
        raise HTTPException(status_code=405, detail=f"Invalid input.")

    # build a data dictionary
    rows_to_insert = [{"id": body.id, "text": body.text},]

    # inserts simple rows into a table using the streaming API (insertAll). 
    errors = client.insert_rows_json(TABLE_PATH, rows_to_insert)

    if errors == []:
        inserted_df = pd.DataFrame.from_dict(rows_to_insert[0])
        # apply encypher rot13 to the sentence
        inserted_df['encoded_text'] = inserted_df['text'].apply(lambda s: encode(s))
    
        # serialize into the return type
        res = [
            SentenceWithCypher(row.id, row.text, row.encoded_text) 
            for row in inserted_df.itertuples()
        ]

        out = res[0]

        return out
    else:
        raise HTTPException(status_code=500, detail=f"Unable to process.")


def encode(sentence: str, encoding = 'rot13') -> str:
    """ Encode the sentence.

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
    """Get a sentence by ID and the rot13 encryption of it.

    Args:
        sentence_id (int, optional): _description_. Defaults to Path(..., alias='sentenceId').

    Returns:
        SentenceWithCypher: the corresponding sentence with cypher object.
    """

    if not int(sentence_id):
        raise HTTPException(status_code=400, detail=f"Invalid ID supplied.")
    
    # hypothesis - only 1 row returned
    sql = f"""
        SELECT id, text
        FROM {TABLE_PATH}
        WHERE id = '{sentence_id}'
    """

    # Execute the query against BigQuery
    sentence_df = client.query_and_wait(sql).to_dataframe()

    # check for sentence retrieval
    if len(sentence_df) == 0:
        raise HTTPException(status_code=404, detail="Sentence not found.")
        
    # apply encypher rot13 to the sentence
    sentence_df['encoded_text'] = sentence_df['text'].apply(lambda s: encode(s))
    
    # serialize into the return type
    res = [
        SentenceWithCypher(row.id, row.text, row.encoded_text) 
        for row in sentence_df.itertuples()
    ]

    out = res[0]

    return out


# TODO remove me - only for local deployment testing
@app.get("/", tags=['root'])
async def read_main():
    return {"msg": "Hello SMG"}