"""Module providing a FastAPI application for the sentence API."""

from __future__ import annotations

import codecs
import logging
import os
import re

import polars as pl
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path
from google.cloud import bigquery

from src.models import Sentence, SentenceWithCypher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv()

app = FastAPI(
    title="SMG GM Data Team - Data Engineer Python API Exercise",
    description="""This is a simple REST API containing two endpoints.
    This API allows you to get a sentence with the encrypted version of it (with rot13),
    but also add new sentences in the existing store.""",
    version="1.0.0",
)

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")
TABLE_ID = os.environ.get("TABLE_ID")

# comment this line to run without gcloud auth (test deployment)
client = bigquery.Client(project=PROJECT_ID)

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
    df["cyphered_text"] = df["text"].apply(lambda s: encode(s))

    logging.warning(df.head())

    res = [
        SentenceWithCypher(id=row.id, text=row.text, cyphered_text=row.cyphered_text)
        for row in df.itertuples()
    ]

    return res[0]


@app.post("/sentences/", response_model=SentenceWithCypher, tags=["sentence"])
def post_sentence(body: Sentence) -> SentenceWithCypher:
    """Create a new sentence in the store and return it with its encrypted version.

    Args:
        body (Sentence): instance of Sentence class containing data to insert.

    Returns:
        SentenceWithCypher: the corresponding sentence with cypher object.
    """

    # FIXME 405 method not allowed ?
    if not isinstance(body.id, int) or bool(re.search(r'[^a-zA-Z0-9\s]', body.text)):
        raise HTTPException(status_code=405, detail="Invalid input.")

    # build a data dictionary
    rows_to_insert = {"id": body.id, "text": body.text}

    # inserts simple rows into a table using the streaming API (insertAll).
    errors = client.insert_rows_json(TABLE_PATH, [rows_to_insert])

    if not errors:
        df = pl.from_dicts(rows_to_insert).to_pandas()
        res = with_cypher_col(df)
        return res


@app.get(
    "/sentences/{sentenceId}", response_model=SentenceWithCypher, tags=["sentence"]
)
def get_sentence_by_sentence_id(
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
        SELECT t.id, t.text
        FROM `{TABLE_PATH}` as t
        WHERE t.id = {sentence_id}
    """

    try:
        # Execute the query against BigQuery
        df = client.query_and_wait(sql).to_dataframe()
    except Exception as e:
        logging.error(f"Error: {e}")

    # check for sentence retrieval
    if len(df) == 0:
        raise HTTPException(status_code=404, detail="Sentence not found.")
    
    res = with_cypher_col(df)
    return res