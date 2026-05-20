Sujet 1 — Évaluation comparative des frameworks d'agents
IA : LangChain, CrewAI, AutoGen et LlamaIndex

Problématique
Les agents IA reposent aujourd'hui sur des frameworks hétérogènes (LangChain, CrewAI,
AutoGen, LlamaIndex) qui diffèrent considérablement dans leurs paradigmes d'orchestration,
leurs mécanismes d'appel d'outils et leurs performances. L'absence de benchmarks standardisés
et reproductibles empêche les praticiens et chercheurs de choisir objectivement le framework le
plus adapté à leur contexte applicatif. Cette recherche vise à combler ce vide en proposant une
méthodologie d'évaluation systématique couvrant la latence, la fiabilité, la complétude des tâches
et la consommation de ressources.
Mots-clés
Agent benchmarking, Tool calling, ReAct pattern, LangGraph, CrewAI, AutoGen, LlamaIndex,
orchestration
Abstract
The proliferation of agentic AI frameworks has created an urgent need for rigorous
comparative evaluation methodologies. This paper presents a systematic benchmark
study of four leading agentic frameworks — LangChain, CrewAI, AutoGen, and
LlamaIndex — across standardized task suites involving tool use, multi-step reasoning,
and collaborative agent execution. We introduce AgentBench-FR, an open evaluation
suite comprising 120 tasks across five difficulty levels, and measure framework
performance along four dimensions: task completion rate, average latency, resource
consumption, and error resilience. Our results reveal significant performance disparities:
AutoGen achieves the highest completion rate on multi-agent tasks (83.4%) while
LangGraph demonstrates superior latency in single-agent pipelines. We further analyze
failure modes and propose architectural guidelines for selecting the appropriate framework

Sujets de recherche IA Agentique — Page 2

based on application constraints. Our benchmark suite is publicly released to foster
reproducible research in agentic AI.