# Checklist rapide du projet

Ce fichier résume les deux volets du projet de manière ultra-lisible et exploitable.

---

## VOLET A: TÂCHES TECHNIQUES

Les tâches à accomplir pour générer les données et les résultats du benchmark.

### Phase 1 : Environnement et configuration

- [x] Créer et activer l'environnement Python `.venv`
- [x] Installer les dépendances (`pip install -r requirements.txt`)
- [x] Créer le fichier local `config.json` (non versionné)
- [ ] Configurer le backend local Ollama et le modèle de référence
- [ ] Tester la réponse locale sur une tâche de référence

Statut au 2026-05-20 : `config.json` créé, chargeur de config validé. Il reste à valider la réponse locale du modèle de référence.

### Phase 2 : Structure des adaptateurs

- [x] Créer le dossier `adapters/`
- [x] Implémenter `adapters/base_adapter.py` (interface commune)
- [x] Implémenter `adapters/langchain_adapter.py`
- [x] Implémenter `adapters/crewai_adapter.py`
- [x] Implémenter `adapters/autogen_adapter.py`
- [x] Implémenter `adapters/llamaindex_adapter.py`
- [x] Tester chaque adaptateur isolément
- [x] Valider que tous retournent le même schéma JSON

Statut : structure `adapters/` initialisée et testée avec `test_adapters.py`.

### Phase 3 : Tâches et prompts

- [x] Élargir `tasks.yaml` à 120 tâches (24 par catégorie × 5 niveaux)
- [ ] Couvrir les 5 catégories :
  - [x] Recherche d'information (24 tâches)
  - [x] Raisonnement séquentiel (24 tâches)
  - [x] Récupération documentaire (24 tâches)
  - [x] Multi-agent (24 tâches)
  - [x] Erreurs et ambiguïtés (24 tâches)
- [x] Créer les prompts associés dans `prompts.yaml` pour chaque framework
- [x] Valider la cohérence avec `validate_tasks.py`

### Phase 4 : Orchestration et exécution

- [x] Créer/mettre à jour `run_all.py` avec les options : `--frameworks`, `--repeats`, `--output-dir`, `--mode`
- [x] Implémenter le mode mock pour tester sans API
- [x] Tester le mode mock: `python run_all.py --frameworks mock --repeats 2 --mode mock`
- [x] Documenter les paramètres fixes (température, tokens, timeout)

### Phase 5 : Collecte des résultats

- [x] Créer le dossier `logs/`
- [x] Implémenter les logs JSON horodatés : `logs/benchmark_YYYY-MM-DD_HHMMSS.json`
- [x] Créer `logs/manifest.json` pour l'index des exécutions
- [x] Implémenter l'archivage automatique
- [x] Valider que les logs sont en JSON valide

### Phase 6 : Analyse

- [x] Créer le script `analyze.py`
- [x] Calculer les statistiques agrégées (taux, latence, erreurs)
- [x] Générer les CSV : `results/summary_by_framework.csv`, `results/summary_by_category.csv`
- [x] Générer les graphiques : `results/latency_boxplot.png`, `results/completion_rates.png`
- [x] Exporter en JSON pour le rapport : `results/analysis.json`
- [ ] Valider que toutes les données pour le rapport sont prêtes

---

## VOLET B: CONTENU DU RAPPORT (LaTeX + pdflatex)

La structure complète du rapport de recherche à rédiger et compiler.

### Structure générale

```
I. Introduction générale
II. État de l'art
III. Problématique et objectifs
IV. Méthodologie expérimentale
V. Description d'AgentBench-FR
VI. Résultats expérimentaux
VII. Analyse comparative
VIII. Discussion
IX. Conclusion et perspectives
X. Références bibliographiques
```

### I. Introduction générale

**Objectif :** Motiver le projet et expliquer son importance.

**À inclure :**
- Contexte de croissance des frameworks d'agents IA
- Problème identifié (absence de benchmarks standardisés)
- Objectif principal (créer AgentBench-FR)
- Vue d'ensemble du rapport

### II. État de l'art

**Objectif :** Situer le projet dans le contexte académique.

**À inclure :**
- Historique et architecture de LangChain, CrewAI, AutoGen, LlamaIndex
- Comparaison fonctionnelle
- Benchmarks existants et leurs lacunes
- Concepts clés (ReAct, Tool calling, Multi-agent orchestration)

### III. Problématique et objectifs

**Objectif :** Formuler clairement les questions de recherche.

**Questions de recherche :**

**RQ1 :** Quel framework offre le meilleur taux de complétion ?

**RQ2 :** Quel framework présente la latence la plus faible ?

**RQ3 :** Quel framework est le plus robuste face aux erreurs ?

**RQ4 :** Quel framework performe le mieux sur les tâches multi-agents ?

**RQ5 :** Dans quelles conditions chaque framework devient-il le plus pertinent ?

**Hypothèses :**

- H1 : AutoGen performera mieux sur les tâches multi-agents
- H2 : LangChain offrira une grande flexibilité générale
- H3 : CrewAI sera efficace pour les workflows par rôles
- H4 : LlamaIndex montrera de meilleurs résultats sur la récupération documentaire

### IV. Méthodologie expérimentale

**Objectif :** Décrire précisément la démarche expérimentale.

**À inclure :**
- Design expérimental
- Variables de contrôle (modèle, température, tokens, timeout, etc.)
- Environnement technique (hardware, versions, OS)
- Protocol de collecte
- Gestion des erreurs

### V. Description d'AgentBench-FR

**Objectif :** Présenter la suite de benchmark proposée.

**À inclure :**
- Vue d'ensemble : 120 tâches, 5 niveaux, 5 catégories
- Les 5 catégories de tâches avec exemples et critères de succès :
  1. Recherche d'information
  2. Raisonnement séquentiel
  3. Récupération documentaire
  4. Collaboration multi-agents
  5. Gestion d'erreurs contrôlées
- Adaptation des prompts par framework
- Niveaux de difficulté

### VI. Résultats expérimentaux

**Objectif :** Présenter les données brutes quantitatives.

**À inclure :**
- Tableau récapitulatif global (Framework | Complétion | Latence | Erreurs | Appels outils | Score)
- Résultats par framework
- Résultats par catégorie
- Résultats par niveau de difficulté
- Graphiques : histogrammes, boxplots, courbes de performance
- Heatmap : Framework × Catégorie
- Tableau des erreurs fréquentes

### VII. Analyse comparative

**Objectif :** Interpréter les résultats et répondre aux questions de recherche.

**À inclure :**
- Réponses explicites à RQ1-RQ5 avec justifications
- Validation/réfutation des hypothèses H1-H4
- Forces et faiblesses de chaque framework
- Analyse des modes d'échec
- Corrélations architecture-performance

### VIII. Discussion

**Objectif :** Débattre les implications et limitations.

**À inclure :**
- Implications pratiques pour la sélection de frameworks
- Recommandations par cas d'usage
- Limitations méthodologiques
- Limitations dues au modèle et aux paramètres
- Limitations de reproductibilité
- Améliorations futures
- Recommandations pour la communauté

### IX. Conclusion et perspectives

**Objectif :** Synthétiser et conclure.

**À inclure :**
- Synthèse des résultats principaux
- Contributions du projet
- Recommandations finales (quel framework pour quel usage)
- Travaux futurs
- Appel à la communauté pour collaboration

### X. Références bibliographiques

**À inclure :**
- Documentation officielle des 4 frameworks
- Articles académiques sur les agents IA
- Benchmarks existants (s'il y en a)
- Articles sur ReAct, Chain-of-Thought, etc.
- Articles sur la récupération documentaire
- Articles sur la collaboration multi-agent

---

## Structure des fichiers LaTeX

### Arborescence recommandée

```
rapport/
├── main.tex                 (document principal)
├── preamble.tex             (packages et configuration)
├── chapters/
│   ├── 01_introduction.tex
│   ├── 02_etat_art.tex
│   ├── 03_problematique.tex
│   ├── 04_methodologie.tex
│   ├── 05_benchmark.tex
│   ├── 06_resultats.tex
│   ├── 07_analyse.tex
│   ├── 08_discussion.tex
│   └── 09_conclusion.tex
├── figures/
│   ├── latency_boxplot.png
│   ├── completion_rates.png
│   ├── heatmap_framework_category.png
│   └── ...
├── tables/
│   ├── results_summary.tex
│   ├── errors_summary.tex
│   └── ...
├── references.bib           (base bibliographique)
└── Makefile                 (build script)
```

### Compilation avec pdflatex

```bash
cd rapport/
pdflatex -interaction=nonstopmode main.tex
bibtex main.aux
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### Checklist de validation du rapport

- [ ] Tous les chapitres rédigés
- [ ] Toutes les figures insérées
- [ ] Toutes les références citées et dans le .bib
- [ ] pdflatex compile sans erreur
- [ ] Table des matières générée correctement
- [ ] Numérotation des sections et figures correcte
- [ ] Relecture complète pour fautes et cohérence
- [ ] Tous les tableaux et graphiques alignés avec les résultats

---

## Flux de travail global

### Étape 1 : Implémentation technique (VOLET A)
```
Semaines 1-2 : Environnement + Adaptateurs
Semaine 3 : Tâches + Prompts
Semaine 4 : Exécution + Collecte
```

### Étape 2 : Analyse des résultats (VOLET A)
```
Semaine 5 : Script analyze.py + Graphiques
```

### Étape 3 : Rédaction du rapport (VOLET B)
```
Semaine 6 : Introduction + État de l'art
Semaine 7 : Problématique + Méthodologie
Semaine 8 : Description + Résultats
Semaine 9 : Analyse + Discussion
Semaine 10 : Conclusion + Relecture
```

---

## Ressources clés

- [Guide_de_realisation.md](Guide_de_realisation.md) : Guide détaillé complet
- [Sujet.md](Sujet.md) : Sujet académique du projet
- [Protocole_de_recherche.md](Protocole_de_recherche.md) : Méthodologie académique
- [tasks.yaml](tasks.yaml) : Liste des tâches
- [prompts.yaml](prompts.yaml) : Prompts par framework
- [config_example.json](config_example.json) : Configuration exemple
- [run_all.py](run_all.py) : Script d'orchestration

---

## Contacts et versions

- **Version du guide** : 2.0 (restructuré avec deux volets)
- **Date** : 2026-05-20
- **Status** : Opérationnel
