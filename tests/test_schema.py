#!/usr/bin/env python3
"""Teste de DADOS (schema/qualidade) — confere que o CSV tem as
colunas esperadas ANTES de deixar o pipeline seguir para treino/deploy.
Este é o tipo de teste que pega um dataset quebrado (coluna renomeada,
faltando, etc.) antes que ele vire um modelo ruim em produção."""
import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from etl_utils import REQUIRED_COLUMNS, validate_schema

# bos_sinteticos.csv fica um nível acima de tests/ -- na raiz do aula6_material
# (rodando local) ou na raiz do SEU repositório, se você o copiou pra lá junto
# com src/, tests/ e requirements-dev.txt (ver "Uso básico" no LEIA-ME).
DATA_DIR = os.path.join(os.path.dirname(__file__), "..")
CSV_PATH = os.path.join(DATA_DIR, "bos_sinteticos.csv")


def test_required_columns_present_in_example_dataset():
    if not os.path.exists(CSV_PATH):
        pytest.skip(f"dataset de exemplo não encontrado em {CSV_PATH} — rode a partir do repositório do curso")
    df = pd.read_csv(CSV_PATH)
    faltando = validate_schema(df)
    assert faltando == [], f"colunas faltando no dataset: {faltando}"


def test_validate_schema_detects_missing_column():
    # dataset PROPOSITALMENTE quebrado (falta a coluna "natureza") --
    # prova que o teste de fato pega o problema, e não só "sempre passa"
    df_quebrado = pd.DataFrame({c: [] for c in REQUIRED_COLUMNS if c != "natureza"})
    faltando = validate_schema(df_quebrado)
    assert faltando == ["natureza"]
