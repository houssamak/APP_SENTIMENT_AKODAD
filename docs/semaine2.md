# Analyse des erreurs du TP2

Sur les 58 avis de test, le modèle commet 7 erreurs : 5 avis positifs sont classés négatifs et 2 avis négatifs sont classés positifs, tous dans des formulations mitigées. Le modèle TF-IDF compte les mots positifs et négatifs sans comprendre leur ordre ni le retournement introduit par « mais finalement » ou une expression similaire. Pour réduire ces erreurs, il faudrait représenter le contexte et l'ordre des mots, puis réévaluer sur un jeu plus grand et varié, notamment avec des embeddings ou un modèle de langue.
