# Correspondance avec le barème

Révision du 22 octobre 2026. Ce document indique où retrouver les éléments préparés ; il ne remplace pas l'évaluation du jury.

| Compétence et critère | Preuve dans le projet |
| --- | --- |
| Veille CE1 : sources reconnues et récentes | Article SetFit et blog explicatif de 2022, blog SetFitABSA de 2023 ; sources des auteurs |
| Veille CE2 : points clés et mathématiques | Note page 2 et notebook : cosinus, perte de paires avec exemple numérique et tête logistique ; étapes ABSA en mots simples |
| Veille CE3 : articulation des sources | Article de recherche → blog de mise en pratique → adaptation ABSA ; notre application à Sentiment140 |
| Veille CE4 : preuve de concept comparée | Notebook, modèles et résultats BiLSTM + GloVe / SetFit + MPNet sur le même test |
| Note CE1 : synthèse | Note de six pages |
| Note CE2 : métrique et optimisation | Page 3 : F1 macro, précision/rappel, validation, arrêt anticipé et réglages fixes SetFit |
| Note CE3 : interprétabilité | Page 5, notebook et exports : suppression locale et agrégation sur 100 tweets |
| Note CE4 : limites et améliorations | Page 6 : budgets identiques, graines, nouveau test, calibration et stabilité des explications |
| Oral CE1 : explications simples | Support : métriques, erreurs, interprétabilité et compromis ; notes du présentateur |
| Oral CE2 : réponse à une question | Questions préparées dans la fiche ; à démontrer pendant la soutenance |
| Oral CE3 : démarche et évaluation complète | Support et notebook ; comparaison des deux modèles |
| Dashboard CE1 : parcours utilisateur | Explorer, tester un message, comparer ; décrit dans la note et la démonstration |
| Dashboard CE2 : deux graphiques interactifs au moins | Répartition, longueurs, fréquences, performances ; filtres, survol et légendes |
| Dashboard CE3 : lisibilité | Graphiques à 16 px, texte foncé et mise en page adaptable |
| Dashboard CE4 : problématique métier | Compréhension du corpus et comparaison de qualité, budget et erreurs |
| Dashboard CE5 : accessibilité | Cinq critères détaillés ci-dessous et contrôles locaux |
| Dashboard CE6 : déploiement web | Mode confirmé : GitHub vers Streamlit ; publier les corrections et vérifier l'URL publique |

| Critère WCAG | Mesure |
| --- | --- |
| 1.1.1 Contenu non textuel | Descriptions, tableaux HTML et attribut alt du nuage |
| 1.4.1 Utilisation de la couleur | Noms, valeurs et motifs en complément des couleurs |
| 1.4.3 Contraste minimum | Texte et nuage foncés sur blanc, labels foncés, accent rouge assombri |
| 1.4.4 Redimensionnement du texte | Affichage fluide, tableaux et contrôle local à 200 % |
| 2.4.2 Titre de page | Titre du navigateur : Analyse de sentiments |

Les contrôles locaux ne constituent pas une certification WCAG complète. L'agrandissement est testé par émulation CSS ; refaire le contrôle avec le zoom habituel sur la version web. La disponibilité publique et les réponses au jury restent à vérifier en situation réelle.
