# Agentic-benchmark

Repository de traçabilité pour le projet de comparaison des frameworks d'agents IA.

Ce dépôt centralise le protocole de recherche, les tâches de benchmark, les paramètres de configuration et les artefacts produits pendant l'expérimentation. L'objectif est de garder une trace claire des choix méthodologiques et des exécutions réalisées sur le projet.

## Objectif du projet

Comparer de manière systématique plusieurs frameworks d'agents IA, notamment LangChain, CrewAI, AutoGen et LlamaIndex, selon des critères de complétion, de latence, de robustesse et de consommation de ressources.

## Contenu du dépôt

- [Sujet.md](Sujet.md) : sujet initial du projet.
- [Protocole_de_recherche.md](Protocole_de_recherche.md) : cadre méthodologique et critères d'évaluation.
- [Principes_pour_debutants.md](Principes_pour_debutants.md) : version simplifiée pour prise en main.
- [tasks.yaml](tasks.yaml) : liste des tâches de benchmark.
- [prompts.yaml](prompts.yaml) : prompts associés aux expériences.
- [config_example.json](config_example.json) : exemple de configuration pour un adaptateur LLM.
- [requirements.txt](requirements.txt) : dépendances Python.
- [run_all.py](run_all.py) : point d'entrée d'exécution du benchmark.
- [combined_for_pdf.tex](combined_for_pdf.tex) : export LaTeX pour la synthèse ou le rapport.

## Traçabilité

Pour assurer la reproductibilité du projet, il est recommandé de conserver dans ce dépôt :

- la version du framework testé,
- la version du modèle utilisé,
- les paramètres de génération,
- la liste des outils disponibles,
- les jeux de tâches utilisés,
- les scripts d'exécution,
- les logs bruts des expériences,
- les notes de décision quand un changement méthodologique est effectué.

## Installation

Sous Windows / PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Exécution

Mode mock, sans appel à une API externe :

```powershell
python run_all.py
```

Si le script attend une configuration spécifique, copier `config_example.json` vers `config.json` puis compléter les paramètres du fournisseur LLM choisi.

## Organisation des résultats

- Les résultats d'exécution doivent être archivés dans un dossier dédié aux logs ou aux sorties d'expérience.
- Les versions successives du protocole doivent être documentées pour permettre de retrouver l'état du projet à chaque itération.
- Le rapport final peut être rédigé à partir des fichiers source du dépôt et des résultats produits.

## Suivi du projet

1. Définir les tâches de benchmark à exécuter.
2. Fixer les paramètres expérimentaux communs à tous les frameworks.
3. Lancer les exécutions et archiver les logs.
4. Comparer les métriques obtenues.
5. Rédiger la synthèse et les conclusions.

## Référence du dépôt

Projet créé pour servir de base de travail et de traçabilité autour du benchmark agentique.