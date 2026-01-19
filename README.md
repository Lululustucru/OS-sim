# OS-Sim — Ordonnanceur Round Robin (Python)

## Présentation
Ce projet implémente une **simulation d’ordonnanceur de système d’exploitation** en Python, basée sur l’algorithme **Round Robin (RR)** avec prise en compte de **bursts CPU et entrées/sorties (I/O)**.

La simulation est **discrète (tick-based)** et reproduit le cycle de vie complet des processus, depuis leur admission jusqu’à leur terminaison, tout en générant une **trace d’exécution CPU** et un **diagramme de Gantt textuel**.

L’objectif est de démontrer une **compréhension concrète des mécanismes d’ordonnancement des OS**, ainsi qu’une conception logicielle claire et extensible.

---

## Fonctionnalités principales
- Ordonnancement **Round Robin préemptif** avec quantum configurable
- Simulation **pas à pas (ticks discrets)**
- Modélisation explicite des états : NEW, READY, RUNNING, BLOCKED, FINISHED
- Gestion réaliste des **bursts CPU / I/O**
- I/O **non bloquantes pour le CPU**
- Génération automatique :
  - d’une trace CPU
  - d’un Gantt textuel compressé

---

## Modèle de processus
Chaque processus est représenté par une structure de données proche d’un **Process Control Block (PCB)** :
- `pid` : identifiant unique
- `arrival_time` : instant d’admission
- `bursts` : séquence ordonnée de bursts CPU et I/O
- `remaining_in_burst` : durée restante du burst courant
- `burst_index` : index du burst courant
- `blocked_until` : instant de fin d’I/O
- `start_time` : premier accès CPU (temps de réponse)
- `finish_time` : fin d’exécution (turnaround)

---

## Architecture de l’ordonnanceur
La simulation repose sur quatre structures distinctes :
- **Incoming list** : processus non encore arrivés (triés par temps d’arrivée)
- **Ready queue (FIFO)** : processus prêts à être exécutés
- **Blocked list** : processus en attente d’I/O
- **Running process** : processus actuellement sur le CPU

Le quantum est géré via un **compteur par dispatch (`quantum_left`)**, garantissant un comportement Round Robin correct sans compteur global ambigu.

---

## Déroulement de la simulation (par tick)
À chaque unité de temps, la simulation suit l’ordre suivant :
1. **Admission des processus**
2. **Gestion des fins d’I/O**
3. **Dispatch** (si CPU libre)
4. **Exécution CPU (1 tick)**
5. **Transitions d’état** :
   - Fin de burst CPU → BLOCKED (I/O) ou FINISHED
   - Expiration du quantum → préemption (retour en READY)
   - Sinon → poursuite de l’exécution

---

## Sorties produites
- **Trace CPU** : liste des PID exécutés (ou `IDLE`) à chaque tick
- **Diagramme de Gantt textuel** (compressé), par exemple :
  ```
  [0–2] P1
  [2–4] P2
  [4–6] IDLE
  ```
- **Indicateurs par processus** :
  - Temps de réponse
  - Turnaround time

---

## Points techniques démontrés
- Séparation claire des états d’ordonnancement
- Gestion correcte de la préemption
- Modélisation fidèle des I/O non bloquantes
- Simulation événementielle déterministe
- Code lisible et structuré (dataclasses, logique modulaire)

---

## Limites et pistes d’amélioration
- Calcul précis du **waiting time** (temps passé uniquement en READY)
- Autres politiques d’ordonnancement : FCFS, SJF/SRTF, priorités, MLFQ
- Ajout d’un **seed** pour des simulations reproductibles
- Statistiques globales (utilisation CPU, throughput)
- Visualisation graphique du Gantt

---

## Objectif du projet
Projet de **simulation système** démontrant :
- la compréhension des algorithmes d’ordonnancement
- la modélisation de transitions d’état complexes
- une conception logicielle claire et extensible

Pertinent pour des postes en :
- systèmes embarqués
- logiciel bas niveau
- performance et modélisation
- ingénierie logicielle orientée systèmes
