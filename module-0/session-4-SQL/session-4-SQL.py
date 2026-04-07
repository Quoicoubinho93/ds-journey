import sqlite3
import statistics
import pandas as pd
from pathlib import Path

# Chargement de df_clean
df_clean = pd.read_parquet(
    Path(r'C:\Users\Abd\Documents\IA_journey\module-0\session-2-pandas\df_clean.parquet')
)

# Création de la base SQLite en mémoire
conn = sqlite3.connect(':memory:')

class MedianAggregate:
    def __init__(self):
        self.values = []
    def step(self, value):
        if value is not None:
            self.values.append(value)
    def finalize(self):
        return statistics.median(self.values) if self.values else None

conn.create_aggregate("MEDIAN", 1, MedianAggregate)
df_clean.to_sql('transactions', conn, index=False, if_exists='replace')

# Fonction utilitaire — exécute une requête et retourne un DataFrame
def query(sql):
    return pd.read_sql_query(sql, conn)


# # Sélection simple
# print(query("""
#     SELECT type_local, valeur_fonciere, prix_m2
#     FROM transactions
#     LIMIT 5
# """))

# # Filtrage — équivalent de .loc[]
# print(query("""
#     SELECT *
#     FROM transactions
#     WHERE code_departement = '75'
#       AND type_local = 'Appartement'
#       AND prix_m2 > 5000
#     LIMIT 10
# """))

# # Agrégation — équivalent de .groupby()
# print(query("""
#     SELECT   type_local,
#              COUNT(*)        AS nb_transactions,
#              AVG(prix_m2)    AS prix_m2_moyen,
#              MEDIAN(prix_m2) AS prix_m2_median
#     FROM     transactions
#     GROUP BY type_local
#     ORDER BY prix_m2_moyen DESC
# """))

# # HAVING — filtre sur l'agrégat (pas sur les lignes brutes)
# print(query("""
#     SELECT   code_departement,
#              COUNT(*) AS nb_transactions,
#              AVG(prix_m2) AS prix_moyen
#     FROM     transactions
#     GROUP BY code_departement
#     HAVING   COUNT(*) > 1000
#     ORDER BY prix_moyen DESC
#     LIMIT    10
# """))


# Crée une deuxième table pour l'exemple
df_regions = pd.DataFrame({
    'code_departement': ['75', '69', '13', '33', '06'],
    'region':          ['Île-de-France', 'Auvergne-Rhône-Alpes',
                        'PACA', 'Nouvelle-Aquitaine', 'PACA']
})
df_regions.to_sql('regions', conn, index=False, if_exists='replace')

# # INNER JOIN — garde uniquement les correspondances
# print(query("""
#     SELECT   t.code_departement,
#              r.region,
#              COUNT(*)     AS nb_transactions,
#              AVG(t.prix_m2) AS prix_moyen
#     FROM     transactions t
#     JOIN     regions r ON t.code_departement = r.code_departement
#     GROUP BY t.code_departement, r.region
#     ORDER BY prix_moyen DESC
# """))

# # LEFT JOIN — garde toutes les lignes de la table gauche
# print(query("""
#     SELECT t.code_departement, r.region
#     FROM   transactions t
#     LEFT JOIN regions r ON t.code_departement = r.code_departement
#     LIMIT 10
# """))

# print(query("""
#     SELECT code_departement,
#            prix_m2,
#            RANK() OVER (
#                PARTITION BY code_departement
#                ORDER BY prix_m2 DESC
#            ) AS rang_dans_dept
#     FROM transactions
#     WHERE type_local = 'Appartement'
#     LIMIT 20
# """)
# )


# print(query("""
#         SELECT   COUNT(*) AS nb_transactions,
#                  AVG(prix_m2) AS prix_moyen,
#                  type_local  
#         FROM     transactions
#         GROUP BY type_local
#         ORDER BY prix_moyen DESC
# """)
# )

# print(query("""
#         SELECT   COUNT(*) AS nb_transactions,
#                  code_departement
#         FROM     transactions
#         WHERE    type_local = 'Maison'
#         GROUP BY code_departement
#         ORDER BY nb_transactions DESC
#         LIMIT    5
# """)
# )

# print(query("""
#         SELECT   MEDIAN(prix_m2) AS prix_m2_median,
#                  nombre_pieces_principales
#         FROM     transactions
#         WHERE    type_local = 'Appartement' AND code_departement = '75'
#         GROUP BY nombre_pieces_principales
#         ORDER BY nombre_pieces_principales ASC
# """)
# )
            

# Crée d'abord cette table dans SQLite :
df_pop = pd.DataFrame({
    'code_departement': ['75', '69', '13', '33', '06',
                         '31', '44', '67', '59', '76'],
    'population':       [2161000, 1418000, 1043000, 1623000, 1081000,
                         1362000, 1429000, 1125000,  2604000, 1254000]
})
df_pop.to_sql('population', conn, index=False, if_exists='replace')

# Q1 : pour chaque département de la table population,
#       affiche le nombre de transactions et le prix_m2 moyen
#       utilise un LEFT JOIN pour garder tous les départements
#       même ceux sans transactions dans la table DVF


print(query("""
        SELECT  p.code_departement, 
                COUNT(*) AS nb_transactions,
                AVG(t.prix_m2) AS prix_m2_moyen
        FROM    population p
        LEFT JOIN transactions t ON p.code_departement = t.code_departement
        GROUP BY p.code_departement  
""")
)

print(query("""
    SELECT *
    FROM transactions
    WHERE code_departement = '67'
"""))



# Q2 : calcule le prix_m2 moyen par habitant
#       (prix_m2_moyen / population * 1000)
#       pour les 10 départements les plus chers au m²
#       (indice : fais le calcul dans le SELECT après la jointure)


# print(query("""
#         SELECT   t.code_departement,
#                  AVG(prix_m2) / p.population * 1000 AS prix_m2_moyen_par_habitant
#         FROM     transactions t
#         JOIN     population p ON t.code_departement = p.code_departement
#         GROUP BY t.code_departement
#         ORDER BY prix_m2_moyen_par_habitant DESC
#         LIMIT    10
               
#         """)
#     )


print(query("""
        WITH medians AS (
            SELECT code_departement,
                   MEDIAN(prix_m2) AS prix_m2_median
            FROM   transactions
            WHERE  type_local = 'Appartement'
            GROUP BY code_departement
        )
        SELECT t.code_departement,
               t.prix_m2,
               m.prix_m2_median AS prix_m2_median_par_dept,
               t.prix_m2 - m.prix_m2_median AS ecart_au_prix_m2_median
        FROM   transactions t
        JOIN   medians m ON t.code_departement = m.code_departement
        WHERE  t.type_local = 'Appartement'
        LIMIT 20
        """)
)



            

