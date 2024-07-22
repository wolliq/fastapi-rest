from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import app

from src.main import encode

import codecs

client = TestClient(app)


def test_rot13():
    encoding = 'rot13'
    test_sentence = 'Hello SMG!'

    codecs_encoded = codecs.encode(test_sentence, encoding)
    smg_func_encoded = encode(test_sentence, encoding)
    
    assert codecs_encoded == smg_func_encoded