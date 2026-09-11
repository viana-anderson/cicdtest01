#!/usr/bin/env python3
"""Teste de MODELO (limiar mínimo de performance) — treina o modelo e
FALHA o pipeline se a acurácia cair abaixo de um limiar aceitável. É
este tipo de teste que impede um modelo pior de ser promovido a
produção sem ninguém perceber."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from treino import treinar_e_avaliar

# bos_sinteticos.csv fica um nível acima de tests/ -- na raiz do aula6_material
# (rodando local) ou na raiz do SEU repositório, se você o copiou pra lá junto
# com src/, tests/ e requirements-dev.txt (ver "Uso básico" no LEIA-ME).
DATA_DIR = os.path.join(os.path.dirname(__file__), "..")
CSV_PATH = os.path.join(DATA_DIR, "bos_sinteticos.csv")

LIMIAR_MINIMO = 0.60  # 60% -- limiar didático, calibrado para o dataset fictício de 40 linhas


def test_model_meets_minimum_accuracy():
    if not os.path.exists(CSV_PATH):
        pytest.skip(f"dataset de exemplo não encontrado em {CSV_PATH} — rode a partir do repositório do curso")
    acc = treinar_e_avaliar(CSV_PATH)
    assert acc >= LIMIAR_MINIMO, (
        f"acurácia {acc:.2%} abaixo do limiar mínimo de {LIMIAR_MINIMO:.0%} — "
        "pipeline não deve promover este modelo"
    )
