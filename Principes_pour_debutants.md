AA# Principes pour débutants — Agents IA et benchmark

Ce document explique, depuis les bases, les concepts clés du projet et des frameworks d'agents (LangChain, CrewAI, AutoGen, LlamaIndex). Il est rédigé pour quelqu'un qui ne connaît rien au sujet.

## 1. Qu'est-ce qu'un "agent IA" ?
- Un agent IA est un programme qui reçoit une demande (prompt) et tente d'accomplir une tâche en utilisant un modèle de langage et éventuellement des outils externes (moteur de recherche, calculatrice, base de données).
- Imaginez un assistant humain : vous lui posez une question, il cherche des informations, utilise un outil si nécessaire, puis vous répond.

## 2. Concepts de base (expliqués simplement)
- Modèle de langage (LLM) : c'est le "cerveau" qui génère du texte. Il prédit des mots pour construire une réponse.
- Prompt : la consigne que vous donnez au modèle (question + instructions). C'est comme donner une tâche à l'agent.
- Token : morceau de texte (mot ou partie de mot) utilisé pour mesurer la longueur d'une demande ou d'une réponse.
- Température : règle qui contrôle la créativité du modèle. Plus elle est élevée, plus les réponses sont variées.
- Tool / Outil : une fonction externe que l'agent peut appeler (API, recherche web, calcul). L'agent décide quand et comment utiliser ces outils.

## 3. Pourquoi utiliser un framework d'agents ?
- Les frameworks fournissent des composants prêts à l'emploi : orchestration, gestion d'outils, mémoire, suivi des interactions.
- Ils aident à structurer des tâches compliquées (plusieurs étapes, plusieurs appels d'outils, agents multiples qui coopèrent).

## 4. Brève présentation des frameworks (idée générale)
- LangChain : orienté chaînes (chains) et pipelines ; bon pour construire des séquences d'étapes et intégrer des outils variés.
- CrewAI : conçu pour des workflows avec rôles et responsabilités ; utile quand plusieurs agents ont des tâches spécialisées.
- AutoGen : puissant pour les scénarios multi-agents interactifs et conversationnels ; facilite la coordination entre agents.
- LlamaIndex : spécialisé dans la récupération et la synthèse d'informations à partir d'un corpus documentaire (RAG — Retrieval Augmented Generation).

## 5. Types de tâches que l'on va benchmarker
- Recherche d'information : trouver une réponse précise.
- Raisonnement séquentiel : résoudre un problème en plusieurs étapes.
- Récupération documentaire : répondre à partir d'un corpus donné.
- Multi-agents : collaboration entre agents spécialisés.
- Gestion d'erreurs : inputs incomplets ou outils défaillants.

## 6. Comment fonctionne une exécution simple (pas-à-pas)
1. Vous posez la question (prompt).
2. L'agent analyse la demande et décide d'une stratégie (ex : chercher, calculer, synthétiser).
3. Si nécessaire, il appelle un outil (ex : recherche web) et récupère des données.
4. Il intègre les résultats et produit une réponse finale.

Exemple concret très simple : "Quel est l'horaire d'ouverture de la bibliothèque municipale ?"
- Étape 1 : Agent lit la question.
- Étape 2 : Agent appelle l'outil de recherche web.
- Étape 3 : Récupère la page contenant l'horaire.
- Étape 4 : Synthétise et répond : "La bibliothèque est ouverte de 9h à 18h du mardi au samedi."

## 7. Variables expérimentales (à maîtriser pour un benchmark fiable)
- Même modèle sous-jacent (même version du LLM).
- Même température et limites de tokens.
- Même jeux d'outils et mêmes timeouts.
- Même format d'entrée/sortie et même nombre d'essais.
Ces contrôles empêchent des biais liés à la configuration.

## 8. Métriques expliquées simplement
- Taux de réussite : proportion de tâches entièrement correctes.
- Complétion partielle : la tâche est partiellement résolue.
- Latence : temps pris pour répondre.
- Nombre d'appels outils : combien de fois l'agent a utilisé des outils.
- Taux d'erreur : exceptions ou réponses invalides.
- Qualitatif (notation humaine) : exactitude, complétude, cohérence.

## 9. Erreurs communes et comment les comprendre
- L'agent invente une réponse (hallucination) : il génère du contenu non vérifié.
- Outil indisponible : faut prévoir que l'appel à un outil puisse échouer et gérer ce cas.
- Ambiguïté dans le prompt : l'agent peut choisir une mauvaise stratégie si la consigne n'est pas claire.

## 10. Bonnes pratiques pour rédiger des tâches et prompts
- Être précis : dire exactement ce que vous attendez en sortie.
- Fournir des exemples de sortie si possible.
- Limiter la complexité d'une tâche pour diagnostiquer les erreurs pas à pas.
- Décrire le format de la réponse (par ex. JSON simple) pour faciliter l'évaluation automatique.

## 11. Glossaire (court)
- Agent : programme qui agit pour accomplir une tâche.
- Framework : boîte à outils logicielle pour construire des agents.
- RAG : méthode qui combine récupération de documents et génération.
- Orchestration : coordination des étapes et des appels d'outils.

## 12. Prochaines étapes recommandées
- Lire le protocole de recherche (document principal) pour comprendre la méthodologie.
- Choisir 5 tâches simples et les formuler clairement.
- Exécuter chaque tâche sur un framework à la fois, en enregistrant prompts, logs et temps.

## 13. Ressources utiles (pour aller plus loin)
- Tutoriels d'introduction aux LLMs (recherchez "Introduction to Large Language Models").
- Documentation officielle : LangChain, AutoGen, LlamaIndex, CrewAI.

---

Si vous le souhaitez, je peux :
- générer 5 exemples de tâches simples adaptés au benchmark,
- rédiger des prompts prêts à l'emploi pour chaque framework,
- ou simplifier davantage une section du fichier.

## Détails complets (expliqués pas à pas)

Cette section apporte des développements concrets pour que vous puissiez mettre en pratique le protocole, même sans connaissances préalables.

### A. Explication approfondie des composants
- `LLM` (modèle de langage) : imaginez un moteur qui complète une phrase pour vous. Il utilise des modèles statistiques entraînés sur de grands textes pour prédire le mot suivant. Les LLM ne "savent" pas comme un humain ; ils imitent des patterns linguistiques.
- `Prompt` : la consigne d'entrée. Un prompt efficace contient : contexte, instruction explicite, format de sortie attendu, et exemples si nécessaire.
- `Tool` (outil) : service externe que l'agent peut appeler (API, recherche web, base de données, calculatrice). L'agent doit décider quand appeler un outil et comment utiliser sa réponse.
- `Orchestration` : la logique qui coordonne LLM et outils (ordre des appels, gestion des erreurs, boucles de clarification).

### B. Démarche pas-à-pas (exécution d'une tâche simple)
1. Écrire un prompt clair (ex : "Donne l'horaire d'ouverture de la mairie de Lyon et cite la source").
2. L'agent analyse et choisit une stratégie (ex: appeler `web_search`).
3. Appel outil et récupération des résultats.
4. Filtrage et sélection de la meilleure source (préférer sources officielles).
5. Génération de la réponse finale en respectant le format demandé.

### C. Détails pratiques sur chaque framework
- LangChain : structure en `chains` et `agents`. Très adapté pour créer pipelines linéaires et intégrer de nombreux outils. Facile à déboguer étape par étape.
- CrewAI : orienté workflows et rôles ; utile si vous voulez définir agents ayant des responsabilités différentes (ex: "recherche", "contrôle qualité").
- AutoGen : facilite la communication entre agents (message-passing). Idéal pour scénarios multi-agents complexes et simulations de dialogues.
- LlamaIndex : optimise l'indexation et la recherche dans un corpus documentaire (RAG). Si l'essentiel du travail est « répondre à partir de documents », c'est souvent la meilleure option.

### D. Templates de prompts (pratiques)
- Prompt informatif simple :
	"Réponds en une phrase à : {question}. Cite la source si trouvée."
- Prompt formaté (JSON) :
	"Réponds uniquement en JSON : {\"answer\": string, \"sources\": [string], \"confidence\": number}."
- Prompt multi-étapes :
	"1) Liste les sous-questions nécessaires ; 2) Pour chaque sous-question, propose une réponse courte ; 3) Fais une synthèse finale."

### E. Exemples de tâches (5 simples + 5 intermédiaires)
- Simples :
	1. Trouver l'horaire d'une administration locale.
	2. Donner la définition d'un terme technique et un exemple.
	3. Résumer un article court (100-200 mots).
	4. Convertir une unité (km -> miles) en montrant le calcul.
	5. Chercher un numéro de contact officiel et citer la source.
- Intermédiaires :
	6. Résoudre un problème mathématique en détaillant les étapes.
	7. Comparer deux sources sur un même fait et indiquer la plus fiable.
	8. Répondre à partir d'un petit corpus (3 documents indexés).
	9. Planifier un événement en plusieurs étapes avec contraintes temporelles.
 10. Coordination multi-agent : agent A collecte, agent B vérifie, agent C synthétise.

### F. Format d'enregistrement (exemple JSON)
Recommandation : enregistrer chaque exécution sous un format structuré pour l'analyse automatique. Exemple minimal :

{
	"task_id": "T1",
	"framework": "LangChain",
	"prompt": "...",
	"start_time": "2026-05-18T10:00:00Z",
	"end_time": "2026-05-18T10:00:04Z",
	"duration_s": 4.0,
	"tool_calls": [ {"tool":"web_search","args":"mairie lyon","duration_s":1.2} ],
	"response": "La mairie est ouverte...",
	"score_manual": {"exactitude":3,"completude":3,"coherence":3},
	"notes": "source officielle citée"
}

### G. Grille d'évaluation et métriques
- Pour chaque réponse, noter : `exactitude`, `complétude`, `cohérence` (0–3).
- Score tache = moyenne des trois notes.
- Metrices automatiques possibles : `latence` (s), `tool_calls_count`, `exact_match` (pour réponses factuelles simples).

### H. Procédure expérimentale (guide rapide)
1. Préparer l'environnement : créer un venv, installer dépendances (ex: `pip install -r requirements.txt`).
2. Choisir et fixer : version du LLM, temperature, max_tokens, timeout.
3. Pour chaque framework et chaque tâche : exécuter N répétitions (3–5) en changeant uniquement la graine si nécessaire.
4. Sauvegarder les logs JSON des exécutions.
5. Faire l'évaluation manuelle et automatisée, puis agréger les résultats (moyennes, écart-type).

Exemple minimal de mesure de temps en Python :

```python
import time
start = time.time()
# exécuter appel au framework
end = time.time()
duration = end - start
```

Mesure mémoire CPU locale : `psutil` (optionnel).  

### I. Métadonnées à collecter
- `seed`, `framework_version`, `llm_model`, `temperature`, `max_tokens`, `timestamp`, `machine_specs`.

### J. Pièges courants et solutions pratiques
- Hallucinations : demander des sources et automatiser un contrôle (outil de vérification ou agent vérificateur).
- Outils indisponibles : prévoir un mécanisme de retry et un message d'erreur standard.
- Variabilité : augmenter le nombre d'exécutions, documenter `seed` et version des outils.

---

Je peux maintenant :
- générer les 5 tâches simples prêtes à l'emploi, ou
- créer un script Python minimal de benchmark qui exécute une tâche et produit le JSON de log.

