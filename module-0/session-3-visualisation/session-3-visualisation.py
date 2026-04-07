"""
Module 0 — Session 3 : Visualisation avec Matplotlib & Seaborn
==============================================================
Dataset : DVF (Demandes de Valeurs Foncières) 2023 — df_clean de session 2

Règles non-négociables :
- Titre toujours
- Labels d'axes avec unités
- set_xlim / set_ylim sur données skewed
- plt.tight_layout() avant plt.show()
- Interface orientée objet : fig, ax = plt.subplots()

Les 4 graphes fondamentaux :
  Histogramme → distribution d'une variable
  Boxplot      → comparaison de distributions par groupe
  Scatter      → relation entre deux variables (+ 3e dim par couleur)
  Heatmap      → corrélations entre variables numériques
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

sns.set_theme(style='whitegrid')

# Rechargement de df_clean depuis session 2
df_clean = pd.read_parquet(
    Path(r'C:\Users\Abd\Documents\IA_journey\module-0\session-2-pandas\df_clean.parquet')
)


# =============================================================================
# RAPPEL — Syntaxe de base des 4 graphes
# =============================================================================

# --- Histogramme ---
# fig, ax = plt.subplots(figsize=(8, 5))
# sns.histplot(data=df_clean, x='prix_m2', bins=50, ax=ax)
# ax.set_xlim(0, 10000)
# ax.set_xlabel("Prix au m² (€/m²)")
# ax.set_ylabel("Nombre de transactions")
# ax.set_title("Distribution du prix au m²")
# plt.tight_layout()
# plt.show()

# --- Boxplot ---
# fig, ax = plt.subplots(figsize=(10, 5))
# sns.boxplot(data=df_clean, x='type_local', y='prix_m2', ax=ax)
# ax.set_ylim(0, 8000)
# plt.tight_layout()
# plt.show()

# --- Scatter avec colorbar ---
# sample = df_clean.sample(2000, random_state=42)
# fig, ax = plt.subplots(figsize=(8, 5))
# sc = ax.scatter(sample['surface_reelle_bati'], sample['prix_m2'],
#                 c=sample['nombre_pieces_principales'],
#                 alpha=0.3, s=10, cmap='viridis')
# plt.colorbar(sc, ax=ax, label='Nombre de pièces')
# plt.tight_layout()
# plt.show()

# --- Heatmap corrélation ---
# colonnes = ['valeur_fonciere', 'surface_reelle_bati',
#             'nombre_pieces_principales', 'prix_m2']
# fig, ax = plt.subplots(figsize=(7, 5))
# sns.heatmap(df_clean[colonnes].corr(), annot=True, fmt='.2f',
#             cmap='coolwarm', center=0, ax=ax)
# plt.tight_layout()
# plt.show()


# =============================================================================
# EXERCICE 1 — Histogramme : Paris vs Lyon
# =============================================================================
# Question : la distribution du prix_m2 est-elle différente entre Paris et Lyon ?
#
# Observations :
# - Deux distributions quasi-disjointes : Lyon [1000-6000], Paris [6000-15000]
# - Les deux sont right-skewed (queue longue à droite) — typique des prix immo
# - Médiane Paris ~10 278€/m², Lyon ~4 179€/m² — facteur 2.5
# - Implication pour la modélisation : travailler sur log(prix_m2) plutôt
#   que prix_m2 directement (distribution log-normale plus adaptée)

df_paris = df_clean.loc[df_clean['code_departement'] == '75']
df_lyon  = df_clean.loc[df_clean['code_departement'] == '69']

mediane_paris = df_paris['prix_m2'].median()
mediane_lyon  = df_lyon['prix_m2'].median()

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(data=df_paris, x='prix_m2', bins=50, alpha=0.5, label='Paris', ax=ax)
sns.histplot(data=df_lyon,  x='prix_m2', bins=50, alpha=0.5, label='Lyon',  ax=ax)

ax.axvline(x=mediane_paris, color='blue', linestyle='--',
           label=f'Médiane Paris {mediane_paris:.0f}€')
ax.axvline(x=mediane_lyon,  color='red',  linestyle='--',
           label=f'Médiane Lyon {mediane_lyon:.0f}€')

ax.set_xlim(0, 20000)
ax.set_xlabel("Prix au m² (€/m²)")
ax.set_ylabel("Nombre de transactions")
ax.set_title("Distribution du prix au m² : Paris vs Lyon")
ax.legend()
plt.tight_layout()
plt.show()


# =============================================================================
# EXERCICE 2 — Boxplot : prix_m2 par nombre de pièces (appartements parisiens)
# =============================================================================
# Question : le prix au m² varie-t-il selon le nombre de pièces à Paris ?
#
# Observations :
# - Médiane stable entre 1 et 5 pièces (~10 000€/m²)
# - Hausse significative à partir de 6 pièces — marché du luxe
# - Variance croissante avec le nombre de pièces — marché plus hétérogène
#   sur les grands biens

paris_apparts = df_clean.loc[
    (df_clean['type_local'] == 'Appartement') &
    (df_clean['code_departement'] == '75') &
    (df_clean['nombre_pieces_principales'].between(1, 5))
]

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=paris_apparts, x='nombre_pieces_principales', y='prix_m2', ax=ax)

ax.set_ylim(0, 25000)
ax.set_xlabel("Nombre de pièces principales")
ax.set_ylabel("Prix au m² (€/m²)")
ax.set_title("Prix au m² par nombre de pièces — Appartements parisiens")
plt.tight_layout()
plt.show()


# =============================================================================
# EXERCICE 3 — Scatter : surface vs prix_m2 coloré par nombre de pièces
# =============================================================================
# Question : y a-t-il une relation entre surface et prix au m² pour les maisons ?
#
# Observations :
# - Tendance négative confirmée : plus la surface est grande, moins le prix
#   au m² est élevé (décote sur les grandes surfaces)
# - Points violets (peu de pièces) concentrés en bas à gauche
# - Points jaunes (beaucoup de pièces) à droite — surface et pièces corrélées
# - Forte concentration sous 100m² — les grandes maisons sont rares

sample = df_clean[df_clean['type_local'] == 'Maison'].sample(3000, random_state=42)

fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.scatter(
    sample['surface_reelle_bati'],
    sample['prix_m2'],
    c=sample['nombre_pieces_principales'],
    alpha=0.3, s=10, cmap='viridis'
)
plt.colorbar(sc, ax=ax, label='Nombre de pièces')

ax.set_xlim(0, 300)
ax.set_ylim(0, 15000)
ax.set_xlabel("Surface (m²)")
ax.set_ylabel("Prix au m² (€/m²)")
ax.set_title("Surface vs Prix au m² — Maisons")
plt.tight_layout()
plt.show()


# =============================================================================
# EXERCICE 4 — Heatmap : corrélations sur les appartements uniquement
# =============================================================================
# Question : les corrélations changent-elles si on segmente sur les appartements ?
#
# Comparaison avec la heatmap globale (tous biens, toutes villes) :
#
#                          Global    Appartements Paris
# surface vs prix_m2        -0.05         -0.15
# pièces  vs prix_m2        -0.21         -0.15
# valeur  vs prix_m2         0.29          0.74
# surface vs pièces         -0.02          0.82
#
# Enseignements :
# - surface vs pièces passe de -0.02 à 0.82 — cohérent, plus de pièces = plus grand
# - valeur vs prix_m2 passe de 0.29 à 0.74 — à Paris la surface varie peu,
#   donc valeur et prix/m² sont très liés
# - La segmentation révèle des structures masquées par l'hétérogénéité globale
# - Principe : toujours segmenter avant d'analyser les corrélations

colonnes = ['valeur_fonciere', 'surface_reelle_bati',
            'nombre_pieces_principales', 'prix_m2']

apparts = df_clean.loc[df_clean['type_local'] == 'Appartement']

fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(apparts[colonnes].corr(), annot=True, fmt='.2f',
            cmap='coolwarm', center=0, ax=ax)
ax.set_title("Corrélations — Appartements (toutes villes)")
plt.tight_layout()
plt.show()