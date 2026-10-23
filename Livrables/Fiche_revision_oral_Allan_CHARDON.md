# Préparer la soutenance de vingt minutes

Allan CHARDON - Projet 9 - 22 octobre 2026.

Cette fiche explique les choix à défendre dans l'ordre du support. Les formulations proposées sont à reprendre avec vos mots. Les durées comprennent le temps de montrer les résultats ; une répétition chronométrée avec les clics réels reste nécessaire.

Le message central : **SetFit obtient un score légèrement meilleur avec beaucoup moins de tweets pour l'adaptation. Il est plus lent dans les mesures du projet. Son intérêt dépend du besoin métier.**

## Le déroulé prévu

| Temps cumulé | Diapositives | Partie attendue |
| --- | --- | --- |
| 0 à 5 min | 1 à 5 | Plan, données, choix du modèle et sources |
| 5 à 10 min | 6 à 10 | Contrôle des données, modèles et évaluation |
| 10 à 15 min | 11 à 15 | Résultats, erreurs, coûts et interprétabilité |
| 15 à 20 min | 16 à 18 | Parcours accessible, démonstration et conclusion |
| Pendant les questions | 19 | Références en appui |

À 5 minutes, arriver au contrôle des doublons. À 10 minutes, commencer les résultats. À 15 minutes, passer au dashboard. La discussion de cinq minutes vient après la présentation.

## De zéro à cinq minutes

### 1 Présentation du projet — 30 secondes

« Pour DataSpace, j'ai testé une méthode récente de classification de textes face à une baseline existante. L'objectif est de reconnaître un sentiment positif ou négatif dans un tweet anglais. Je présente le choix des données et ma veille, la comparaison des modèles, puis le dashboard. »

### 2 Objectif de la preuve de concept — 45 secondes

« Le besoin est d'explorer des messages et d'automatiser une première lecture de leur sentiment. Je vérifie si une méthode récente peut rester performante avec un petit jeu d'adaptation. Je regarde donc le score, les données nécessaires et le temps de calcul. Le projet démontre un fonctionnement ; il ne remplace pas encore une analyse humaine en production. »

Le besoin d'entreprise est un scénario : aucun gain financier réel n'a été mesuré.

### 3 Pourquoi Sentiment140 — une minute

« Ce corpus est disponible, volumineux et adapté à une tâche simple de sentiment. Il contient 1,6 million de tweets anglais, autant de négatifs que de positifs. Cela permet de conserver une réserve d'entraînement et un test important. Je garde le texte et le label ; le positif 4 devient 1 pour faciliter les calculs. »

« Les labels proviennent des émoticônes, pas d'une validation humaine de chaque tweet. Ils peuvent comporter des erreurs. Le corpus date de 2009. Mes conclusions concernent ces tweets, en anglais et sans classe neutre. »

### 4 La veille et le choix de SetFit — une minute trente

« Ma référence est l'article de recherche SetFit de septembre 2022, donc de moins de cinq ans à la date du projet. Il propose d'adapter un encodeur de phrases avec peu de textes labellisés, sans prompt. Cela répond à ma question sur le besoin en données. »

« Deux blogs des auteurs, sur Hugging Face, m'aident à l'expliquer. Le blog SetFit de 2022 présente les deux étapes et un exemple de code avec MPNet. Le blog SetFitABSA de 2023 réutilise la méthode pour trouver le sentiment de chaque aspect d'un avis : un écran apprécié et une batterie critiquée, par exemple. »

« L'article présente donc le concept, un blog le met en pratique et l'autre l'adapte. Mon projet conserve le sentiment global du tweet. L'analyse par aspect est une piste, pas un modèle entraîné ici. Les appels de la documentation sont adaptés à Sentiment140, différent des datasets des tutoriels. »

Les blogs sont des sources techniques de leurs auteurs, complémentaires au papier. Les sites cités dans la consigne sont des exemples. Ne pas présenter les blogs comme des articles de revue scientifique.

### 5 Le plan de comparaison — une minute quinze

« Le plan prévoit de préparer les données, entraîner les deux approches, comparer leurs résultats, expliquer le modèle puis présenter les prédictions dans Streamlit. Le notebook contient les deux méthodes. »

« Le train apprend les paramètres ; la validation suit les choix ; le test mesure le résultat final. Le BiLSTM utilise 300 000 tweets ; SetFit, 512 par classe, soit 1 024. Leur test final est commun. La graine 42 permet de retrouver les tirages. »

« Je compare une baseline existante à une adaptation utilisant moins de données. Le protocole compare deux solutions complètes ; il n'isole pas à lui seul l'effet de SetFit. »

La validation SetFit comprend aussi 2 000 tweets, contre 25 000 pour le BiLSTM. Les 1 024 tweets ne représentent donc pas toutes les données mobilisées.

## De cinq à dix minutes

### 6 Le contrôle des doublons — une minute

« Certains textes du test étaient présents dans le train ou la validation, ce qui peut rendre l'évaluation trop favorable. Je les retire, ainsi que les répétitions et textes vides après nettoyage. Le test passe de 50 000 à 47 512 tweets. Les retraits dépendent des textes, pas du modèle qui réussit le mieux. »

« Les modèles sauvegardés sont conservés. Ce test corrigé reste un sous-ensemble du même corpus ; il ne garantit pas une indépendance par utilisateur ou par période. »

### 7 La baseline BiLSTM et GloVe — 55 secondes

« La baseline est une approche plus ancienne, déjà entraînée. GloVe associe à chaque mot un vecteur de 200 nombres. Le LSTM traite la séquence ; sa version bidirectionnelle la lit dans les deux sens. Une couche finale prédit le sentiment. »

« Les séquences de 40 mots couvrent les 37 mots maximum observés sur le train nettoyé. Le vocabulaire de 30 000 entrées limite la mémoire. Le dropout et l'arrêt anticipé limitent le surapprentissage. Je conserve l'état obtenant le meilleur F1 de validation. »

GloVe est déjà préentraîné : ne pas dire que la baseline apprend toute la langue à partir de zéro.

### 8 Le fonctionnement de SetFit — une minute vingt-cinq

« MPNet transforme un tweet entier en un vecteur de 768 nombres tenant compte du contexte. SetFit adapte cet encodeur avec des paires de textes. Deux textes de même sentiment forment une paire positive, même si les deux sont négatifs. Deux sentiments différents forment une paire négative. »

« Le cosinus compare l'orientation des vecteurs. La perte cherche une similarité de 1 pour la même classe et de 0 sinon. Si une paire de même classe a une similarité de 0,8, son erreur au carré vaut 0,04. L'apprentissage modifie les poids pour réduire cette erreur. »

« Une régression logistique apprend ensuite à classer les vecteurs adaptés. Pour prédire, on encode le nouveau texte puis on applique ce classifieur. Il n'y a ni génération de réponse ni prompt. Le préentraînement apporte déjà des connaissances ; les paires ne créent pas de nouvelles annotations indépendantes. »

### 9 Évaluer et choisir les réglages — une minute

« Pour une classe, la précision répond à : parmi les messages annoncés dans cette classe, combien sont corrects ? Le rappel répond à : parmi les vrais messages de cette classe, combien ai-je retrouvés ? Le F1 combine les deux. Le F1 macro moyenne les F1 des deux sentiments. L'accuracy indique la part de labels correctement retrouvés. »

« La perte entraîne les poids ; le F1 mesure la qualité des prédictions. Le BiLSTM retient le meilleur état de validation. Les réglages SetFit sont fixés pour un budget pratique, puis évalués sur validation. Je ne prétends pas avoir trouvé les meilleurs paramètres possibles. »

### 10 Les nettoyages — 40 secondes

« La baseline applique un nettoyage plus fort : minuscules, suppression de ponctuation, URL, mentions et hashtags. SetFit garde davantage de contexte. Les URL et mentions sont normalisées, les caractères pictographiques deviennent des descriptions et les répétitions sont réduites. Le signe du hashtag est retiré, sans découper ses mots. »

« Le dashboard partage le nettoyage SetFit du notebook. La différence de nettoyage entre modèles est une limite de la comparaison. »

## De dix à quinze minutes

### 11 Les résultats — une minute

« Le F1 macro passe de 0,8120 à 0,8163 : un gain faible de 0,427 point de pourcentage. Les accuracies sont de 81,22 % et 81,63 %. Ce sont des accords avec les labels du corpus, potentiellement bruités. »

« SetFit utilise 1 024 tweets pour l'adaptation contre 300 000, soit environ 293 fois moins. Le ratio exclut préentraînement et validation. Il ne signifie pas 293 fois moins de calcul ou d'heures d'annotation réellement mesurées. »

### 12 L'interprétabilité globale — une minute dix

« Les coefficients du classifieur portent sur les dimensions du vecteur, pas directement sur des mots. Je retire donc les mots un à un et mesure la variation de probabilité positive. Je moyenne les variations absolues sur 100 tweets, équilibrés entre les sentiments, pour les mots observés au moins trois fois. »

« Le tableau synthétise la sensibilité sur cet échantillon. Ce n'est pas une liste universelle des mots importants. Trois occurrences restent peu nombreuses et le contexte change l'effet. Le nuage de mots du dashboard montre des fréquences ; il ne mesure pas l'importance pour le modèle. »

### 13 Les matrices de confusion — 50 secondes

« Les lignes sont les labels ; les colonnes, les prédictions. La diagonale contient les bonnes réponses. SetFit retrouve 838 positifs supplémentaires, mais classe aussi 643 négatifs supplémentaires comme positifs. Le bilan est de 195 bonnes réponses de plus. »

« Pour repérer des plaintes, le rappel négatif compte particulièrement. Il passe de 83,51 % pour le BiLSTM à 80,82 % pour SetFit. Le meilleur score global ne suffit pas à recommander SetFit pour tous les usages. »

### 14 Les données et le calcul — 50 secondes

« Le budget de données d'adaptation diminue, mais pas le calcul. Les entraînements enregistrés prennent environ 11,6 minutes pour le BiLSTM et 43 minutes pour SetFit. Ce sont des durées historiques ; le matériel initial est insuffisamment documenté pour un benchmark strict. »

« Sur le test, l'inférence CPU prend 3,1 secondes contre 370,5 secondes, hors chargement et nettoyage, avec des lots différents. L'expérience ne démontre donc pas un avantage de vitesse. »

### 15 Une explication locale — une minute dix

« Pour “My Favourite website is down”, le modèle prédit négatif. La différence entre la probabilité positive du texte complet et celle sans “down” vaut environ −0,9961. Retirer ce mot fait donc remonter la probabilité positive : sa présence contribue au négatif dans cette phrase. »

« “Website” a également un effet très fort. Retirer un mot modifie le contexte et peut rendre la phrase inhabituelle. L'explication locale concerne une décision ; la synthèse globale agrège plusieurs contextes. Les probabilités ne sont pas calibrées et les variations ne prouvent pas une causalité. »

## De quinze à vingt minutes

### 16 Le parcours et l'accessibilité — une minute

« Trois questions organisent les onglets : quelles données sont analysées, quel sentiment est prédit pour un message et comment se comparent les modèles ? Les graphiques permettent de filtrer et de survoler les données. »

« Les figures ont des descriptions et des alternatives en tableau. Le nuage possède un texte alternatif. Les noms et motifs complètent la couleur. Les textes sont foncés sur fond clair, l'affichage supporte l'agrandissement et la page a un titre descriptif. Cela répond aux cinq critères demandés ; je ne revendique pas une certification WCAG complète. »

### 17 La démonstration — trois minutes trente

Ouvrir et charger l'application web avant l'oral ; garder le support dans un autre onglet.

| Durée | Action | Ce qu'elle prouve |
| --- | --- | --- |
| 50 s | Retirer puis rétablir un sentiment ; survoler la répartition et l'histogramme | Deux graphiques interactifs et un filtre partagé |
| 30 s | Modifier le nombre de mots et ouvrir un tableau | Exploration et alternative textuelle ; fréquence différente de l'importance |
| 70 s | Tester `I love this beautiful day`, puis `I hate this terrible day`, puis choisir un exemple | Texte libre et comparaison à un label connu |
| 40 s | Lire les scores et le budget de train dans Performances | Résultats importés du notebook |
| 20 s | Montrer le titre et le zoom du navigateur à 200 %, puis revenir à 100 % | Redimensionnement et lisibilité |

Dire : « Hugging Face héberge les fichiers du modèle. Streamlit les charge et calcule les prédictions sur son serveur. Le cache évite de recharger le modèle à chaque clic. Les performances affichées proviennent de l'évaluation du notebook. »

Si un exemple surprend, expliquer l'erreur et le bruit possible du label ; ne pas garantir que toutes les phrases sont reconnues.

### 18 Conclusion — 30 secondes

« SetFit reste compétitif avec un budget d'adaptation réduit et un léger gain de score. Le choix dépend aussi de la vitesse et des erreurs à éviter. Je confirmerais le résultat avec des budgets identiques, plusieurs graines et un nouveau test manuel. Comparer MPNet gelé à MPNet adapté isolerait aussi l'apport de l'adaptation contrastive. »

## Justifier les paramètres pendant les questions

| Choix | Justification |
| --- | --- |
| Graine 42 et stratification | Retrouver les tirages et conserver les proportions des classes ; une graine seule ne mesure pas la variabilité |
| 300 000 tweets pour la baseline | Budget du modèle sauvegardé, réduit par rapport au corpus ; pas une taille démontrée optimale |
| GloVe Twitter et BiLSTM | Vecteurs préentraînés sur Twitter et modèle plus ancien adapté aux séquences ; baseline existante |
| MPNet | Encodeur proposé dans le blog SetFit ; aucune comparaison de tous les encodeurs |
| 512 tweets par classe | Budget équilibré et réduit par rapport à la baseline ; supérieur aux cas à 8 ou 16 exemples de certains articles |
| Vocabulaire 30 000, longueur 40 | Maîtrise de la mémoire ; longueur suffisante pour le train observé ; symbole pour les mots inconnus |
| 128 unités par direction, dropout 0,3 | Capacité pratique et régularisation ; pas d'optimum démontré |
| Lots 256 pour le BiLSTM, 16 pour SetFit | Compromis de mémoire et de calcul pour deux modèles différents |
| Taux 0,001 et 0,00002 | Ampleurs de mise à jour différentes ; adaptation progressive de l'encodeur préentraîné |
| Une époque et dix itérations de paires | Budget limité ; les paires réutilisent les mêmes textes |
| SetFit : longueur 64 | Limite de sous-mots à l'entraînement ; un sous-mot n'est pas toujours un mot, et cette valeur ne décrit pas la configuration sauvegardée d'inférence |
| Seuil BiLSTM de 0,5 | Règle binaire simple conservée ; un seuil métier serait choisi sur validation, jamais sur le test |

Une époque est un passage sur les données de l'étape concernée. Un lot est un groupe d'exemples traité ensemble. Le taux d'apprentissage règle l'amplitude des mises à jour. Le dropout désactive temporairement des activations à l'entraînement pour limiter la dépendance à quelques signaux.

## Questions probables

| Question | Réponse courte |
| --- | --- |
| Est-il beaucoup plus performant ? | Le gain de score est faible. L'intérêt est la compétitivité avec moins de données d'adaptation, avec une inférence plus lente ici. |
| La comparaison est-elle équitable ? | Même test, mais budgets, nettoyages et validations différents : comparaison de pipelines, pas isolation de tous les facteurs. |
| Avez-vous tout optimisé ? | Les poids sont appris et le BiLSTM sélectionne son meilleur état. Les hyperparamètres SetFit sont fixes ; une recherche systématique reste à faire. |
| Pourquoi pas seulement l'accuracy ? | Le F1 macro complète les bonnes réponses par la précision et le rappel de chaque classe. Les classes étant presque équilibrées, les scores sont proches ici. |
| Pourquoi 0,823 ailleurs ? | C'est le score de validation SetFit. 0,8163 est le résultat final sur le test corrigé, différent en taille et en contenu. |
| Le test est-il entièrement indépendant ? | Les doublons observables sont retirés, mais il vient du même corpus. Des chevauchements train/validation restent dans les partitions historiques. Un découpage propre suivi d'un réentraînement serait plus solide. |
| Pourquoi ne pas refaire les entraînements ? | La remise conserve les modèles et documente leurs limites. Les nouveaux essais devraient avoir un protocole propre et un nouveau test final. |
| Un mot fréquent est-il important ? | Pas forcément : la fréquence décrit les données, l'effet de suppression décrit la sensibilité du modèle. |
| Pourquoi “website” influence-t-il autant ? | Le modèle traite la phrase entière. La suppression change son contexte ; ce n'est pas un poids universel du mot. |
| Peut-on traiter le français ou le neutre ? | Pas avec les garanties de ce projet ; il faut un encodeur, des données et une évaluation adaptés. |
| Que choisir pour des plaintes ? | Examiner le rappel négatif et le coût des erreurs. La baseline retrouve mieux les négatifs ici. |

## Avant la remise et l'oral

Publier les corrections sur le dépôt GitHub utilisé par Streamlit, redéployer, puis vérifier les trois onglets et une vraie prédiction sur l'URL publique. Le premier téléchargement du modèle représente environ 438 Mo : ouvrir l'application à l'avance. L'URL n'a pas été fournie pour une vérification distante pendant cette révision.

Faire une répétition avec les clics réels. Si la présentation dépasse vingt minutes, raccourcir les paramètres ; conserver résultats, interprétabilité et démonstration. Ne pas lancer d'entraînement pendant l'oral. Les détails et références servent aux questions.

Le notebook final est la référence des calculs. La note les synthétise en six pages et le support comporte dix-neuf diapositives. Le notebook exploratoire ancien et les anciens scores ne sont pas les références de la soutenance.
