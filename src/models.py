"""Module providing models for the sentence API application."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Sentence(BaseModel):
    """Class representing a Sentence"""

    id: int = Field(example=10)
    text: str = Field(
        description="text contained in the sentence", example="super movie title"
    )


class SentenceWithCypher(BaseModel):
    """Class representing a SentenceWithCypher"""

    id: int = Field(example=10)
    text: str = Field(
        description="text contained in the sentence", example="super movie title"
    )
    cyphered_text: str = Field(
        description="cyphered text with rot13", example="fhcre zbivr gvgyr"
    )
