# Données de la preuve de concept

Sentiment140 a été créé par Alec Go, Richa Bhayani et Lei Huang en 2009. `training.1600000.processed.noemoticon.csv` contient 1,6 million de tweets anglais. Le notebook utilise les labels 0 et 4, puis convertit 4 en 1.

Le corpus source se lit en ISO-8859-1. Les exports dans `SPLIT` sont en UTF-8, avec les colonnes `tweet` et `label`.

| Fichier | Usage | Lignes |
| --- | --- | ---: |
| SPLIT/train.csv | Réserve d'entraînement | 1 525 000 |
| SPLIT/val.csv | Validation d'origine | 25 000 |
| SPLIT/test.csv | Test initial | 50 000 |
| SPLIT/test_independant.csv | Comparaison et dashboard après filtrage | 47 512 |

Le test corrigé reste un sous-ensemble du test initial. Il exclut les textes bruts présents dans le train ou la validation, les chevauchements après nettoyage avec les données utilisées par chaque modèle, les répétitions internes et les textes vides après nettoyage. Le détail figure dans `Results/audit_donnees.json`.

Les partitions d'origine sont conservées pour recharger les modèles sans modifier leurs données d'entraînement. Les indices du vocabulaire du BiLSTM sont sauvegardés dans son modèle.

Références : [article d'origine](https://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf), [fiche du corpus](https://huggingface.co/datasets/stanfordnlp/sentiment140), [GloVe Twitter](https://nlp.stanford.edu/projects/glove/).
