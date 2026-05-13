import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================

st.set_page_config(
    page_title="Analyse du Changement Climatique en Afrique",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Analyse du Changement Climatique en Afrique")
st.markdown("Analyse exploratoire des données climatiques africaines avec Streamlit.")

# ==========================================
# DESCRIPTION DU JEU DE DONNÉES
# ==========================================
st.markdown(
    """
## 📘 Description du jeu de données

Ce jeu de données contient des informations climatiques collectées dans plusieurs pays africains sur plusieurs décennies.

Les principales variables étudiées sont :

- **DATE** : date de l’observation climatique,
- **COUNTRY** : pays africain concerné,
- **PRCP** : quantité de précipitations enregistrée,
- **TAVG** : température moyenne,
- **TMIN** : température minimale,
- **TMAX** : température maximale.

L’objectif de cette analyse est de :

- observer l’évolution des températures en Afrique,
- comparer les changements climatiques entre plusieurs pays,
- analyser les tendances climatiques au fil du temps,
- étudier la relation entre température et précipitations.

Cette étude permet également de mieux comprendre les impacts potentiels du réchauffement climatique sur le continent africain.
"""
)

# ==========================================
# CHARGEMENT DES DONNÉES
# ==========================================

@st.cache_data

def load_data():
    df = pd.read_csv("../data/Africa_climate_change.csv")

    # Gestion des valeurs manquantes
    df['PRCP'] = df['PRCP'].fillna(df['PRCP'].median())

    df['TMIN'] = df['TMIN'].interpolate()
    df['TMAX'] = df['TMAX'].interpolate()

    df['TAVG'] = df['TAVG'].fillna(
        (df['TMAX'] + df['TMIN']) / 2
    )

    # Suppression ligne 20
    df = df.drop(index=20)

    # Conversion date
    df['DATE'] = pd.to_datetime(df['DATE'])

    return df


# Charger les données

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Paramètres")

show_data = st.sidebar.checkbox("Afficher les données")

# ==========================================
# AFFICHAGE DES DONNÉES
# ==========================================
csv_genere = df.to_csv(index=False)
st.download_button(
    label="Download the dataset",
    data=csv_genere,
    file_name="Africa_climate_change.csv"
)
if show_data:
    st.subheader("📄 Aperçu des données")
    st.dataframe(df.head())

    st.subheader("📌 Informations sur le dataset")
    st.write(df.info())

    st.subheader("❌ Valeurs manquantes")
    st.write(df.isnull().sum())

# ==========================================
# GRAPHIQUE 1
# ÉVOLUTION TEMPÉRATURE TUNISIE VS CAMEROUN
# ==========================================

st.header("📈 Évolution de la température moyenne")

# Filtrer les pays

df_filtre = df[df["COUNTRY"].isin(["Tunisia", "Cameroon"])]

# Extraire l'année

df_filtre = df_filtre.assign(
    Year=df_filtre["DATE"].dt.year
)

# Moyenne annuelle

df_grouped = (
    df_filtre
    .groupby(["COUNTRY", "Year"])["TAVG"]
    .mean()
    .reset_index()
)

# Création graphique

fig1, ax1 = plt.subplots(figsize=(10, 5))

for country in df_grouped["COUNTRY"].unique():
    data = df_grouped[df_grouped["COUNTRY"] == country]

    ax1.plot(
        data["Year"],
        data["TAVG"],
        label=country
    )

ax1.set_title(
    "Évolution de la température moyenne (Tunisie vs Cameroun)"
)

ax1.set_xlabel("Année")
ax1.set_ylabel("Température moyenne (°F)")
ax1.legend()
ax1.grid(True)
ax1.set_xlim(1980, 2005)

st.pyplot(fig1)

# ==========================================
# HISTOGRAMMES SENEGAL
# ==========================================

st.header("🇸🇳 Distribution des températures au Sénégal")

# Filtrer Sénégal

df_sn = df[df["COUNTRY"] == "Senegal"].copy()

# Extraire l'année

df_sn["Year"] = df_sn["DATE"].dt.year

# Séparation des périodes

df1 = df_sn[
    (df_sn["Year"] >= 1980) &
    (df_sn["Year"] < 2000)
]


df2 = df_sn[
    (df_sn["Year"] >= 2000) &
    (df_sn["Year"] <= 2023)
]

# Histogramme

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.hist(
    df1["TAVG"],
    bins=30,
    alpha=0.5,
    label="1980-2000"
)

ax2.hist(
    df2["TAVG"],
    bins=30,
    alpha=0.5,
    label="2000-2023"
)

ax2.set_title("Distribution des températures au Sénégal")
ax2.set_xlabel("Température moyenne (°F)")
ax2.set_ylabel("Fréquence")
ax2.legend()

st.pyplot(fig2)

# ==========================================
# TEMPÉRATURE MOYENNE PAR PAYS
# ==========================================

st.header("🌡️ Température moyenne par pays")

# Calcul moyenne

df_avg = (
    df.groupby("COUNTRY")["TAVG"]
    .mean()
    .sort_values()
)

# Graphique barres

fig3, ax3 = plt.subplots(figsize=(12, 5))

ax3.bar(df_avg.index, df_avg.values)

ax3.set_title("Température moyenne par pays")
ax3.set_ylabel("Température moyenne (°F)")
ax3.set_xlabel("Pays")

plt.xticks(rotation=45)

st.pyplot(fig3)

# ==========================================
# TOP 10 PAYS LES PLUS CHAUDS
# ==========================================

st.header("🔥 Top 10 des pays les plus chauds")

# Tri décroissant

df_hot = (
    df.groupby("COUNTRY")["TAVG"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Graphique

fig4, ax4 = plt.subplots(figsize=(10, 5))

ax4.bar(df_hot.index, df_hot.values)

ax4.set_title("Pays les plus chauds")
ax4.set_ylabel("Température moyenne (°F)")
ax4.set_xlabel("Pays")

plt.xticks(rotation=45)

st.pyplot(fig4)

# ==========================================
# RELATION TEMPÉRATURE ET PRÉCIPITATIONS
# ==========================================

st.header("🌧️ Relation entre température et précipitations")

fig5, ax5 = plt.subplots(figsize=(10, 5))

ax5.scatter(
    df["PRCP"],
    df["TAVG"],
    alpha=0.3
)

ax5.set_xlabel("Précipitations")
ax5.set_ylabel("Température")
ax5.set_title("Relation entre température et précipitations")

st.pyplot(fig5)

# ==========================================
# STATISTIQUES DESCRIPTIVES
# ==========================================

st.header("📊 Statistiques descriptives")

st.dataframe(df.describe())

# ==========================================
# INTERPRÉTATIONS DES ANALYSES
# ==========================================

st.header("Interprétation des résultats")

st.subheader("Température moyenne : Tunisie vs Cameroun de 1980 à 2005")
st.markdown(
    """
- Le graphique montre l’évolution des températures moyennes annuelles.
- Une tendance haussière peut indiquer les effets du réchauffement climatique.
- Cameroun (Bleu) presente une temperature moyenne nettement plus elevee, se situant globalement entre 77.5°F et 82.5°F, C'est coherant avec un climat tropical humide tandis 
la Tunisie (Orange) plus fraiche en moyenne, oscillant entre 65°F et 70°F, ce aui reflete son climat mediterraneen/aride .

    """
)

st.subheader("Distribution des températures au Sénégal")
st.markdown(
    """
- Les histogrammes permettent de comparer les températures entre deux périodes.
- Si les températures récentes (2000-2023) sont plus élevées, cela suggère une augmentation climatique.
- Une concentration des valeurs vers les températures élevées peut révéler un réchauffement progressif.
    """
)

st.subheader("Température moyenne par pays")
st.markdown(
    """
- Certains pays affichent des températures moyennes plus importantes que d’autres.
- Les différences climatiques dépendent de plusieurs facteurs :
    - position géographique,
    - proximité de l’océan,
    - désertification,
    - altitude.
    """
)

st.subheader(" Relation entre température et précipitations")
st.markdown(
    """
- Le nuage de points montre la relation entre les précipitations et la température.
- Une faible corrélation signifie que les précipitations n’expliquent pas entièrement les variations de température.
- Les changements climatiques sont influencés par plusieurs variables environnementales.
    """
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown(
    "Projet Streamlit — Analyse du changement climatique en Afrique 🌍"
)





