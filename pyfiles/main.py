import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("/Users/alphaamadoudiallo/Desktop/EDA & Visualisation/Changement climatique en Afrique/data/Africa_climate_change.csv")

df.info()
df.isnull().sum()

df['PRCP'] = df['PRCP'].fillna(df['PRCP'].median())

# interpolation sert à remplir les valeurs manquantes (NaN)
# en estimant leur valeur à partir des données voisines.
df['TMIN'] = df['TMIN'].interpolate()
df['TMAX'] = df['TMAX'].interpolate()

df['TAVG'] = df['TAVG'].fillna((df['TMAX'] + df['TMIN']) / 2)

#Suppression de la ligne 20
df = df.drop(index=20)

#Graphique lineaire
#illustrant les fluctuations moyennes de température en Tunisie et au Cameroun

#Conversion de la date
df["DATE"] = pd.to_datetime(df["DATE"])

#Filtrer les pays
df_filtre = df[df["COUNTRY"].isin(["Tunisia", "Cameroon"])]
#Extraire l'année
df_filtre = df_filtre.assign(Year=df_filtre["DATE"].dt.year)
#Calculer la température moyenne annuelle par pays
df_grouped = df_filtre.groupby(["COUNTRY", "Year"])["TAVG"].mean().reset_index()

#Tracer le graphique
plt.figure()
for country in df_grouped["COUNTRY"].unique():
    data = df_grouped[df_grouped["COUNTRY"] == country]
    plt.plot(data["Year"], data["TAVG"], label=country)
#Personnalisation
plt.title("Évolution de la température moyenne (Tunisie vs Cameroun)")
plt.xlabel("Année")
plt.ylabel("Température moyenne (°F)") # °F = °Fahrenheit
plt.legend()
plt.grid()
plt.xlim(1980, 2005)  # zoom sur les années
#Affichage
plt.show()


#histogrammes pour représenter la distribution des températures au Sénégal entre 1980 et 2000,
#puis entre 2000 et 2023 (sur la même figure)

#Filtrer Senegal
df_sn = df[df["COUNTRY"] == "Senegal"].copy()
df_sn["Year"] = df_sn["DATE"].dt.year
#Separer les periodes
df1 = df_sn[(df_sn["Year"] >= 1980) & (df_sn["Year"] < 2000)]
df2 = df_sn[(df_sn["Year"] >= 2000) & (df_sn["Year"] <= 2023)]

#Tracer l'histogramme
plt.figure()
plt.hist(df1["TAVG"], bins=30, alpha=0.5, label="1980-2000")
plt.hist(df2["TAVG"], bins=30, alpha=0.5, label="2000-2023")

#Personnalisation
plt.title("Distribution Temperature au Senegal")
plt.xlabel("Température moyenne (°F)")
plt.ylabel("Frequence")
plt.legend()

#Affichage
plt.show()



#Température moyenne par pays
df_avg = df.groupby("COUNTRY")["TAVG"].mean().sort_values()
plt.figure(figsize=(10,5))
df_avg.plot(kind="bar")
plt.title("Température moyenne par pays")
plt.ylabel("Température moyenne (°F)")
plt.xlabel("Pays")
plt.xticks(rotation=45)
plt.show()


#Pays les plus chauds
df_avg = df.groupby("COUNTRY")["TAVG"].mean().sort_values(ascending=False)
df_avg.head(10).plot(kind="bar")
plt.title("Pays les plus chauds")
plt.show()

#Relation température et précipitations
plt.scatter(df["PRCP"], df["TAVG"], alpha=0.3)
plt.xlabel("Précipitations")
plt.ylabel("Température")
plt.show()