# Projet IA - Principes, sujet et guide de réalisation

Ce document rassemble une version exploitable pour l'export PDF du projet. Il suit le sujet du benchmark comparatif des frameworks d'agents IA et reprend les étapes de réalisation essentielles.

## Sujet du projet

Le projet porte sur la comparaison de quatre frameworks d'agents IA : LangChain, CrewAI, AutoGen et LlamaIndex.

L'étude repose sur AgentBench-FR, une suite de 120 tâches réparties sur 5 niveaux de difficulté, avec les objectifs suivants :

- mesurer le taux de complétion,
- mesurer la latence moyenne,
- mesurer la consommation de ressources,
- mesurer la robustesse face aux erreurs,
- analyser la qualité des réponses.

## Étapes à suivre

- Définir l'objectif du benchmark et les hypothèses du sujet.
- Préparer l'environnement Python et installer les dépendances.
- Créer le fichier local `config.json` avec les clés API et les paramètres du modèle.
- Mettre en place un adaptateur commun pour chaque framework.
- Intégrer les API des agents avec la même structure d'entrée et de sortie.
- Construire les 120 tâches dans `tasks.yaml`.
- Construire les prompts associés dans `prompts.yaml`.
- Lancer les exécutions avec les mêmes paramètres pour tous les frameworks.
- Sauvegarder les réponses, les appels outils, les erreurs et la latence dans des logs.
- Comparer les résultats entre les frameworks.
- Rédiger le rapport final et préparer le PDF.

## Intégration des API des agents

Chaque framework doit être exposé par un adaptateur qui reçoit :

- un prompt,
- des paramètres de génération,
- éventuellement des outils,
- éventuellement un contexte documentaire,
- une configuration d'API.

L'adaptateur doit renvoyer :

- la réponse finale,
- les appels outils,
- la durée d'exécution,
- les erreurs éventuelles,
- les métadonnées utiles.

### Configuration recommandée

Le fichier `config.json` doit rester local et non versionné. Il peut contenir :

```json
{
  "llm_provider": "openai",
  "api_key_env": "OPENAI_API_KEY",
  "model": "gpt-4o",
  "temperature": 0.0,
  "max_tokens": 512
}
```

La clé API doit être stockée dans une variable d'environnement, jamais en dur dans le dépôt.

### Rôle des frameworks

- LangChain : orchestration flexible avec chaînes, outils et agents.
- CrewAI : coordination par rôles et responsabilités.
- AutoGen : dialogue et collaboration multi-agents.
- LlamaIndex : récupération documentaire et synthèse fondée sur un corpus.

## Métriques d'évaluation

Les résultats doivent être comparés selon :

- le taux de réussite,
- le taux de complétion partielle,
- la latence moyenne,
- le nombre d'appels aux outils,
- le taux d'erreur,
- la consommation de ressources,
- la qualité qualitative de la réponse.

## Structure recommandée du rapport PDF

1. Introduction générale
2. État de l'art
3. Problématique et objectifs
4. Méthodologie expérimentale
5. Description d'AgentBench-FR
6. Résultats expérimentaux
7. Analyse comparative
8. Discussion des limites
9. Conclusion et perspectives

## Traçabilité

Pour garantir la reproductibilité, conserver :

- la version de chaque framework,
- la version du modèle,
- les paramètres de génération,
- la liste des outils,
- les jeux de tâches utilisés,
- les scripts d'exécution,
- les logs bruts,
- les décisions méthodologiques.

## Conclusion

Le projet vise à produire un benchmark reproductible et documenté, avec un rendu final exploitable dans un mémoire ou un rapport PDF.
