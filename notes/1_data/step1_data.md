# Étape 1 : Extraction et Préparation des Données (Classique)

## Contexte
La finance décentralisée (DeFi) repose sur des transactions transparentes et accessibles via des blockchains publiques. Ces transactions génèrent un volume important de données brutes, disponibles sur des plateformes comme Uniswap et Aave. L’extraction et la préparation de ces données sont des étapes cruciales pour analyser les comportements des utilisateurs.

## Problématique
Les données transactionnelles des applications DeFi sont souvent massives, non structurées et complexes.  
Comment collecter, nettoyer et transformer ces données pour en tirer des informations exploitables tout en respectant les contraintes de qualité et de format ?

## Objectif
- Obtenir un jeu de données structuré, propre et prêt à l’analyse.  
- Préparer les données pour des étapes ultérieures comme le clustering ou l’optimisation (normalisation, réduction de dimension, etc.).

## Contraintes
- Volume important de données à gérer, pouvant poser des problèmes de mémoire ou de temps d'exécution.
- Accès aux données via des APIs (Dune Analytics, Etherscan) qui peuvent avoir des limites de requêtes ou des restrictions d’utilisation.
- Nécessité de garantir la qualité des données (ex : suppression des doublons, gestion des données manquantes).

---

## ToDoList
1. **Collecte des données** :
   - [ ] Utiliser les APIs disponibles pour récupérer les transactions des principales plateformes DeFi (Uniswap, Aave).
   - [ ] Automatiser le processus de récupération des données si possible.
   
2. **Nettoyage des données** :
   - [ ] Supprimer les transactions erronées, incomplètes ou redondantes.
   - [ ] Vérifier la cohérence des formats (dates, montants, etc.).

3. **Transformation des données** :
   - [ ] Extraire les informations pertinentes (fréquence des transactions, montants, types de tokens, etc.).
   - [ ] Convertir les données au format nécessaire pour l’analyse (ex : DataFrame avec pandas).

4. **Prétraitements classiques** :
   - [ ] Effectuer une normalisation des données pour réduire l’échelle des valeurs (si nécessaire).
   - [ ] Réduire la dimensionnalité si le nombre de variables est trop élevé (PCA, etc.).

5. **Vérification** :
   - [ ] Contrôler la qualité du jeu de données final.
   - [ ] Tester la compatibilité avec les outils d’analyse des étapes suivantes.
