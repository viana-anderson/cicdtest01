#!/usr/bin/env python3
"""Teste UNITÁRIO — testa uma função pura, isolada, sem depender de
Airflow, Docker ou nenhum serviço externo rodando. Isso é o que torna
esse teste rápido o suficiente para rodar em TODO push, no CI."""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from etl_utils import clean_text


def test_clean_text_lowercases():
    entrada = pd.Series(["FURTO DE CELULAR"])
    resultado = clean_text(entrada)
    assert resultado.iloc[0] == "furto de celular"


def test_clean_text_strips_edges():
    entrada = pd.Series(["   roubo veiculo   "])
    resultado = clean_text(entrada)
    assert resultado.iloc[0] == "roubo veiculo"


def test_clean_text_preserves_internal_spacing():
    # limitação conhecida e documentada: clean_text NÃO colapsa espaços
    # duplos no MEIO do texto (mesmo comportamento do DAG da Aula 04/05)
    entrada = pd.Series(["furto   de   bicicleta"])
    resultado = clean_text(entrada)
    assert resultado.iloc[0] == "furto   de   bicicleta"
