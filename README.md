# Classification de sentiments avec SetFit

Projet 9 d'Allan CHARDON. La preuve de concept compare un BiLSTM avec GloVe et SetFit avec MPNet sur Sentiment140. La révision du 22 octobre 2026 suit le barème : veille, modélisation, interprétabilité, présentation et accessibilité.

## Résultats

Les modèles sont évalués sur les mêmes 47 512 tweets, après retrait des chevauchements avec le train et la validation, des répétitions et des textes vides après nettoyage.

| Modèle | Exemples de train | Accuracy | F1 macro |
| --- | ---: | ---: | ---: |
| BiLSTM + GloVe | 300 000 | 0,8122 | 0,8120 |
| SetFit + MPNet | 1 024 | 0,8163 | 0,8163 |

Le gain de F1 est de 0,427 point. Le train est environ 293 fois plus petit, hors préentraînement et validation. SetFit est plus lent à l'inférence dans ces mesures. Les budgets, nettoyages et validations diffèrent et un seul entraînement est disponible par modèle.

Les résultats du 26 septembre 2026 figurent dans Results. Cette révision ajoute les explications et l'accessibilité ; elle ne réentraîne pas les modèles. Les anciennes analyses d'incertitude restent archivées.

## Lancer le projet

Avec Python 3.11 ou 3.12, depuis la racine :

```powershell
python -m pip install -r Dashboard/requirements.txt
python -m streamlit run Dashboard/app.py
```

Pour le notebook, installer requirements.txt. environment.yml décrit aussi un environnement Conda. Le premier chargement demande Internet et environ 438 Mo ; Streamlit conserve ensuite le modèle en cache.

Le notebook de référence est Notebooks/notebook_final_entrainement.ipynb. REUSE_TRAINED_MODELS = True recharge les poids. False active les entraînements. Réentraîner la baseline nécessite GloVe Twitter 200d ou une matrice dont le vocabulaire est vérifié. Les partitions initiales restent nécessaires au contrôle des données.

## Dashboard et accessibilité

Le parcours conserve trois onglets : explorer les données, prédire un sentiment, comparer les modèles. Les graphiques sont interactifs, décrits et accompagnés de tableaux de valeurs. Les groupes sont distingués par des noms et motifs. Le nuage possède un texte alternatif, les contrastes sont renforcés et le titre de page est explicite.

Le modèle est chargé depuis AllanC23/setfit-mpnet-sentiment à la révision 403b8b648f16e6eb919ef76037ae62fcc80daa1d. Hugging Face héberge les fichiers ; Streamlit calcule les prédictions sur CPU. Les scores affichés proviennent du notebook.

Les contrôles locaux incluent un agrandissement de page à 200 % par émulation CSS. Ils ne constituent pas une certification WCAG complète ; refaire le contrôle avec le zoom habituel sur la version web.

## Mettre à jour la version web

Le déploiement utilise GitHub et Streamlit Community Cloud. Publier Dashboard, SRC, .streamlit/config.toml, Data/SPLIT/test_independant.csv et Results/comparaison_modeles.csv, puis redéployer Dashboard/app.py. Dashboard/requirements.txt contient les dépendances. La configuration .streamlit doit rester à la racine du dépôt.

Vérifier les trois onglets, une prédiction et les tableaux sur l'URL publique. Aucune URL n'a été transmise pour contrôler la version web depuis cette session.

## Livrables et sources

Livrables contient le plan d'une page, le notebook, la note de six pages, le dashboard et le support de 19 diapositives. Les noms utilisent août 2026, mois de démarrage. La fiche de révision et conformite_bareme.md préparent l'oral. L'archive comprend données, modèles et code.

- Tunstall et al. (2022), [SetFit](https://arxiv.org/abs/2209.11055) : article principal.
- Jo et al. (2022), [blog SetFit](https://huggingface.co/blog/setfit) : explication des deux phases et exemple de code avec MPNet.
- Laperdon et al. (2023), [SetFitABSA](https://huggingface.co/blog/setfit-absa) : adaptation du concept au sentiment par aspect, étudiée dans la veille.
- [Quickstart SetFit 1.1.3](https://huggingface.co/docs/setfit/v1.1.3/en/quickstart) : code adapté de SST-2 à Sentiment140.
- Go et al. (2009), [Sentiment140](https://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf) : corpus et labels automatiques.
