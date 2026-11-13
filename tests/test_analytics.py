"""Tests des tranches de confiance du tableau de bord CSV."""

import pandas as pd

from ui.analytics import ETIQUETTES_CONFIANCE, distribution_confiance


def test_tranches_respectent_exactement_le_seuil_d_abstention() -> None:
    scores = pd.Series([0.5, 0.5999, 0.6, 0.7, 0.8, 0.9, 1.0])
    resultats = distribution_confiance(scores)

    assert list(resultats.index) == ETIQUETTES_CONFIANCE
    assert list(resultats.astype(int)) == [2, 1, 1, 1, 2]


def test_scores_absents_ou_hors_intervalle_ne_sont_pas_comptes() -> None:
    resultats = distribution_confiance(pd.Series([None, float("nan"), 0.49, 1.01]))
    assert list(resultats.astype(int)) == [0, 0, 0, 0, 0]
