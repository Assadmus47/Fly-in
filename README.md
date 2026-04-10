# 🚁 Fly-in — TODO List & Estimations

## ⏱️ Estimation globale : 4 à 7 jours de travail

---

## 📦 Étape 0 — Setup du projet
**Durée estimée : ~1h**

- [ ] Créer la structure des fichiers/dossiers
- [ ] Créer le `Makefile` (rules : install, run, debug, clean, lint)
- [ ] Créer le `requirements.txt` (ou `pyproject.toml`)
- [ ] Créer le `.gitignore`
- [ ] Créer le `README.md` (structure vide à remplir progressivement)
- [ ] Initialiser le venv

---

## 📂 Étape 1 — Le Parser
**Durée estimée : ~4h**

- [ ] Lire et parser la ligne `nb_drones`
- [ ] Parser les zones `start_hub`, `end_hub`, `hub` avec coordonnées et metadata
- [ ] Parser les connexions `connection: zone1-zone2 [metadata]`
- [ ] Gérer les commentaires (`#`)
- [ ] Valider le format : unicité des noms, types valides, valeurs positives
- [ ] Gérer les erreurs de parsing avec messages clairs (ligne + cause)
- [ ] Tests manuels sur le fichier d'exemple + créer ses propres fichiers de test

---

## 🏗️ Étape 2 — Les structures de données (Graph OOP)
**Durée estimée : ~3h**

- [ ] Classe `Zone` (nom, coords, type, couleur, max_drones, drones actuels)
- [ ] Classe `Connection` (zone1, zone2, max_link_capacity)
- [ ] Classe `Graph` (zones, connexions, méthodes de navigation)
  - [ ] Méthode : récupérer les voisins d'une zone
  - [ ] Méthode : vérifier si une zone est accessible (pas blocked, capacité dispo)
- [ ] Classe `Drone` (id, zone actuelle, état, chemin prévu)
- [ ] **Contrainte importante** : aucune lib graph externe (pas de networkx, graphlib, etc.)

---

## 🔍 Étape 3 — L'algorithme de pathfinding
**Durée estimée : ~5h**

- [ ] Implémenter un BFS/Dijkstra "from scratch" pour trouver le chemin le plus court
  - [ ] Prendre en compte les coûts par type de zone (normal=1, restricted=2, priority=1)
  - [ ] Ignorer les zones `blocked`
  - [ ] Préférer les zones `priority`
- [ ] Trouver plusieurs chemins disjoints (pour distribuer les drones)
- [ ] Gérer l'attribution des chemins aux drones (quel drone prend quel chemin)

---

## ⚙️ Étape 4 — Le moteur de simulation (turn-by-turn)
**Durée estimée : ~6h**  ← partie la plus complexe

- [ ] Logique de simulation tour par tour
- [ ] Chaque drone peut : avancer, attendre, ou entrer sur une connexion vers une zone restricted
- [ ] Appliquer les règles de capacité des zones (`max_drones`)
- [ ] Appliquer les règles de capacité des connexions (`max_link_capacity`)
- [ ] Gérer les zones restricted (2 tours, le drone doit OBLIGATOIREMENT arriver le tour suivant)
- [ ] Gérer les conflits (deux drones veulent la même zone)
- [ ] Drones qui quittent une zone libèrent la capacité pour le même tour
- [ ] Simulation se termine quand tous les drones sont arrivés à `end_hub`

---

## 📤 Étape 5 — Output de la simulation
**Durée estimée : ~1h**

- [ ] Afficher chaque tour sur une ligne
- [ ] Format : `D1-zone D2-zone ...`
- [ ] Pour les drones sur connexion vers restricted : `D1-connexion`
- [ ] Ne pas afficher les drones qui n'ont pas bougé
- [ ] Ne plus afficher les drones déjà arrivés

---

## 🎨 Étape 6 — Représentation visuelle
**Durée estimée : ~3h**

- [ ] Affichage coloré dans le terminal (avec `colorama` ou codes ANSI)
  - [ ] Couleurs des zones selon leur type
  - [ ] Positions des drones visibles
- [ ] (Optionnel bonus) Interface graphique avec `matplotlib` ou `pygame`

---

## 📊 Étape 7 — Optimisation de l'algorithme
**Durée estimée : ~3h**

- [ ] Vérifier les performances sur les cartes easy (≤ 6-8 turns)
- [ ] Vérifier les performances sur les cartes medium (≤ 12-20 turns)
- [ ] Vérifier les performances sur les cartes hard (≤ 35-60 turns)
- [ ] Améliorer la distribution des drones sur les chemins
- [ ] Gérer les deadlocks (drones bloqués mutuellement)

---

## 🧪 Étape 8 — Tests & robustesse
**Durée estimée : ~2h**

- [ ] Créer ses propres fichiers de cartes pour les edge cases
  - [ ] Carte avec zone blocked
  - [ ] Carte avec zone restricted
  - [ ] Carte avec max_link_capacity
  - [ ] Carte sans chemin possible
  - [ ] Fichier mal formé (parsing errors)
- [ ] Tests avec pytest ou unittest

---

## 📝 Étape 9 — Finalisation
**Durée estimée : ~2h**

- [ ] Compléter le `README.md`
  - [ ] Description du projet
  - [ ] Instructions d'installation/exécution
  - [ ] Description de l'algorithme choisi
  - [ ] Documentation de la représentation visuelle
  - [ ] Ressources + comment l'IA a été utilisée
- [ ] Vérifier que `flake8` et `mypy` passent sans erreurs
- [ ] Vérifier que le `Makefile` fonctionne correctement
- [ ] Relecture du code + docstrings

---

## 🏆 Bonus (optionnel, après le mandatory)
**Durée estimée : +2h si tu y vas**

- [ ] Atteindre exactement les benchmarks de performance pour toutes les cartes
- [ ] Résoudre la carte "The Impossible Dream" (25 drones) en < 45 tours

---

## 🗓️ Planning suggéré

| Jour | Étapes |
|------|--------|
| Jour 1 | Setup (0) + Parser (1) |
| Jour 2 | Structures de données (2) + début Pathfinding (3) |
| Jour 3 | Fin Pathfinding (3) + début Simulation (4) |
| Jour 4 | Fin Simulation (4) + Output (5) |
| Jour 5 | Visuel (6) + Tests (8) |
| Jour 6 | Optimisation (7) + Finalisation (9) |
| Jour 7 | Buffer (corrections, bonus, relecture) |

---

> 💡 **Clé du projet** : La partie la plus difficile est l'étape 4 (moteur de simulation).
> Le pathfinding seul c'est connu (BFS/Dijkstra), mais coordonner plusieurs drones
> simultanément avec toutes les contraintes de capacité, c'est là que ça se complique.
