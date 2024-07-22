"""Module providing a FastAPI application for the sentence API."""

from __future__ import annotations

import codecs
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path
from google.cloud import bigquery

from src.models import Sentence, SentenceWithCypher

load_dotenv()

app = FastAPI(
    title="SMG GM Data Team - Data Engineer Python API Exercise",
    description="""This is a simple REST API containing two endpoints.
    This API allows you to get a sentence with the encrypted version of it (with rot13),
    but also add new sentences in the existing store.""",
    version="1.0.0",
)

# comment this line to run without gcloud auth (test deployment)
client = bigquery.Client()

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")
TABLE_ID = os.environ.get("TABLE_ID")

TABLE_PATH = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"


def encode(sentence: str, encoding="rot13") -> str:
    """Encode the sentence.

    Args:
        sentence (str): the input str to encode using the ROT13.
        encoding (str, optional): Defaults to 'rot13' known as a Caesar cipher.

    Returns:
        str: the encoded string.
    """
    return codecs.encode(sentence, encoding)


def with_cypher_col(df: pd.DataFrame) -> SentenceWithCypher:
    """Apply the encoding to the input DataFrame object.

    Args:
        df (pd.DataFrame): the input DataFrame object containing 1 row with id and text columns.

    Returns:
        res (SentenceWithCypher): the mapped output SentenceWithCypher object.
    """
    df["cyphered_text"] = df["text"].apply(encode)

    res = [
        SentenceWithCypher(id=row.id, text=row.text, cyphered_text=row.cyphered_text)
        for row in df.itertuples()
    ]

    return res[0]


@app.post("/sentences/", response_model=SentenceWithCypher, tags=["sentence"])
async def post_sentence(body: Sentence) -> SentenceWithCypher:
    """Create a new sentence in the store and return it with its encrypted version.

    Args:
        body (Sentence): instance of Sentence class containing data to insert.

    Returns:
        SentenceWithCypher: the corresponding sentence with cypher object.
    """
    if not int(body.id) and not str(body.text):
        raise HTTPException(status_code=405, detail="Invalid input.")

    # build a data dictionary
    rows_to_insert = [
        {"id": body.id, "text": body.text},
    ]

    # inserts simple rows into a table using the streaming API (insertAll).
    errors = client.insert_rows_json(TABLE_PATH, rows_to_insert)

    if not errors:
        df = pd.DataFrame.from_dict(rows_to_insert[0])
        res = with_cypher_col(df)
        return res

    raise HTTPException(status_code=500, detail="Unable to insert rows.")


@app.get(
    "/sentences/{sentenceId}", response_model=SentenceWithCypher, tags=["sentence"]
)
async def get_sentence_by_sentence_id(
    sentence_id: int = Path(..., alias="sentenceId")
) -> SentenceWithCypher:
    """Get a sentence by ID and the rot13 encryption of it.

    Args:
        sentence_id (int, optional): _description_. Defaults to Path(..., alias='sentenceId').

    Returns:
        SentenceWithCypher: the corresponding sentence with cypher object.
    """

    if not int(sentence_id):
        raise HTTPException(status_code=400, detail="Invalid ID supplied.")

    # hypothesis - only 1 row returned
    sql = f"""
        SELECT id, text
        FROM {TABLE_PATH}
        WHERE id = '{sentence_id}'
    """

    # Execute the query against BigQuery
    df = client.query_and_wait(sql).to_dataframe()

    # check for sentence retrieval
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="Sentence not found.")

    res = with_cypher_col(df)
    return res
