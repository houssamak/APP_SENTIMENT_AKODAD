"""Préparation des séries affichées par les graphiques Streamlit."""

import pandas as pd

BORNES_CONFIANCE = [0.5, 0.6, 0.7, 0.8, 0.9, 1.000001]
ETIQUETTES_CONFIANCE = ["[0,5–0,6[", "[0,6–0,7[", "[0,7–0,8[", "[0,8–0,9[", "[0,9–1]"]


def distribution_confiance(scores: pd.Series) -> pd.Series:
    """Compte les scores par tranches semi-ouvertes, alignées sur le seuil 0,60."""
    numeriques = pd.to_numeric(scores, errors="coerce").dropna()
    tranches = pd.cut(
        numeriques,
        bins=BORNES_CONFIANCE,
        labels=ETIQUETTES_CONFIANCE,
        right=False,
    )
    return tranches.value_counts(sort=False).reindex(ETIQUETTES_CONFIANCE, fill_value=0)
