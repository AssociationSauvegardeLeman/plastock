"""
Plastock module

This module provides the methods and utilities for the plastock project. It assumes that plastockconf.py is in the
same directory as this file.

"""
import pandas as pd
import numpy as np
from plastockconf import table_css_styles
import matplotlib.pyplot as plt
import seaborn as sns
from myst_nb import glue

from plastockconf import table_css_styles_top, format_kwargs


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.utils import resample
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

from scipy.stats import beta
from scipy.stats import multinomial

def capitalize_x_tick_labels(an_ax):
    an_ax.set_xticks(an_ax.get_xticks())
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
    d_sum = data_summary.style.set_table_styles(table_css_styles_top).format(precision=2)
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
                           xlim: int = 1000, figsize: tuple = (8, 7), object_column: str = "Particules", hue_order: list = None):
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
        ylim (int, optional): La limite pour l'axe des ordonnées (par défaut, 1000).
        xlim (int, optional): La limite pour l'axe des abscisses (par défaut, 1000).
        figsize (tuple, optional): La taille de la figure à générer (par défaut, (8, 7)).
        object_column (str, optional): Le nom de la colonne contenant les objets (par défaut, "Particules").
        hue_order (list, optional): L'ordre des étiquettes de groupe pour le graphique (par défaut, None).

    Returns:
        Un objet de figure matplotlib, attaché à un objet myst_nb.glue. La figure comporte quatre objets d'axe : un
        nuage de points (scatterplot), un histogramme, un boxplot et un ecdfplot.
    """
    groupby = ['échantillon', voi]
    some_data = data.groupby(groupby, as_index=False)[vals].sum()
    some_data[voi] = some_data[voi].apply(lambda x: labels[x])
    
    fig, axs = plt.subplots(2, 2, figsize=figsize)
    
    if hue_order:
        sns.scatterplot(data=some_data, x="échantillon", y=vals, hue=voi, ax=axs[0, 0], hue_order=hue_order)
        sns.boxplot(data=some_data, x=voi, y=vals, hue=voi, showfliers=True, ax=axs[0, 1], dodge=False,
                    order=hue_order)
        sns.histplot(data=some_data, x=vals, hue=voi, ax=axs[1, 0], stat=stat, kde=True, hue_order=hue_order)
        sns.ecdfplot(data=some_data, x=vals, hue=voi, ax=axs[1, 1], hue_order=hue_order)
    else:
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
    # axs[0, 1].get_legend().remove()
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
                      format_kwargs: dict = format_kwargs, label: bool = False) -> pd.DataFrame:
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
    
    if not label:
        caption = f'<b>Tableau {section}{page}-{table_no} :</b> {caption} {rule}'
    if label:
        caption = " "
        
    if format_index == 'both':
        table = table.format_index(str.capitalize, axis=1).format_index(str.capitalize, axis=0).format(**format_kwargs)
    if format_index == 'columns':
        table = table.format_index(str.capitalize, axis=1).format(**format_kwargs)
    if format_index == 'index':
        table = table.format_index(str.capitalize, axis=0).format(**format_kwargs)
    
    return table.set_caption(caption)

def reindex_df(category, df, index):
    df = df.reindex(index=index)
    return df
def calculate_combined_stats(category, data: pd.DataFrame = None, index=None, val_column='pcs_m'):
    # Descriptive statistics of the sample density and quantity of pieces found
    # Aggregates the data on category and sample_id
    grouped = data.groupby([category, 'échantillon'], as_index=False)[val_column].sum()
    
    group_summary = grouped.groupby(category, as_index=True).agg(
        {'échantillon': 'nunique', val_column: ['mean', 'median']})
    group_summary.columns = group_summary.columns.droplevel(0)
    
    # Calculating percentage of total samples
    group_summary['percentage'] = (group_summary['nunique'] / data['échantillon'].nunique()) * 100
    group_summary.reset_index(drop=False, inplace=True)
    
    # Renaming columns for clarity
    group_summary.rename(columns={'nunique': 'échantillons', 'mean': 'Moyenne', 'median': 'Médiane', 'percentage': '%'},
                         inplace=True)
    group_summary.set_index(category, inplace=True, drop=True)
    
    # Make the index labels if required
    if index is not None:
        group_summary = reindex_df(category, group_summary, index=index)
    
    return group_summary.style.set_table_styles(table_css_styles).format(precision=2).hide(axis=0, names=True)


def analyze_scenario(scenario_data, func, n_iterations=100):
    """
    Analyze a specific scenario using Random Forest regression with bootstrapping,
    and calculate feature importances.

    :param data: DataFrame containing the dataset.
    :param feature_1: The name of the first feature for filtering.
    :param feature_1_value: The value of the first feature to filter by.
    :param feature_2: The name of the second feature for filtering.
    :param feature_2_value: The value of the second feature to filter by.
    :param n_iterations: Number of bootstrap iterations. Default is 100.
    :param bin_width: Width of each bin for histogram. Default is 0.2.
    :return: A tuple containing bins, bin probabilities, flattened predictions, and feature importances.
    """
    
    # Prepare data for regression
    y_scaler = MinMaxScaler()
    y_scaled = y_scaler.fit_transform(scenario_data['pcs_m'].values.reshape(-1, 1)).flatten()
    
    # Initialize the OneHotEncoder
    # here we encode the ordinal data
    encoder = OneHotEncoder(sparse_output=False)
    
    X = scenario_data.drop('pcs_m', axis=1)
    
    # Apply the encoder to the categorical columns
    encoded_data = encoder.fit_transform(scenario_data[['fréquentation', 'situation', 'distance', 'substrat']])
    # Create a DataFrame with the encoded data
    X_encoded = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(
        ['fréquentation', 'situation', 'distance', 'substrat']))
    
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_scaled, test_size=0.2, random_state=42)
    
    # Bootstrap predictions and accumulate feature importances
    bootstrap_predictions = []
    feature_importances_accumulated = np.zeros(X_train.shape[1])
    
    # Collect diagnostic at each repetition
    cum_mse = []
    cum_r2 = []
    
    for _ in range(n_iterations):
        X_train_sample, y_train_sample = resample(X_train, y_train)
        rf_model_sample = func
        rf_model_sample.fit(X_train_sample, y_train_sample)
        
        pred = rf_model_sample.predict(X_test)
        
        r2 = r2_score(y_test, pred)
        pred = y_scaler.inverse_transform(pred.reshape(-1, 1)).flatten()
        bootstrap_predictions.append(pred)
        mse = mean_squared_error(y_test, pred)
        
        feature_importances_accumulated += rf_model_sample.feature_importances_
        
        cum_mse.append(mse)
        cum_r2.append(r2)
        
        # Average feature importances
    feature_importances = feature_importances_accumulated / n_iterations
    
    # Flatten the predictions array
    predictions_flat = np.array(bootstrap_predictions).flatten()
    
    return predictions_flat, feature_importances, cum_mse, cum_r2


def plot_histogram(predictions, observed, title="", reference='camp-dist-1', display=False, xlabel='pcs/m',
                   ylabel='Densité de Probabilité', bins=20):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(predictions, bins=bins, stat="probability", ax=ax, label='prédictions', zorder=1)
    sns.histplot(observed, bins=bins, stat="probability", label='observée', zorder=0, ax=ax)
    plt.title(title, loc='left')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    glue(reference, fig, display=display)
    plt.close()


def evalutate_model(r2s, mses, label, model='random-forest'):
    r2 = np.round(np.mean(r2s), 2)
    mse = np.round(np.mean(mses), 2)
    results = {"cross validated error": r2, "mean² error": mse, 'model': model}
    return pd.DataFrame(results, index=[label])


# Calculating quantiles for Scenario 2
q_uants = [0.01, 0.25, 0.5, 0.75, 0.99]
index = ['1%', '25%', '50%', '75%', '99%', 'Moyenne']


def makeqdf(observed, predicted, index=index, quants=q_uants, caption=""):
    o_q = np.quantile(observed, quants)
    m_o = np.mean(observed)
    o_p = np.quantile(predicted, quants)
    m_p = np.mean(predicted)
    
    results = {'observée': [*o_q, m_o], 'prédiction': [*o_p, m_p]}
    return pd.DataFrame(results, index=index).style.set_table_styles(table_css_styles_top).format(
        precision=2).set_caption(caption)


def sum_a_b(zipped):
    for element in zipped:
        # the new beta distribution would be
        # total success, (total tries - total success)
        new_element_0 = np.array([np.array([x[0], x[1] - x[0]]) for x in element[0]])
        new_element_1 = np.array([x for x in element[1]])
        t3 = new_element_0 + new_element_1
        
        yield t3


# Grid approximation
# grid_val_index = np.linspace(0, 5.99, 600)
groupby_columns = ['sample_id', 'location', 'date', 'city', 'orchards', 'vineyards', 'buildings', 'forest',
                   'undefined', 'public_services', 'streets']


def draw_a_beta_value(generator):
    d = next(generator)
    # drawing a random number from the beta distribution
    # this is the the chance p, that a binomial distribution will
    # result in True.
    my_beta = [beta(x[0], x[1]).rvs(1) for x in d]
    yield my_beta


def binomial_probability_of_failure(generator):
    # in this case failure means exceeding the value
    # for trash a success is never exceeding the value
    d = next(generator)
    di = [x[0] for x in d]
    yield di


def bin_land_use_values(*, data: pd.DataFrame, column: str, num_bins: int = 4) -> pd.DataFrame:
    """
    Bins the specified column's values into a given number of bins and adds a new column to the DataFrame with these bin labels.

    Args:
        data (pd.DataFrame): The DataFrame to modify.
        column (str): The name of the column to bin.
        num_bins (int, optional): The number of bins to use. Defaults to 20.

    Returns:
        pd.DataFrame: The modified DataFrame with an additional column for binned values.
    """
    data[f'{column}_bin'] = pd.cut(data[column], bins=num_bins, labels=[1, 2, 3, 4], include_lowest=True)
    return data


def calculate_likelihood(*, aggregated_data: pd.DataFrame, bin_density_column: str, pcs_column: str = 'pcs/m',
                         grid_range: np.ndarray = None, bins: list = None) -> pd.DataFrame:
    """
    Calculates the likelihood of observing the aggregated pcs/m data for each grid point and bin density value.

    Args:
        aggregated_data (pd.DataFrame): The aggregated data to be used for likelihood calculation.
        bin_density_column (str): The column representing bin density numbers.
        pcs_column (str, optional): The pcs/m column to use for calculation. Defaults to 'pcs/m'.
        grid_range (np.ndarray, optional): The range of grid values. Defaults to np.linspace(0, 9.99, 1000).

    Returns:
        pd.DataFrame: A DataFrame with likelihood values for each grid value and bin density number.
    """
    likelihood_df = pd.DataFrame(index=grid_range)
    
    for bin_value in bins:
        bin_data = aggregated_data[aggregated_data[bin_density_column] == bin_value]
        if bin_data.empty:
            likelihoods = [np.array([1, 1]) for grid_point in grid_range]
        else:
            likelihoods = [np.array([(bin_data[pcs_column] > grid_point).sum(), len(bin_data)]) for grid_point in
                           grid_range]
        likelihood_df[f'Likelihood_{bin_value}'] = likelihoods
    return likelihood_df


def calculate_beta_prior(*, grid_range: np.ndarray = [],
                         bin_density_numbers: list = list(range(1, 21))) -> pd.DataFrame:
    """
    Calculates a Beta(1, 1) prior for each value in the specified grid range for each bin density number.

    Args:
        grid_range (np.ndarray, optional): The range of grid values. Defaults to np.linspace(0, 9.99, 1000).
        bin_density_numbers (List[int], optional): List of bin density numbers. Defaults to range(1, 21).

    Returns:
        pd.DataFrame: A DataFrame with Beta(1, 1) prior values for each grid value and bin density number.
    """
    prior_df = pd.DataFrame(index=grid_range)
    prior_values = np.array([1, 1])  # since Beta(1, 1) is = odds at all points
    
    for bin_number in bin_density_numbers:
        prior_df[f'Bin_{bin_number}'] = [prior_values for _ in grid_range]
    return prior_df


def define_posterior(likelihood, prior, grid_val_index: np.array = None):
    # the alpha, beta parameters of the likelihood and prior are assembled
    alpha_beta = list(zip(likelihood.values, prior.values))
    # this is a generator that yields the sum of the alpha, beta parameters
    # of the likelihood and prior. It generates one value for each point on the grid.
    a_b_sum = sum_a_b(alpha_beta)
    
    posteriors = []
    for i in grid_val_index:
        # the sum of successes and failures for the scenario at the given
        # grid value are used as the alpha, beta parameters of the beta distribtion
        # for the binomial/bernouli probability that a sample will exceed the grid
        # value i.
        st = binomial_probability_of_failure(draw_a_beta_value(a_b_sum))
        val = next(st)
        posteriors.append(val)
    
    # return posterior probabilities with gird index and column labels
    post_grid_pstock = pd.DataFrame(posteriors, index=grid_val_index, columns=prior.columns)
    
    # identify the x scale of the grid
    post_grid_pstock['X'] = post_grid_pstock.index
    
    # this column is the normalized probabilities that a sample
    # will exceed a value on the grid.
    post_grid_pstock['norm'] = post_grid_pstock['Bin_1'] / post_grid_pstock['Bin_1'].sum()
    
    return post_grid_pstock


def non_zero(alist):
    # find the first non-zero object in an array
    # return the index number and the value.
    for i, anum in enumerate(alist):
        if anum != 0:
            return i, anum
    return None


def draw_sample_from_multinomial(normed, n=100):
    # the norm column from the posterior data frame is
    # used as the probabilities of a multinomial distribution
    rv = multinomial(1, normed.values)
    y = rv.rvs(n)
    
    indexes = []
    for i in range(0, len(y)):
        indexes.append(non_zero(y[i])[0])
    return indexes


def posterior_predictions(p_g_p):
    p_norm = p_g_p['norm']
    
    indexes = draw_sample_from_multinomial(p_norm)
    results_scale = p_g_p.reset_index(drop=True)
    sample_totals = results_scale.loc[indexes, "X"]
    
    return sample_totals