# Guide de réalisation du projet

Ce document sert de feuille de route pour réaliser le projet de benchmark des frameworks d'agents IA de bout en bout. Il est aligné sur le sujet du projet: comparaison de LangChain, CrewAI, AutoGen et LlamaIndex à travers la suite AgentBench-FR, composée de 120 tâches réparties sur 5 niveaux de difficulté.

## Structure du guide

Ce guide se divise en deux parties distinctes:

- **PARTIE A: TÂCHES TECHNIQUES** - Toutes les tâches de développement, configuration et exécution pour générer les données et résultats.
- **PARTIE B: CONTENU DU RAPPORT** - Structure complète du rapport de recherche, chapitres, questions à répondre et contenu nécessaire pour chaque section.

## Étapes à suivre

- Définir clairement l'objectif du benchmark: comparer LangChain, CrewAI, AutoGen et LlamaIndex sur la complétion, la latence, la robustesse et la consommation de ressources.
- Reprendre les hypothèses du sujet: AutoGen performant en multi-agent, LangChain flexible, CrewAI orienté rôles, LlamaIndex fort sur la récupération documentaire.
- Préparer l'environnement Python et installer les dépendances.
- Créer le fichier de configuration local `config.json` avec les clés API et les paramètres du modèle.
- Choisir le framework à tester et lui associer un adaptateur commun.
- Intégrer les API des agents en respectant la même structure d'entrée et de sortie pour tous.
- Préparer les 120 tâches du benchmark dans `tasks.yaml` en respectant les 5 catégories: recherche d'information, raisonnement séquentiel, récupération documentaire, multi-agent, ambiguïtés et erreurs contrôlées.
- Préparer les prompts associés dans `prompts.yaml` en gardant le même objectif métier pour chaque framework.
- Lancer les exécutions avec les mêmes paramètres pour tous les frameworks: même modèle, même température, même limite de tokens, même budget d'outils, même timeout et même nombre d'essais.
- Sauvegarder les réponses, les appels outils, les erreurs, la latence et les métadonnées dans des logs horodatés.
- Comparer les résultats obtenus entre les frameworks avec les métriques du sujet: taux de complétion, latence moyenne, consommation de ressources et résilience aux erreurs.
- Préparer la synthèse finale et la mise en forme PDF du mémoire ou du rapport.

---

# PARTIE A: TÂCHES TECHNIQUES

Cette partie énumère les tâches de développement, de configuration et d'exécution à accomplir pour produire les données d'expérimentation.

## 1. Objectif du projet

Le but est de comparer plusieurs frameworks d'agents IA, notamment LangChain, CrewAI, AutoGen et LlamaIndex, sur des tâches identiques afin de mesurer :

- le taux de complétion,
- la latence,
- la robustesse,
- la consommation de ressources,
- la qualité des réponses.

Le projet doit rester reproductible. Chaque choix technique doit donc être documenté.

## 2. Organisation recommandée du travail

1. Reprendre la problématique et les hypothèses du sujet.
2. Fixer le protocole expérimental commun à tous les frameworks.
3. Mettre en place les adaptateurs API.
4. Construire la suite AgentBench-FR et les prompts.
5. Lancer les expériences répétées.
6. Archiver les traces et les logs.
7. Analyser les résultats par tâche et par framework.
8. Rédiger le rapport final et préparer le PDF.

## 3. Préparer l'environnement

Avant de commencer le développement, il faut installer les dépendances et vérifier la cohérence de l'environnement.

### 3.1 Installation de base

Sous Windows / PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
**Checklist technique :**

- [x] Créer l'environnement virtuel avec `python -m venv .venv`
- [x] Activer l'environnement
- [x] Vérifier que pip est à jour avec `pip --version`
- [x] Installer les dépendances avec `pip install -r requirements.txt`
- [x] Tester les imports: `python -c "import langchain; import crewai; import pyautogen; import llama_index"`

Statut au 2026-05-20 : environnement `.venv` opérationnel, dépendances `requirements.txt` installées et vérifiées.
### 3.2 Vérification du projet

Les fichiers de référence du dépôt sont :

- [Sujet.md](Sujet.md) pour le sujet académique,
- [Protocole_de_recherche.md](Protocole_de_recherche.md) pour la méthodologie,
- [tasks.yaml](tasks.yaml) pour les tâches,
- [prompts.yaml](prompts.yaml) pour les prompts,
- [config_example.json](config_example.json) pour la configuration,
- [run_all.py](run_all.py) pour le lancement global.

**Checklist technique :**

- [x] Vérifier que `Sujet.md` contient le sujet académique complet
- [x] Vérifier que `Protocole_de_recherche.md` est cohérent
- [x] Lister les tâches existantes dans `tasks.yaml`
- [x] Vérifier que `prompts.yaml` a des prompts pour au moins 10 tâches
- [x] Vérifier que `config_example.json` est un modèle valide
- [x] Vérifier que `run_all.py` existe et est exécutable

Prochaine étape immédiate : démarrer la Phase 2 (structure des adaptateurs) avec un socle minimal exécutable.

## 4. Intégration des API des agents

Cette étape est la plus importante pour la réalisation concrète du benchmark. L'idée est de créer une couche d'abstraction commune qui permet d'appeler différents frameworks avec le même contrat d'entrée et de sortie.

### 4.1 Principe général

Chaque framework doit être exposé derrière un adaptateur unique. Cet adaptateur reçoit :

- un prompt,
- des paramètres de génération,
- éventuellement une liste d'outils,
- éventuellement un contexte documentaire,
- une configuration d'API.

Il renvoie :

- la réponse finale,
- les appels outils effectués,
- la durée d'exécution,
- les erreurs éventuelles,
- les métadonnées utiles à l'analyse.

### 4.2 Configuration des accès API

Le fichier [config_example.json](config_example.json) montre une configuration minimale. En pratique, il faut créer un fichier local `config.json` non versionné contenant :

- le fournisseur LLM,
- la variable d'environnement de la clé API,
- le nom du modèle,
- la température,
- la limite de tokens,
- éventuellement les paramètres réseau ou de proxy.

Exemple logique de configuration :

```json
{
  "llm_provider": "openai",
  "api_key_env": "OPENAI_API_KEY",
  "model": "gpt-4o",
  "temperature": 0.0,
  "max_tokens": 512
}
```

La clé API ne doit jamais être écrite en dur dans le dépôt. Elle doit rester dans l'environnement local ou dans un gestionnaire de secrets.

Pour le sujet actuel, il est conseillé de garder une configuration unique par campagne de test afin que tous les frameworks utilisent le même modèle et les mêmes paramètres.

**Checklist technique :**

- [x] Créer `config.json` (local, non versionné) à partir de `config_example.json`
- [x] Définir le fournisseur LLM (ex: openai, anthropic, azure)
- [ ] Ajouter la clé API à la variable d'environnement (ne pas l'écrire en dur)
- [x] Tester la connexion: `python -c "from adapters.config import load_config; cfg=load_config(); print(cfg)"`
- [x] Documenter la clé API attendue dans le `.gitignore` ou un fichier de secrets

### 4.3 Variables d'environnement

Selon le fournisseur choisi, prévoir par exemple :

- `OPENAI_API_KEY`,
- `ANTHROPIC_API_KEY`,
- `AZURE_OPENAI_API_KEY`,
- `AZURE_OPENAI_ENDPOINT`,
- `GOOGLE_API_KEY`.

L'adaptateur doit lire la bonne variable à partir de la configuration.

### 4.4 Structure de l'adaptateur

Chaque framework doit idéalement implémenter la même interface métier, par exemple :

```python
class AgentAdapter:
    def run(self, task: dict, config: dict) -> dict:
        """Exécute une tâche et renvoie une structure standardisée."""
```

Structure de sortie recommandée :

```python
{
  "framework": "LangChain",
  "task_id": "T1",
  "prompt": "...",
  "response": "...",
  "tool_calls": [],
  "latency_seconds": 0.0,
  "error": null,
  "metadata": {}
}
```

**Checklist technique :**

- [x] Créer le dossier `adapters/` à la racine
- [x] Implémenter `adapters/base_adapter.py` avec l'interface commune
- [x] Implémenter `adapters/langchain_adapter.py`
- [x] Implémenter `adapters/crewai_adapter.py`
- [x] Implémenter `adapters/autogen_adapter.py`
- [x] Implémenter `adapters/llamaindex_adapter.py`
- [x] Tester chaque adaptateur sur une tâche simple: `python test_adapters.py`
- [x] Vérifier que tous les adaptateurs retournent le même schéma JSON
- [x] Vérifier que chaque adaptateur peut mesurer: latency, error, tool_calls, response

### 4.5 Intégration par framework

#### LangChain

Utiliser LangChain pour orchestrer un agent avec outils, mémoire ou chaîne simple selon la tâche. Le flux conseillé est :

1. charger le modèle depuis la configuration,
2. définir les outils,
3. construire l'agent ou la chaîne,
4. exécuter le prompt,
5. enregistrer la réponse et les appels outils.

#### CrewAI

CrewAI convient bien aux rôles spécialisés. Le flux conseillé est :

1. définir les rôles d'agents,
2. attribuer une mission claire à chaque rôle,
3. organiser la coordination,
4. exécuter la tâche,
5. collecter la sortie finale et les traces.

#### AutoGen

AutoGen est adapté aux échanges multi-agents. Le flux conseillé est :

1. créer les agents conversationnels,
2. définir leurs responsabilités,
3. autoriser la collaboration ou la vérification,
4. exécuter le dialogue,
5. sauvegarder la conversation et la synthèse finale.

#### LlamaIndex

LlamaIndex doit être utilisé surtout pour la récupération documentaire et les réponses fondées sur un corpus. Le flux conseillé est :

1. indexer les documents,
2. configurer le moteur de requête,
3. lancer la question,
4. récupérer les passages utiles,
5. enregistrer la réponse avec les références.

**Checklist technique par framework :**

- [ ] LangChain: tester avec `AgentExecutor` + outils + logs
- [ ] CrewAI: tester avec 2-3 rôles d'agents + mission
- [ ] AutoGen: tester avec dialogue multi-agents
- [ ] LlamaIndex: tester avec indexation et récupération

### 4.6 Correspondance avec le sujet

Le sujet impose une lecture comparative et reproductible. Le guide doit donc conserver les mêmes axes d'évaluation pour tous les frameworks :

- complétion de tâche,
- latence moyenne,
- consommation de ressources,
- taux d'erreur,
- robustesse face aux sorties partielles ou incorrectes,
- qualité de la réponse finale.

**Checklist technique :**

- [x] Créer un fichier `metrics.py` qui définit les axes d'évaluation
- [x] Ajouter un logging JSON structuré pour chaque métrique
- [x] Tester que chaque adaptateur loggue correctement

### 4.7 Pont commun entre frameworks

Pour éviter les différences de structure, chaque adaptateur doit :

- accepter la même structure d'entrée,
- produire le même schéma de sortie,
- utiliser les mêmes paramètres de génération,
- journaliser les mêmes métadonnées,
- gérer les erreurs de la même manière.

Cela permet une comparaison plus juste.

**Checklist technique :**

- [x] Créer une classe `BenchmarkRunner` qui orchestre les adaptateurs
- [x] Implémenter un système de logs JSON commun
- [x] Créer un fichier `logs/benchmark_YYYY-MM-DD_HHMMSS.json`
- [x] Tester: `python benchmark.py --framework langchain --repeats 1 --task T1`

## 5. Préparer les tâches et les prompts

Les tâches doivent rester comparables entre frameworks. Le fichier [tasks.yaml](tasks.yaml) liste les tâches de base, et [prompts.yaml](prompts.yaml) montre comment adapter le même exercice à chaque framework.

Pour le sujet, les tâches doivent couvrir au minimum :

- la recherche d'information,
- le raisonnement en plusieurs étapes,
- la récupération documentaire,
- la collaboration multi-agents,
- la gestion d'erreurs contrôlées.

Le nombre cible est de 120 tâches réparties sur 5 niveaux de difficulté.

**Checklist technique :**

- [x] Étendre `tasks.yaml` à 120 tâches (24 par catégorie * 5 niveaux)
- [x] Créer des tâches dans les 5 catégories:
   - [x] Recherche d'information (24 tâches)
   - [x] Raisonnement séquentiel (24 tâches)
   - [x] Récupération documentaire (24 tâches)
   - [x] Multi-agent (24 tâches)
   - [x] Erreurs et ambiguïtés (24 tâches)
- [x] Pour chaque tâche T_i, créer des prompts dans `prompts.yaml` pour les 4 frameworks
- [x] Valider que chaque prompt est coherent et testable
- [x] Créer un script `validate_tasks.py` pour vérifier la cohérence

Bonnes pratiques :

- formuler une consigne courte et non ambiguë,
- garder la même difficulté pour tous les frameworks,
- fixer les mêmes entrées variables,
- éviter les indices propres à un framework,
- préciser le format de sortie attendu.

## 6. Définir le protocole d'exécution

Le fichier [run_all.py](run_all.py) orchestre les exécutions. Le principe attendu est :

1. choisir un ou plusieurs frameworks,
2. exécuter chaque tâche plusieurs fois,
3. collecter les logs,
4. lancer l'analyse.

Pour obtenir des résultats comparables, il faut fixer :

- le même modèle,
- la même température,
- la même limite de tokens,
- le même budget d'outils,
- le même nombre de répétitions.

**Checklist technique :**

- [x] Créer ou mettre à jour `run_all.py` avec les options: `--frameworks`, `--repeats`, `--output-dir`, `--mode` (mock/real)
- [x] Ajouter les arguments optionnels: `--verbose`, `--log-level`, `--timeout`
- [x] Tester le mode mock: `python run_all.py --frameworks mock --repeats 2 --mode mock`
- [x] Créer un script `run_benchmark.sh` pour lancer la campagne complète
- [x] Documentez les paramètres fixes: température, max_tokens, timeout par tâche

## 7. Collecte et traçabilité des résultats

Chaque exécution doit enregistrer au minimum :

- l'identifiant de la tâche,
- le framework utilisé,
- le prompt envoyé,
- la réponse finale,
- les appels outils,
- la latence,
- les erreurs,
- la date et l'heure,
- la version du modèle.

Il est recommandé de conserver les sorties brutes dans un dossier de logs séparé et de ne jamais les écraser sans archivage.

**Checklist technique :**

- [x] Créer un dossier `logs/` pour stocker les résultats JSON
- [x] Implémenter un système de timestamps: `logs/benchmark_YYYY-MM-DD_HHMMSS.json`
- [x] Créer `logs/manifest.json` pour indexer toutes les exécutions
- [x] Implémenter un archivage automatique: `logs/archive/`
- [x] Créer un script `cleanup_logs.py` pour gérer les anciens logs
- [x] Tester que les logs sont valides JSON: `python -m json.tool logs/*.json`

## 8. Analyse des résultats

Une fois les expériences terminées, comparer les frameworks selon :

- le taux de réussite,
- le taux d'erreur,
- la latence moyenne,
- le nombre d'appels outils,
- la qualité des réponses,
- la robustesse sur les tâches multi-agents.

Les résultats peuvent être présentés sous forme de :

- tableau comparatif,
- graphique de latence,
- histogramme des taux de réussite,
- tableau des erreurs fréquentes,
- synthèse qualitative.

Pour le PDF final, il est utile de présenter aussi :

- un tableau récapitulatif par framework,
- un tableau récapitulatif par catégorie de tâche,
- une synthèse des échecs récurrents,
- une lecture des différences architecturales observées.

**Checklist technique :**

- [x] Créer un script `analyze.py` qui lit tous les logs JSON
- [x] Calculer les statistiques agrégées par framework et par catégorie
- [x] Générer les tableaux CSV: `results/summary_by_framework.csv`, `results/summary_by_category.csv`
- [x] Générer les graphiques: `results/latency_boxplot.png`, `results/completion_rates.png`
- [x] Exporter les résultats en JSON pour le rapport: `results/analysis.json`
- [ ] Créer un rapport HTML interactif (optionnel): `results/dashboard.html`
- [ ] Valider que toutes les données nécessaires au rapport sont prêtes

---

# PARTIE B: CONTENU DU RAPPORT DE RECHERCHE

Cette partie définit la structure complète du rapport en LaTeX, les sections, les questions à répondre et le contenu attendu pour chaque chapitre.

Le rapport sera rédigé en LaTeX et compilé avec `pdflatex`.

## Plan général du rapport

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

---

## I. Introduction générale

### Objectif de cette section

Motiver le projet et expliquer pourquoi ce benchmark est nécessaire.

### Questions à répondre

- Pourquoi les frameworks d'agents IA sont-ils importants actuellement ?
- Quel problème ce projet vise-t-il à résoudre ?
- Pourquoi un benchmark systématique est-il nécessaire ?
- Quel impact ce travail aura-t-il ?

### Contenu minimal à inclure

1. **Contexte et justification**
   - Croissance exponentielle des frameworks d'agents IA
   - Prolifération de LangChain, CrewAI, AutoGen, LlamaIndex
   - Impact sur l'industrie et la recherche

2. **Le problème identifié**
   - Absence de benchmarks standardisés
   - Difficulté pour les praticiens à choisir le bon framework
   - Manque de données comparatives reproductibles

3. **Objectif principal**
   - Proposer AgentBench-FR comme suite de benchmark
   - Fournir une évaluation rigoureuse et reproductible
   - Aider les praticiens à prendre des décisions éclairées

4. **Vue d'ensemble du rapport**
   - Plan des chapitres suivants
   - Contribution du travail

### Structure LaTeX recommandée

```latex
\section{Introduction}
\subsection{Contexte et motivation}
\subsection{Problématique}
\subsection{Objectifs}
\subsection{Contributions}
\subsection{Structure du rapport}
```

---

## II. État de l'art

### Objectif de cette section

Situer le projet dans le contexte académique et technologique existant.

### Questions à répondre

- Quels frameworks d'agents existent et comment ont-ils évolué ?
- Quels benchmarks existent déjà pour les agents IA ?
- Quelles lacunes identifiez-vous ?
- Quels sont les paradigmes d'orchestration existants ?

### Contenu minimal à inclure

1. **Frameworks d'agents IA**
   - LangChain: histoire, architecture, cas d'usage
   - CrewAI: orientation rôles, architecture
   - AutoGen: dialogue multi-agent, architecture
   - LlamaIndex: récupération documentaire, architecture

2. **Comparaison fonctionnelle**
   - Outils et intégrations
   - Orchestration et workflows
   - Support multi-agent
   - Performance et scalabilité

3. **Benchmarks existants**
   - Benchmarks académiques pour LLMs
   - Benchmarks pour les agents (s'ils existent)
   - Limitations des benchmarks actuels

4. **Lacunes et opportunités**
   - Manque de benchmark systématique pour les agents
   - Besoin de reproductibilité
   - Besoin de standardisation

5. **Concepts clés**
   - ReAct (Reasoning + Acting)
   - Tool calling patterns
   - Multi-agent orchestration
   - Metrics for agent evaluation

### Structure LaTeX recommandée

```latex
\section{État de l'art}
\subsection{Frameworks d'agents IA}
\subsubsection{LangChain}
\subsubsection{CrewAI}
\subsubsection{AutoGen}
\subsubsection{LlamaIndex}
\subsection{Benchmarks existants}
\subsection{Lacunes identifiées}
```

---

## III. Problématique et objectifs

### Objectif de cette section

Formuler précisément les questions de recherche et les hypothèses testées.

### Questions de recherche principales

**RQ1:** Quel framework offre le meilleur taux de complétion sur des tâches standardisées ?

**RQ2:** Quel framework présente la latence la plus faible ?

**RQ3:** Quel framework est le plus robuste face aux erreurs et ambiguïtés ?

**RQ4:** Quel framework performe le mieux sur les tâches multi-agents ?

**RQ5:** Dans quelles conditions chaque framework devient-il le plus pertinent ?

### Hypothèses de recherche

**H1:** AutoGen sera plus performant (taux de complétion) sur les tâches multi-agents, grâce à son paradigme conversationnel et collaboratif.

**H2:** LangChain offrira une grande flexibilité et de bonnes performances générales sur les tâches simples et complexes.

**H3:** CrewAI sera particulièrement efficace pour les workflows structurés par rôles et responsabilités.

**H4:** LlamaIndex montrera de meilleurs résultats sur les tâches reposant sur la récupération et la synthèse documentaire.

### Périmètre de l'étude

- **Frameworks étudiés:** LangChain, CrewAI, AutoGen, LlamaIndex
- **Nombre de tâches:** 120 tâches
- **Niveaux de difficulté:** 5 niveaux
- **Catégories:** 5 catégories de tâches
- **Modèle LLM:** Même modèle pour tous les frameworks
- **Paramètres fixes:** Même température, tokens, timeout
- **Reproductibilité:** Tous les résultats doivent être reproductibles

### Structure LaTeX recommandée

```latex
\section{Problématique et objectifs}
\subsection{Questions de recherche}
\subsection{Hypothèses}
\subsection{Périmètre de l'étude}
```

---

## IV. Méthodologie expérimentale

### Objectif de cette section

Décrire précisément comment l'expérimentation a été menée pour garantir la reproductibilité.

### Questions à répondre

- Comment les expériences ont-elles été conçues ?
- Quels paramètres ont été fixés et pourquoi ?
- Comment la reproductibilité a-t-elle été assurée ?
- Quels outils et environnement ont été utilisés ?

### Contenu minimal à inclure

1. **Design expérimental**
   - Vue d'ensemble de l'approche
   - Phases de l'expérimentation
   - Variables contrôlées vs libres

2. **Variables de contrôle**
   - Modèle LLM utilisé
   - Température
   - Limite de tokens
   - Budget d'appels outils
   - Timeout par tâche
   - Nombre de répétitions

3. **Environnement technique**
   - Hardware utilisé (CPU, mémoire, GPU)
   - Versions des frameworks
   - Version de Python
   - Système d'exploitation

4. **Protocol de collecte**
   - Ordre d'exécution des tâches
   - Gestion des erreurs
   - Logging des résultats
   - Format des données collectées

5. **Gestion des erreurs**
   - Comment les timeouts sont gérés
   - Comment les erreurs d'API sont gérées
   - Nombre de retries éventuels

### Structure LaTeX recommandée

```latex
\section{Méthodologie expérimentale}
\subsection{Design de l'expérimentation}
\subsection{Variables contrôlées}
\subsection{Environnement technique}
\subsection{Protocol de collecte}
\subsection{Gestion des erreurs}
```

---

## V. Description d'AgentBench-FR

### Objectif de cette section

Présenter la suite de benchmark proposée: ses tâches, sa structure et son design.

### Questions à répondre

- Pourquoi 120 tâches réparties sur 5 niveaux ?
- Comment les 5 catégories ont-elles été choisies ?
- Comment les prompts ont-ils été adaptés par framework ?
- Quels critères de succès pour chaque tâche ?

### Contenu minimal à inclure

1. **Vue d'ensemble d'AgentBench-FR**
   - Nom et objectif
   - Nombre total de tâches: 120
   - Répartition: 5 catégories × 24 tâches
   - Niveaux de difficulté: 5 niveaux

2. **Les 5 catégories de tâches**

   a) **Recherche d'information**
      - Objectif: Trouver une information dans une source donnée
      - Exemple de tâche
      - Critère de succès

   b) **Raisonnement séquentiel**
      - Objectif: Résoudre un problème en plusieurs étapes
      - Exemple de tâche
      - Critère de succès

   c) **Récupération documentaire**
      - Objectif: Répondre à partir d'un corpus
      - Exemple de tâche
      - Critère de succès

   d) **Collaboration multi-agents**
      - Objectif: Coordonner plusieurs agents
      - Exemple de tâche
      - Critère de succès

   e) **Gestion d'erreurs contrôlées**
      - Objectif: Gérer des entrées ambiguës ou erronées
      - Exemple de tâche
      - Critère de succès

3. **Niveaux de difficulté**
   - Niveau 1: Tâches simples
   - Niveau 2: Tâches modérées
   - Niveau 3: Tâches intermédiaires
   - Niveau 4: Tâches complexes
   - Niveau 5: Tâches très complexes

4. **Adaptation des prompts**
   - Prompts génériques vs spécifiques
   - Adaptation pour LangChain
   - Adaptation pour CrewAI
   - Adaptation pour AutoGen
   - Adaptation pour LlamaIndex

### Structure LaTeX recommandée

```latex
\section{Description d'AgentBench-FR}
\subsection{Vue d'ensemble}
\subsection{Catégories de tâches}
\subsubsection{Recherche d'information}
\subsubsection{Raisonnement séquentiel}
\subsubsection{Récupération documentaire}
\subsubsection{Collaboration multi-agents}
\subsubsection{Gestion d'erreurs}
\subsection{Niveaux de difficulté}
\subsection{Adaptation des prompts}
```

---

## VI. Résultats expérimentaux

### Objectif de cette section

Présenter les données brutes et les résultats quantitatifs du benchmark.

### Contenu minimal à inclure

1. **Tableau récapitulatif global**
   - Framework | Complétion | Latence avg | Erreurs | Appels outils | Score global

2. **Résultats par framework**
   - LangChain: taux de complétion, latence, erreurs
   - CrewAI: taux de complétion, latence, erreurs
   - AutoGen: taux de complétion, latence, erreurs
   - LlamaIndex: taux de complétion, latence, erreurs

3. **Résultats par catégorie**
   - Tableau: Recherche vs Raisonnement vs Récupération vs Multi-agent vs Erreurs

4. **Résultats par niveau de difficulté**
   - Graphique montrant la performance vs difficulté

5. **Graphiques et figures**
   - Histogramme des taux de complétion
   - Boxplot des latences
   - Courbe de performance vs difficulté
   - Heatmap: Framework × Catégorie

6. **Tableau des erreurs fréquentes**
   - Framework | Type d'erreur | Fréquence | Exemple

### Structure LaTeX recommandée

```latex
\section{Résultats expérimentaux}
\subsection{Vue d'ensemble}
\subsection{Résultats par framework}
\subsection{Résultats par catégorie}
\subsection{Résultats par niveau de difficulté}
\subsection{Graphiques et figures}
\subsection{Erreurs et anomalies}
```

---

## VII. Analyse comparative

### Objectif de cette section

Interpréter les résultats et répondre aux questions de recherche.

### Questions à répondre

- Quel framework performe le mieux globalement ? **Réponse à RQ1**
- Quel framework a la latence la plus basse ? **Réponse à RQ2**
- Quel framework est le plus robuste ? **Réponse à RQ3**
- Quel framework excelle en multi-agent ? **Réponse à RQ4**
- Pour quel cas d'usage utiliser quel framework ? **Réponse à RQ5**

### Contenu minimal à inclure

1. **Réponses aux questions de recherche**
   - RQ1: Complétion (avec justification)
   - RQ2: Latence (avec justification)
   - RQ3: Robustesse (avec justification)
   - RQ4: Multi-agent (avec justification)
   - RQ5: Recommandations (avec justification)

2. **Validation/Réfutation des hypothèses**
   - H1 validée/réfutée et pourquoi
   - H2 validée/réfutée et pourquoi
   - H3 validée/réfutée et pourquoi
   - H4 validée/réfutée et pourquoi

3. **Forces et faiblesses de chaque framework**
   - LangChain: forces, faiblesses
   - CrewAI: forces, faiblesses
   - AutoGen: forces, faiblesses
   - LlamaIndex: forces, faiblesses

4. **Analyse des modes d'échec**
   - Erreurs communes
   - Cas d'usage problématiques
   - Patterns de défaillance

5. **Corrélations architecture-performance**
   - Comment l'architecture explique les résultats
   - Liens entre design et performance

### Structure LaTeX recommandée

```latex
\section{Analyse comparative}
\subsection{Réponses aux questions de recherche}
\subsection{Validation des hypothèses}
\subsection{Forces et faiblesses}
\subsection{Modes d'échec}
\subsection{Corrélations architecture-performance}
```

---

## VIII. Discussion

### Objectif de cette section

Débattre les implications, les limitations et les perspectives.

### Questions à répondre

- Quelles sont les implications pratiques des résultats ?
- Comment ces résultats aident-ils les praticiens ?
- Quelles sont les limitations de l'étude ?
- Qu'aurait-on pu améliorer ?

### Contenu minimal à inclure

1. **Implications pour la sélection de frameworks**
   - Recommandations par cas d'usage
   - Recommandations par contexte (startup, entreprise, académique)

2. **Limitations méthodologiques**
   - Limitations du design expérimental
   - Limitations de l'implémentation
   - Biais potentiels

3. **Limitations liées au modèle et aux paramètres**
   - Résultats spécifiques au modèle utilisé
   - Dépendance envers la température et les tokens
   - Généralisabilité des résultats

4. **Limitations de la reproductibilité**
   - Coûts API
   - Variabilité du LLM
   - Accès restreint aux frameworks

5. **Améliorations futures**
   - Tester avec d'autres modèles LLM
   - Augmenter le nombre de tâches
   - Tester sur du hardware différent
   - Intégrer d'autres frameworks

6. **Recommandations pour la communauté**
   - Standardiser les benchmarks
   - Partager les résultats
   - Continuer le développement

### Structure LaTeX recommandée

```latex
\section{Discussion}
\subsection{Implications pratiques}
\subsection{Limitations méthodologiques}
\subsection{Limitations des résultats}
\subsection{Améliorations futures}
\subsection{Recommandations}
```

---

## IX. Conclusion et perspectives

### Objectif de cette section

Synthétiser et conclure.

### Contenu minimal à inclure

1. **Synthèse des résultats principaux**
   - Résumé des 5 questions de recherche
   - Résumé des hypothèses validées

2. **Contributions du projet**
   - AgentBench-FR comme nouvelle ressource
   - Insights sur les frameworks
   - Méthodologie reproductible

3. **Recommandations finales**
   - Quel framework pour quel cas d'usage
   - Critères de sélection

4. **Travaux futurs**
   - Évolutions d'AgentBench-FR
   - Tester d'autres frameworks
   - Tester avec d'autres modèles
   - Cas d'usage en production

5. **Appel à la communauté**
   - Partage du benchmark
   - Collaboration
   - Améliorations

### Structure LaTeX recommandée

```latex
\section{Conclusion}
\subsection{Synthèse}
\subsection{Contributions}
\subsection{Recommandations}
\section{Travaux futurs}
```

---

## X. Références bibliographiques

### Contenu à inclure

- Documentation officielle des 4 frameworks
- Articles académiques sur les agents IA
- Benchmarks existants (si pertinents)
- Articles fondateurs (ReAct, Chain-of-Thought, etc.)
- Articles sur la récupération documentaire
- Articles sur la collaboration multi-agent

### Format LaTeX

```latex
\bibliographystyle{plain}
\bibliography{references}
```

Fichier `references.bib`:

```bibtex
@software{langchain2024,
  title={LangChain},
  author={Chase, Harrison},
  year={2024},
  url={https://www.langchain.com}
}

@paper{wei2023chain,
  title={Chain-of-Thought Prompting Elicits Reasoning in Large Language Models},
  author={Wei, Jason and others},
  journal={arXiv},
  year={2023}
}

% ... plus de références
```

---

## Structure des fichiers LaTeX pour pdflatex

### Arborescence recommandée

```
rapport/
├── main.tex                     (document principal)
├── preamble.tex                 (packages et config)
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
├── references.bib
├── build/                       (fichiers générés)
└── Makefile                     (build script)
```

### Fichier main.tex

```latex
\documentclass[12pt,a4paper]{report}
\usepackage[utf-8]{inputenc}
\usepackage[french]{babel}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}

\title{Évaluation comparative des frameworks d'agents IA:\\ LangChain, CrewAI, AutoGen et LlamaIndex}
\author{[Votre nom]}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

\input{chapters/01_introduction.tex}
\input{chapters/02_etat_art.tex}
\input{chapters/03_problematique.tex}
\input{chapters/04_methodologie.tex}
\input{chapters/05_benchmark.tex}
\input{chapters/06_resultats.tex}
\input{chapters/07_analyse.tex}
\input{chapters/08_discussion.tex}
\input{chapters/09_conclusion.tex}

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

### Compilation avec pdflatex

```bash
cd rapport/
pdflatex -interaction=nonstopmode main.tex
bibtex main.aux
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Ou avec un Makefile:

```makefile
all: main.pdf

main.pdf: main.tex references.bib $(CHAPTERS) $(FIGURES)
	pdflatex -interaction=nonstopmode main.tex
	bibtex main.aux
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex

clean:
	rm -f *.aux *.log *.bbl *.blg *.toc *.out build/*

.PHONY: all clean
```

---

## 9. Rédaction du rapport

Le rapport final doit expliquer :

1. la problématique,
2. la méthodologie,
3. la configuration technique,
4. les résultats,
5. les limites,
6. la conclusion.

Il faut aussi documenter les choix faits pendant le projet, notamment si un framework a demandé des ajustements spécifiques.

Le PDF final doit reprendre un plan clair et académique, par exemple :

1. Introduction générale,
2. État de l'art,
3. Problématique et objectifs,
4. Méthodologie expérimentale,
5. Description d'AgentBench-FR,
6. Résultats,
7. Analyse comparative,
8. Discussion,
9. Conclusion et perspectives.

## 10. Recommandations pratiques

- Commencer par un mode mock pour valider la chaîne complète avant de brancher de vraies API.
- Tester chaque adaptateur séparément avant de lancer le benchmark complet.
- Garder une structure de logs lisible et horodatée.
- Fixer les paramètres expérimentaux une seule fois avant les mesures finales.
- Documenter toute différence entre la théorie et l'implémentation.

## 11. Livrables attendus

À la fin du projet, le dépôt doit contenir :

- la documentation méthodologique,
- les tâches du benchmark,
- les prompts,
- les scripts d'exécution,
- les configurations d'exemple,
- les logs d'expérience,
- le rapport final,
- les éléments de traçabilité des décisions.

Le PDF doit être généré à partir d'un document source propre et cohérent, avec les mêmes termes que le sujet: frameworks, benchmark, AgentBench-FR, métriques et reproductibilité.

## 12. Conclusion

Ce guide donne une trajectoire complète pour réaliser le projet, depuis la préparation de l'environnement jusqu'à l'analyse finale. Il sert de base pour intégrer les API des agents, standardiser les exécutions et conserver une traçabilité suffisante pour un travail académique reproductible.