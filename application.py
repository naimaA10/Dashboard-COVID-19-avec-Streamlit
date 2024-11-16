"""Projet Covid avec Streamlit."""

import datetime
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def clean_csv(path):
    """
    Retourne un DataFrame avec les collones qui nous interesse.

    Parameters:
        path (str) : le chemin vers le document.
        csv avec les données d'interet.
    Returns:
        dflines (DataFrame): un data frame.
    """
    data = pd.read_csv(path)

    # dfCol contient que les colonnes qui nous intéresse
    dfcol = data.loc[:, [
        "location", "date", "total_cases", "new_cases_smoothed",
        "total_deaths", "new_deaths_smoothed", ]]

    # Garder les lignes utiles :
    dflines = dfcol.query(
        "location == 'France' | location == 'Spain' "
        "| location == 'Germany' | location == 'Sweden' "
        "| location == 'England' | location == 'Italy'")
    return dflines


def select_df_country(data, country):
    """
    Retourne un DataFrame avec uniquement les rangs de pays country.

    Parameters:
        data (DataFrame): dataframe d'interêt.
        country (str).
    Returns:
        data (DataFrame): un sous data frame.
    """
    country = switch_country_english(country)
    # Mauvais pays (ne devrait pas arriver)
    if data.columns is None:
        return None
    return data[data["location"] == country]


def select_df_dates(data, date1, date2):
    """
    Retourne un DataFrame avec les valeurs entre date1 et date2.

    Parameters:
        data (DataFrame): Dataframe d'interêt.
        date1 (datetime.date): Date de début.
        date2 (datetime.date): Date de fin.
    Returns:
        data (DataFrame): Un sous data frame.
    """
    date1 = str(date1)
    date2 = str(date2)
    if date1 > date2:
        return None  # Erreur la date1 doit se trouver avant date2
    data = data[data["date"] >= date1]
    data = data[data["date"] <= date2]
    return data


# Conversion des noms en anglais pour la recherche dans le dataset
def switch_country_english(country):
    """
    Retourne la traduction en anglais du pays.

    Parameters:
        country (str): pays en francais.
    Returns:
        english (str): pays en anglais.
    """
    english = ""
    if country == "France":
        english = "France"
    if country == "Allemagne":
        english = "Germany"
    if country == "Suède":
        english = "Sweden"
    if country == "Angleterre":
        english = "England"
    if country == "Italie":
        english = "Italy"
    if country == "Espagne":
        english = "Spain"
    return english


def switch_type_graph_english(type_plot):
    """
    Retourne la traduction en anglais du type de colonne voulue.

    Parameters:
        type_plot (str): Type de colonne en francais.
    Returns:
        english (str): Pays en anglais.
    """
    english = ""
    if type_plot == "Nouveaux cas":
        english = "new_cases_smoothed"
    if type_plot == "Nouveaux décès":
        english = "new_deaths_smoothed"
    if type_plot == "Nombre total de cas":
        english = "total_cases"
    if type_plot == "Nombre total de décès":
        english = "total_deaths"
    return english


def plot_covid(data, colour, country, dates, to_plot):
    """
    Retourne la figure graphique.

    Parameters:
        data (DataFrame): DataFrame d'interet filtré.
        colour (str) : Code couleur.
        country (str) : Pays d'interet.
        date1 (datetime.date): Date de début.
        date2 (datetime.date): Date de fin.
    Returns:
        plot (figure): Plot généré.
    """
    fig = plt.figure(figsize=(10, 10))
    plt.set_loglevel('WARNING')
    plt.plot(
        data['date'],
        data[switch_type_graph_english(to_plot)], color=colour)
    plt.title(
        f"Evolution de {to_plot} de COVID 19 " +
        f"en {country} du {dates[0]} au {dates[1]}")
    plt.xlabel("Temps")
    plt.ylabel(f"{to_plot}")
    # Nombre de graduations :
    plt.xticks(np.arange(0, len(data['date']), 30), rotation="vertical")
    plt.savefig('covid_graph.png')
    return fig


if __name__ == '__main__':
    # Lecture du fichier CSV
    df = clean_csv(
        "https://raw.githubusercontent.com/owid/" +
        "covid-19-data/master/public/data/owid-covid-data.csv")
    # Elements graphiques :

    st.title("PyCovid")

    # Barre des paramètres :

    st.sidebar.header("Paramètres souhaités: ")
    pays = st.sidebar.selectbox(
        label="Choisissez un pays",
        options=[
            "France", "Italie",
            "Allemagne", "Suède",
            "Espagne", "Angleterre"],
        key="country")

    color = st.sidebar.color_picker(
        label="Choisissez la couleur de la courbe",)
    date_deb = st.sidebar.date_input(
        "Choisissez la date de début : ",
        datetime.date(2022, 1, 1))

    date_fin = st.sidebar.date_input(label="Choisissez la date de fin :")

    # lancer la fonction globale d'ici

    # Main Panel :
    st.write(
        'Bienvenue dans PyCovid.'
        'Cette application vous permet de visualiser '
        'les derniers chiffres relatifs à la Covid 19.')
    options_graphs = st.sidebar.selectbox(
        label='Choississez le type de graphe',
        options=[
            'Nouveaux cas',
            'Nouveaux décès',
            'Nombre total de cas',
            'Nombre total de décès'])

    # Affichage du graphique
    graph = plot_covid(select_df_dates(
        select_df_country(df, pays),
        date_deb, date_fin),
        colour=color, dates=(date_deb, date_fin),
        country=pays, to_plot=options_graphs)
    st.pyplot(graph)

    # Affichage du tableau
    # st.write(df)

    # Sauvegarde de l'image
    img = io.BytesIO()
    plt.savefig(img, format='png')

    # Bouton de téléchargement
    btn = st.download_button(
        label="Télécharger la courbe",
        data=img,
        file_name='plot-covid.png',
        mime="image/png"
    )
