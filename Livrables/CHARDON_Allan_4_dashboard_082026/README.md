# Dashboard de classification de sentiments

Depuis ce dossier, dans un environnement Python 3.11 ou 3.12 :

```powershell
python -m pip install -r requirements.txt
python -m streamlit run Dashboard/app.py
```

Parcours : explorer les tweets, tester un message, comparer les modèles. Les graphiques possèdent des descriptions, des tableaux et des motifs. Le nuage possède un texte alternatif. Les contrastes et l'agrandissement à 200 % ont été contrôlés localement ; refaire le contrôle sur la version web. Les résultats proviennent du notebook. Le modèle public AllanC23/setfit-mpnet-sentiment est chargé à une révision figée. Le premier chargement nécessite Internet et environ 438 Mo de téléchargement.

Sur Streamlit Community Cloud, sélectionner Dashboard/app.py et Python 3.11 ou 3.12. Publier aussi SRC, Data/SPLIT/test_independant.csv, Results/comparaison_modeles.csv et .streamlit/config.toml. La configuration .streamlit doit rester à la racine du dépôt. Mettre à jour GitHub, redéployer, puis vérifier les trois onglets et une prédiction sur l'URL publique. Aucune URL n'a été transmise pour un contrôle distant.
