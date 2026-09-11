#!/usr/bin/env python3
"""Aula 06 -- versão em função (importável) do treino rápido da Aula 05,
para poder ser chamada tanto por um script de linha de comando quanto
pelo teste de MODELO do CI (tests/test_model_threshold.py)."""
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

FEATURE_COLS = ["natureza", "bairro", "turno"]
TARGET_COL = "houve_violencia"


def treinar_e_avaliar(caminho_csv: str, random_state: int = 42) -> float:
    """Treina o DecisionTreeClassifier (mesmo modelo da Aula 05) e
    devolve a acurácia no conjunto de teste."""
    df = pd.read_csv(caminho_csv)
    df_modelo = df[FEATURE_COLS + [TARGET_COL]].dropna()

    for col in FEATURE_COLS:
        le = LabelEncoder()
        df_modelo[col] = le.fit_transform(df_modelo[col].astype(str))

    X = df_modelo[FEATURE_COLS]
    y = df_modelo[TARGET_COL].astype(bool)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=random_state
    )
    modelo = DecisionTreeClassifier(max_depth=3, random_state=random_state)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    return accuracy_score(y_test, y_pred)


if __name__ == "__main__":
    import sys
    caminho = sys.argv[1] if len(sys.argv) > 1 else "bos_sinteticos.csv"
    acc = treinar_e_avaliar(caminho)
    print(f"Acurácia no teste: {acc:.2%}")
