# Préparer la soutenance de vingt minutes

Allan CHARDON — Projet 9

Le message à retenir : **SetFit obtient un score légèrement meilleur avec moins de tweets pour l'adaptation. Il est plus lent ici et retrouve moins bien les négatifs. Le choix dépend de l'usage.**

Cette fiche sert de repère. Reformuler avec ses mots et répéter avec un chronomètre, en comptant les clics du dashboard.

| Temps | Diapositives | Contenu |
| --- | --- | --- |
| 0 à 5 min | 1 à 5 | Objectif, données, choix de SetFit et sources |
| 5 à 10 min | 6 à 10 | Préparation, modèles et évaluation |
| 10 à 15 min | 11 à 15 | Résultats et explications |
| 15 à 20 min | 16 à 18 | Dashboard et conclusion |
| Questions | 19 | Références en appui |

La discussion de cinq minutes vient après ces vingt minutes.

## De zéro à cinq minutes

**1 et 2 — Objectif — 1 min 15.** « Pour DataSpace, je compare une méthode récente à une baseline pour reconnaître le sentiment d'un tweet anglais. Je vérifie si SetFit reste performant avec peu de données d'adaptation. Le besoin serait d'aider à explorer des messages clients. C'est une preuve de concept, sans gain financier mesuré ni validation en production. »

**3 — Données — 1 min.** « Sentiment140 contient 1,6 million de tweets anglais, moitié négatifs et moitié positifs. Je garde le texte et le sentiment. Le volume permet un test important. Les labels viennent automatiquement des émoticônes et peuvent être faux. Les tweets datent de 2009 et il n'y a pas de classe neutre. »

**4 — Veille — 1 min 30.** « L'article SetFit de septembre 2022 est ma référence. Cette méthode de moins de cinq ans adapte un modèle de phrases à partir de paires de textes. Le blog SetFit de 2022 montre sa mise en pratique avec MPNet. Le blog SetFitABSA de 2023 l'adapte au sentiment par aspect : écran apprécié et batterie critiquée, par exemple. Je conserve ici le sentiment global. L'article présente le concept, un blog l'applique et l'autre l'adapte. Mon code reprend les appels du tutoriel sur un autre dataset, Sentiment140. »

**5 — Plan — 1 min 15.** « Je prépare les données, compare les modèles, explique les résultats puis construis le dashboard. Le train apprend les paramètres, la validation suit les choix et le test mesure le résultat final. La baseline utilise 300 000 tweets de train ; SetFit, 1 024. Les validations contiennent 25 000 et 2 000 tweets. Le test est commun. Budgets et nettoyages diffèrent : je compare deux solutions complètes. »

## De cinq à dix minutes

**6 — Doublons — 1 min.** « Je retire du test les textes déjà présents dans le train ou la validation, avant et après nettoyage, puis les répétitions et textes vides. Il passe de 50 000 à 47 512 tweets pour les deux modèles. Je conserve les modèles existants. Le test reste issu du même corpus, sans garantie d'indépendance par auteur ou période. »

**7 — Baseline — 55 s.** « GloVe représente chaque mot par 200 nombres. Le BiLSTM lit la phrase dans les deux sens, puis prédit le sentiment. Il utilise lui aussi un préentraînement. Le vocabulaire de 30 000 entrées limite la mémoire ; les 40 mots couvrent le maximum de 37 observé sur le train nettoyé. Le dropout et l'arrêt anticipé limitent le surapprentissage. »

**8 — SetFit — 1 min 25.** « MPNet représente la phrase par 768 nombres tenant compte du contexte. SetFit adapte ces représentations avec des paires. La cible vaut 1 pour un même sentiment, y compris deux négatifs, et 0 sinon. Le cosinus compare les représentations. L'erreur d'une paire est le carré de l'écart entre similarité et cible : avec 0,8 et 1, elle vaut 0,04. L'entraînement réduit la moyenne des erreurs. Une régression logistique apprend ensuite à classer les représentations adaptées. Les paires réutilisent les textes sans nouvelles annotations. »

**9 — Évaluation — 1 min.** « La précision répond à : parmi les tweets annoncés négatifs, combien le sont vraiment ? Le rappel répond à : parmi les vrais négatifs, combien ai-je retrouvés ? Le F1 combine les deux. Le F1 macro moyenne les F1 des deux sentiments. L'accuracy est la part de bonnes réponses. La perte entraîne les poids ; le F1 évalue les prédictions. La baseline retient son meilleur état de validation. Les paramètres SetFit sont fixes, sans recherche complète des meilleurs réglages. »

**10 — Nettoyage — 40 s.** « La baseline retire davantage d'éléments. SetFit garde plus de contexte : URL et mentions normalisées, émojis remplacés par des mots, signe du hashtag retiré. Le dashboard partage ce nettoyage. Cette différence entre modèles limite la comparaison. »

## De dix à quinze minutes

**11 — Scores — 1 min.** « Le F1 macro passe de 0,8120 à 0,8163, soit seulement 0,427 point de pourcentage. L'accuracy passe de 81,22 % à 81,63 %. Le gain est modeste. SetFit utilise environ 293 fois moins de tweets d'adaptation ; ce ratio exclut préentraînement et validation. Il ne mesure pas une économie de calcul ou d'heures d'annotation. »

**12 — Vue globale — 1 min 10.** « Je retire les mots un à un et mesure le changement du score positif. Je moyenne l'amplitude des changements sur 100 tweets équilibrés, pour les mots présents au moins trois fois. Cela décrit la sensibilité sur cet échantillon. Le nuage de mots montre des fréquences, différentes de l'importance pour le modèle. »

**13 — Erreurs — 50 s.** « La diagonale des matrices contient les bonnes réponses. SetFit retrouve 838 positifs de plus, mais classe 643 négatifs supplémentaires comme positifs : 195 bonnes réponses de plus au total. Pour détecter des plaintes, le rappel négatif compte particulièrement. Il baisse de 83,51 % à 80,82 % : la baseline peut donc mieux répondre à ce besoin. »

**14 — Calcul — 50 s.** « Les entraînements historiques durent environ 11,6 minutes et 43 minutes. Le matériel initial est insuffisamment documenté pour un benchmark strict. Sur le test, l'inférence CPU prend 3,1 secondes et 370,5 secondes, hors chargement et nettoyage, avec des lots différents. SetFit est plus lent ici. »

**15 — Vue locale — 1 min 10.** « Pour “My Favourite website is down”, SetFit prédit négatif. Retirer “down” fait remonter le score positif : le mot soutient le négatif dans cette phrase. “Website” a aussi un effet fort : retirer un mot modifie le contexte. L'explication locale concerne une prédiction ; la vue globale rassemble plusieurs exemples. Les scores ne sont pas calibrés et les effets ne prouvent pas une causalité. »

## De quinze à vingt minutes

**16 — Accessibilité — 1 min.** « Les trois onglets permettent d'explorer les données, tester un message et comparer les modèles. Les descriptions et tableaux complètent les graphiques. Les noms et motifs complètent la couleur. Les textes sont contrastés, l'affichage supporte l'agrandissement et la page a un titre. Cela couvre les cinq critères demandés, sans certification WCAG complète. »

**17 — Démonstration — 3 min 30.** Ouvrir l'application web à l'avance.

| Durée | Manipulation |
| --- | --- |
| 50 s | Filtrer un sentiment et survoler répartition et histogramme : deux graphiques interactifs |
| 30 s | Changer le nombre de mots et ouvrir un tableau : exploration et alternative textuelle |
| 70 s | Tester `I love this beautiful day`, puis `I hate this terrible day`, puis un exemple du corpus |
| 40 s | Montrer les scores et le budget de données dans Performances |
| 20 s | Montrer le titre et le zoom à 200 %, puis revenir à 100 % |

« Hugging Face héberge les fichiers. Streamlit charge le modèle et calcule les prédictions sur son serveur. Le cache évite de tout recharger à chaque clic. Les scores viennent du notebook. » Si un exemple échoue, expliquer l'erreur.

**18 — Conclusion — 30 s.** « SetFit reste compétitif avec peu de données d'adaptation, mais son gain de score est faible. Je poursuivrais avec des données récentes, des budgets comparables et plusieurs tirages. J'élargirais aussi l'échantillon des explications. »

## Questions probables

| Question | Réponse courte |
| --- | --- |
| Pourquoi 512 tweets par classe ? | Budget réduit et équilibré, supérieur aux cas à 8 ou 16 de certains articles. Ce n'est pas un optimum démontré. |
| Pourquoi MPNet ? | Il est utilisé dans le blog SetFit. Je n'ai pas comparé tous les encodeurs. |
| Avez-vous tout optimisé ? | Les poids sont appris. La baseline retient son meilleur état ; SetFit garde des réglages fixes. Une recherche sur validation reste à faire. |
| La comparaison est-elle équitable ? | Même test, mais budgets, nettoyages et validations différents. Je compare deux solutions, sans isoler chaque facteur. |
| Pourquoi un score de 0,823 ailleurs ? | C'est la validation SetFit ; 0,8163 est le F1 du test final. |
| Les données sont-elles indépendantes ? | Les doublons observables sont retirés du test. La validation historique contient encore 421 textes du train. Un nouveau découpage avant entraînement serait préférable. |
| Un mot fréquent est-il important ? | Pas forcément : fréquence et effet sur une prédiction sont différents. |
| Peut-on traiter le français ou le neutre ? | Il faut des données, un modèle et une évaluation adaptés. Ici : deux sentiments en anglais. |
| Faut-il republier sur Hugging Face ? | Les poids n'ont pas changé ; simplifier les documents ne demande pas de republier le modèle. |

Une époque est un passage sur les données. Un lot est un groupe traité ensemble. Le taux d'apprentissage règle l'amplitude des mises à jour. La graine 42 permet de retrouver les tirages ; elle ne mesure pas leur variabilité.

## Sources et dernière répétition

- [Article SetFit](https://arxiv.org/abs/2209.11055)
- [Blog SetFit](https://huggingface.co/blog/setfit)
- [Blog SetFitABSA](https://huggingface.co/blog/setfit-absa)
- [Tutoriel de code](https://huggingface.co/docs/setfit/v1.1.3/en/quickstart)
- [Perte utilisée](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss)

Vérifier l'URL publique, les trois onglets et une vraie prédiction. Prévoir le chargement initial du modèle, environ 438 Mo. Ne pas lancer d'entraînement pendant l'oral. Si la répétition dépasse vingt minutes, raccourcir les paramètres et conserver les résultats, les explications et la démonstration.
