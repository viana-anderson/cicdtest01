#!/usr/bin/env python3
"""
Aula 06 -- funcoes puras extraidas do DAG do Airflow (Aula 04/05), para
poderem ser IMPORTADAS e TESTADAS separadamente pelo CI -- essa e a
mudanca de habito mais importante da aula: transformar logica que
estava dentro de uma task do Airflow em funcoes comuns, testaveis sem
precisar subir um container do Airflow inteiro no pipeline de CI.
"""
import pandas as pd


def clean_text(series: pd.Series) -> pd.Series:
    """Mesma normalizacao usada na task clean() do DAG (Aula 04/05):
    minusculas + remove espaco no inicio/fim. Extraida aqui como
    funcao pura para poder ser testada por um teste UNITARIO, sem
    precisar do Airflow rodando."""
    return series.str.lower().str.strip()


REQUIRED_COLUMNS = [
    "id", "texto_relato", "natureza", "bairro", "turno",
    "dia_semana", "houve_violencia", "valor_prejuizo_reais",
    "idade_vitima", "reincidencia",
]


def validate_schema(df: pd.DataFrame) -> list:
    """Teste de DADOS (schema/qualidade): confere se todas as colunas
    esperadas existem. Devolve a lista de colunas faltando (vazia se
    estiver tudo certo) -- usado pelo tests/test_schema.py."""
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]
