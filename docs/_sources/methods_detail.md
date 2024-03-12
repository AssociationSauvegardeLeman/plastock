# Methods

## Random Forest

source: [random forest regressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html#sklearn.ensemble.RandomForestRegressor)

A random forest is a meta estimator that fits a number of classifying decision trees on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting. The sub-sample size is controlled with the max_samples parameter if bootstrap=True (default), otherwise the whole dataset is used to build each tree.

Bootstrap Aggregation is a general procedure that can be used to reduce the variance for those algorithm that have high variance. An algorithm that has high variance are decision trees, like classification and regression trees (CART). Decision trees are sensitive to the specific data on which they are trained. If the training data is changed (e.g. a tree is trained on a subset of the training data) the resulting decision tree can be quite different and in turn the predictions can be quite different. That is, a small change in the training data set can result in a very different tree. The reason for this lies in the hierarchical nature of the tree classifiers. An error that occurs in a node at a high level of the tree propagates all the way down to the leaves below it.

Bagging is the application of the Bootstrap procedure to a high-variance machine learning algorithm, typically decision trees. Bagging (bootstrap aggregating) can reduce the variance and improve the generalization error performance. The basic idea is to create B variants, X1, X2,...,XB , of the training set X, using bootstrap techniques, by uniformly sampling from X with replacement. For each of the training set variants Xi , a tree Ti is constructed. The final decision for the classification of a given point is in favor of the class predicted by the majority of the subclassifiers Ti,wheri=1,2,...,B.

### Prediction



### Feature importance: permutation

source: [permuation feature importance](https://scikit-learn.org/stable/modules/permutation_importance.html#permutation-importance)

Permutation feature importance is a model inspection technique that can be used for any fitted estimator when the data is tabular. This is especially useful for non-linear or opaque estimators. The permutation feature importance is defined to be the decrease in a model score when a single feature value is randomly shuffled. This procedure breaks the relationship between the feature and the target, thus the drop in the model score is indicative of how much the model depends on the feature. This technique benefits from being model agnostic and can be calculated many times with different permutations of the feature.



```python
# hist_leman = pd.read_csv("data/end_pipe/hist_leman.csv")
# hist_leman.rename(columns={"sample_id":"loc_date", "location":"slug", "pcs/m":"pcs_m"}, inplace=True)

# hist_leman.loc[hist_leman.slug == 'preverenges', 'region'] = 'Grand lac'
# hist_leman.loc[hist_leman.slug == 'tolochenaz', 'region'] = 'Grand lac'
# hist_leman.loc[hist_leman.slug == 'versoix', 'region'] = 'Grand lac'
# hist_leman.loc[hist_leman.slug == 'vidy', 'region'] = 'Grand lac'
# # hist_leman = hist_leman[hist_leman.code.isin(ti_work.code.unique())].copy()
# lh_df = pd.concat([hist_leman[hist_leman.code.isin(ti_work.code.unique())].copy(), ti_work])

# slh = lh_df[lh_df.city == 'Saint-Sulpice (VD)'].loc_date.unique()
# ssp=pd.read_csv('data/end_pipe/swt_all.csv')
# keep = [x for x in ssp.loc_date.unique() if x not in slh]
# ssp_2022 = ssp[ssp.loc_date.isin(keep)].copy()
# ssp_2022.rename(columns={'pcs/m':'pcs_m'}, inplace=True)
# ssp_2022['date'] = pd.to_datetime(ssp_2022['date'])
# ssp_dt = ssp_2022.groupby(['loc_date', 'date'], as_index=False).pcs_m.sum()

# these_codes = ['Gfrags', 'G27', 'G30', 'Gfoams', 'Gcaps', 'G95', 'G112', 'G74', 'G89', 'G31']
# order = ['MCBP', 'SLR', 'IQAASL', 'Solid-Waste-Team', 'Plastock']
# summary_index = ['min', '25%', '50%', '75%', 'max', 'mean', 'std', 'count', 'total']

# lh_df_dt = lh_df[lh_df.code.isin(these_codes)].groupby(['loc_date','date', 'region', 'project'], as_index=False).agg({'pcs_m':'sum'})
# dt = lh_df.groupby(['loc_date', 'slug', 'project'], as_index=False)['pcs_m'].sum()
# dt = dt.groupby(['slug', 'project'], as_index=False)['pcs_m'].mean()
# dtcigs = lh_df[(lh_df.code == "G27")].groupby(['loc_date', 'slug', 'project'], as_index=False)['pcs_m'].sum()
# dtcigs = dtcigs.groupby(['slug', 'project'], as_index=False)['pcs_m'].mean()
# dtfrags = lh_df[(lh_df.code == 'Gfrags')].groupby(['loc_date', 'slug', 'project'], as_index=False)['pcs_m'].sum()
# dtfrags = dtfrags.groupby(['slug', 'project'], as_index=False)['pcs_m'].mean()
# dtcigs["G27"] = dtcigs["pcs_m"]
# dtfrags["Gfrags"] = dtfrags["pcs_m"]

# dt['Total'] = dt['pcs_m']

# region_map = lh_df[["slug", "region"]].drop_duplicates(["slug", "region"])
# region_map.set_index("slug", drop=True, inplace=True)

# # gps_map = beach_data[["Plage", "latitude", "longitude"]].drop_duplicates("Plage")
# # gps_map.set_index("Plage", drop=True, inplace=True)

# gps = dt[["slug","project", "Total"]].merge(dtcigs[["slug","project", "G27"]],left_on=["slug","project"], right_on=["slug","project"])

# gps = gps.merge(dtfrags[["slug","project", "Gfrags"]], left_on=["slug","project"], right_on=["slug","project"])
# gps["region"] = gps.slug.apply(lambda x: region_map.loc[x])

# gps["lat"] = gps.Plage.apply(lambda x: gps_map.loc[x, "latitude"])
# gps["lon"] = gps.Plage.apply(lambda x: gps_map.loc[x, "longitude"])

# lats = pd.read_csv("data/ignorethese/u_iq_ps_beaches.csv")

# lats.loc[lats.slug == "savoniere", "slug"] = "savonniere"
# lats.loc[lats.slug == "savonniere", "location"] = "Savonnière"
# lats.loc[lats.slug == "savonniere", "city"] = "Savonnière"
# lats.loc[lats.slug == "versoix-p", "location"] = "Versoix"
# gps_map = lats[["slug", "latitude", "longitude"]].drop_duplicates("slug").set_index("slug")
# gps["lat"] = gps.slug.apply(lambda x: gps_map.loc[x, "latitude"])
# gps["lon"] = gps.slug.apply(lambda x: gps_map.loc[x, "longitude"])
# gps_pstock = gps[gps.project == "Plastock"].copy()
# gps_prev = gps[gps.project != "Plastock"].copy()


# label_map = lats[["slug", "location"]].drop_duplicates("slug")
# label_map.set_index("slug", drop=True, inplace=True)
# gps_pstock["label"] = gps_pstock.slug.apply(lambda x: label_map.loc[x])

# gps_prev.to_csv("resources/maps/previous_results.csv", index=False)
# gps_pstock.to_csv("resources/maps/plastock_lm.csv", index=False)





def sum_a_b(zipped):
    for element in zipped:
        # the new beta distribution would be
        # total success, (total tries - total success)
        new_element_0 = np.array([np.array([x[0], x[1] - x[0]]) for x in element[0]])
        new_element_1 = np.array([x for x in element[1]])
        t3 = new_element_0 + new_element_1
        
        yield t3

# Grid approximation
grid_val_index = np.linspace(0, 5.99, 600)
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
    data[f'{column}_bin'] = pd.cut(data[column], bins=num_bins, labels=[1, 2, 3, 4 ], include_lowest=True)
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

def calculate_beta_prior(*, grid_range: np.ndarray = grid_val_index, bin_density_numbers: List[int] = list(range(1,
                                                                                                    21))) -> pd.DataFrame:
    """
    Calculates a Beta(1, 1) prior for each value in the specified grid range for each bin density number.

    Args:
        grid_range (np.ndarray, optional): The range of grid values. Defaults to np.linspace(0, 9.99, 1000).
        bin_density_numbers (List[int], optional): List of bin density numbers. Defaults to range(1, 21).

    Returns:
        pd.DataFrame: A DataFrame with Beta(1, 1) prior values for each grid value and bin density number.
    """
    prior_df = pd.DataFrame(index=grid_range)
    prior_values = np.array([1, 1])  # Constant value since Beta(1, 1) is uniform
    
    for bin_number in bin_density_numbers:
        prior_df[f'Bin_{bin_number}'] = [prior_values for grid_point in grid_range]
    return prior_df



def define_posterior(likelihood, prior, grid_val_index: np.array = None):
    
    # the alpha, beta parameters of the likelihood and prior are assembled
    alpha_beta = list(zip(likelihood.values, prior.values))
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
    post_grid_pstock['norm'] = post_grid_pstock['Bin_1']/post_grid_pstock['Bin_1'].sum()
    
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

```
