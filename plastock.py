"""
Plastock module

This module provides the methods and utilities for the plastock project. It assumes that plastockconf.py is in the
same directory as this file.

"""
import pandas as pd
from plastockconf import table_css_styles
import matplotlib.pyplot as plt
import seaborn as sns
from myst_nb import glue


def capitalize_x_tick_labels(an_ax):
    an_ax.set_xticks(an_ax.get_xticks().tolist())
    an_ax.set_xticklabels([x.get_text().capitalize() for x in an_ax.get_xticklabels()])


def capitalize_x_and_y_axis_labels(an_ax):
    a_label = an_ax.get_xlabel()
    an_ax.set_xlabel(a_label.capitalize())
    
    a_label = an_ax.get_ylabel()
    an_ax.set_ylabel(a_label.capitalize())
    
def capitalize_legend_components(ax):
    h, l = ax.get_legend_handles_labels()
    new_l = [x.capitalize() for x in l]
    ax.legend(h, new_l)



def attribute_summary(some_data, vals, voi, columns: dict = None, labels: dict = None,
                      a_property: dict = {'color': 'red'}, limits: dict = {'moyenne': 180, '50%': 121},
                      as_type: str = 'int') -> pd.DataFrame:
    """
    Résumé des attributs
    
    dépendances: pandas, plastockconf

    Cette fonction génère un résumé des attributs demandés à partir des données fournies. Elle effectue une agrégation
    par groupe en utilisant les colonnes spécifiées, et génère des statistiques descriptives telles que la
    moyenne, le maximum et le minimum pour chaque groupe.

    Args:
        some_data (pd.DataFrame): Le DataFrame contenant les données à résumer.
        vals (str): Le nom de la colonne contenant les valeurs à agréger.
        voi (str): Le nom de la colonne contenant les valeurs d'intérêt (groupe).
        columns (dict, optional): Un dictionnaire pour renommer les colonnes de résultats (par défaut, None).
        labels (dict, optional): Un dictionnaire de correspondance pour les étiquettes de groupes (par défaut, None).
        a_property (dict, optional): Un dictionnaire de propriétés CSS pour le style (par défaut, {'color': 'red'}).
        limits (dict, optional): Un dictionnaire de limites pour le formatage (par défaut, {'moyenne': 180, '50%': 121}).

    Returns:
        pd.DataFrame: Un DataFrame résumant les attributs avec une mise en forme spécifique.
    """
    # make summary of the requested attribute
    groupby = ['échantillon', voi]
    data = some_data.groupby(groupby, as_index=False)[vals].sum()
    data[voi] = data[voi].apply(lambda x: labels[x])
    
    # get the quantiles for each attribute in the group
    data_summary = data.groupby(voi, as_index=False)[vals].describe()
    
    # rename the columns and set the index
    data_summary[['max', 'min']] = data_summary[['max', 'min']].astype(as_type)
    data_summary[['count']] = data_summary[['count']].astype('int')
    data_summary.rename(columns=columns, inplace=True)
    data_summary.set_index(voi, inplace=True, drop=True)
    data_summary.index.name = None
    
    # apply limits for formatting purposes
    # the styler will use the mask generated from the
    # limts dictionary to apply the style to the cells
    select_values = data_summary["moyenne"] > limits["moyenne"]
    test_one = data_summary.loc[select_values].index
    
    select_values = data_summary["50%"] > limits["50%"]
    test_two = data_summary.loc[select_values].index
    
    # apply css styles to the styler object
    # apply mask to the styler object
    d_sum = data_summary.style.set_table_styles(table_css_styles).format(precision=2)
    d_sum = d_sum.set_properties(subset=pd.IndexSlice[test_one, ["moyenne"]], **a_property)
    
    return d_sum.set_properties(subset=pd.IndexSlice[test_two, ["50%"]], **a_property)


def attribute_summary_test(some_data: pd.DataFrame, vals: str, voi: str, as_type: str = 'int'):
    """
    Résume les attributs d'un DataFrame basé sur des groupes spécifiques.
    
    dépendances: pandas

    Cette fonction regroupe les données de 'some_data' par 'echantillon' et une variable d'intérêt 'voi',
    calcule la somme des valeurs de la colonne spécifiée par 'vals' pour chaque groupe, puis fournit
    des statistiques descriptives pour chaque groupe.

    Args:
        some_data (pd.DataFrame): Le DataFrame contenant les données à analyser.
        vals (str): Le nom de la colonne dont les valeurs sont résumées.
        voi (str): Le nom de la variable d'intérêt utilisée pour le groupement.

    Returns:
        pd.DataFrame: Un DataFrame contenant les statistiques descriptives pour chaque valeur de 'voi',
        incluant le nombre d'observations, la valeur maximale, la valeur minimale, la moyenne, l'écart-type, etc.

    Le DataFrame résultant est indexé par 'voi' avec le nom de l'index supprimé pour une présentation plus claire.
    """
    
    groupby = ['échantillon', voi]
    data = some_data.groupby(groupby, as_index=False)[vals].sum()
    
    data_summary = data.groupby(voi, as_index=False)[vals].describe()
    data_summary[['max', 'min']] = data_summary[['max', 'min']].astype(as_type)
    data_summary[['count']] = data_summary[['count']].astype('int')
    data_summary.set_index(voi, inplace=True, drop=True)
    data_summary.index.name = None
    
    return data_summary


def attribute_summary_grid(data, vals, voi, figname, labels: dict = None, stat="probability", ylim: int = 1000,
                           xlim: int = 1000, figsize: tuple = (8, 7), object_column: str = "Particules"):
    """
    Résumé des attributs sous forme de grille de graphiques

    Cette fonction génère une grille de graphiques pour résumer les attributs à partir des données fournies. Elle effectue
    une agrégation par groupe en utilisant les colonnes spécifiées, puis crée des graphiques pour visualiser les données.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données à résumer.
        vals (str): Le nom de la colonne contenant les valeurs à agréger.
        voi (str): Le nom de la colonne contenant les valeurs d'intérêt (groupe).
        figname (str): Le nom du graphique à générer et afficher.
        labels (dict, optional): Un dictionnaire de correspondance pour les étiquettes de groupes (par défaut, None).
        stat (str, optional): Le type de statistique à afficher dans l'histogramme ('probability' par défaut).

    Returns:
        Un objet de figure matplotlib, attaché à un objet myst_nb.glue. La figure comporte quatre objets d'axe : un
        nuage de points (scatterplot), un histogramme, un boxplot et un ecdfplot.
    """
    groupby = ['échantillon', voi]
    some_data = data.groupby(groupby, as_index=False)[vals].sum()
    some_data[voi] = some_data[voi].apply(lambda x: labels[x])
    
    fig, axs = plt.subplots(2, 2, figsize=figsize)
    
    sns.scatterplot(some_data, x="échantillon", y=vals, hue=voi, ax=axs[0, 0])
    sns.boxplot(some_data, x=voi, y=vals, hue=voi, showfliers=True, ax=axs[0, 1], dodge=False)
    sns.histplot(some_data, x=vals, hue=voi, ax=axs[1, 0], stat=stat, kde=True)
    sns.ecdfplot(some_data, x=vals, hue=voi, ax=axs[1, 1])
    axs[0, 0].set_ylim(-.01, ylim)
    axs[0, 1].set_ylim(-.01, ylim)
    axs[1, 1].set_xlim(-.01, xlim)
    axs[1, 0].set_xlim(-.01, xlim)
    axs[0, 0].tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
    axs[0, 0].set_xlabel("Échantillon")
    axs[0, 0].set_ylabel(object_column)
    capitalize_legend_components(axs[0, 0])
    axs[0, 1].get_legend().remove()
    axs[1, 0].set_xlabel(object_column)
    axs[1, 0].set_ylabel("Probabilité")
    axs[0, 1].set_xlabel("")
    axs[0, 1].set_ylabel(object_column)
    axs[0, 1].tick_params(axis="x", rotation=45)
    axs[1, 0].get_legend().remove()
    axs[1, 1].set_xlabel(object_column)
    plt.subplots_adjust(wspace=.3)
    sns.move_legend(axs[1, 1], title=" ", loc='best')
    
    plt.tight_layout()
    
    glue(figname, fig, display=False)
    plt.close()


def add_table_to_page(table, table_no, caption, section, page, rule, format_index='both',
                      format_kwargs: dict = dict(precision=2, thousands="'", decimal=",")) -> pd.DataFrame:
    """
    Ajoute un tableau à une page dans un document.

    Cette fonction prend un tableau et ajoute son contenu à une page spécifique dans un document.
    Elle permet également de formater les en-têtes du tableau en majuscules si nécessaire.

    Args:
        table (pd.DataFrame): Le tableau à ajouter à la page.
        table_no (int): Le numéro du tableau.
        caption (str): La légende du tableau.
        section (str): La section du document.
        page (int): Le numéro de la page.
        rule (str): La règle du tableau.
        format_index (str, optional): Le format à appliquer aux en-têtes du tableau (par défaut 'both').
            - 'both' : Appliquer le format aux en-têtes des lignes et des colonnes.
            - 'columns' : Appliquer le format aux en-têtes des colonnes uniquement.
            - 'index' : Appliquer le format aux en-têtes des lignes uniquement.

    Returns:
        pd.DataFrame: Le tableau formaté avec la légende spécifiée et prêt à être ajouté au document.
    """
    caption = f'<b>Table {section}{page}-{table_no}: </b>{caption} {rule}'
    if format_index == 'both':
        table = table.format_index(str.capitalize, axis=1).format_index(str.capitalize, axis=0).format(**format_kwargs)
    if format_index == 'columns':
        table = table.format_index(str.capitalize, axis=1).format(**format_kwargs)
    if format_index == 'index':
        table = table.format_index(str.capitalize, axis=0).format(**format_kwargs)
    
    return table.set_caption(caption)