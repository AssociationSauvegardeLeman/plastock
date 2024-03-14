# imported methods from iqaasl
import pandas as pd
import setvariables as conf_
from typing import List, Dict, Union, Tuple, Callable
from matplotlib.colors import ListedColormap
from plastockconf import table_css_styles_top



# def convert_pixel_to_cm(file_name: str = None) -> ():
#     im = PILImage.open(file_name)
#     width, height = im.size
#     dpi = im.info.get("dpi", (72, 72))
#     width_cm = width / dpi[0] * 2.54
#     height_cm = height / dpi[1] * 2.54
#
#     return width_cm, height_cm

def use_gfrags_gfoams_gcaps(data, codes,columns=["Gfoams", "Gfrags", "Gcaps"]):
    for col in columns:
        change = codes.loc[codes.parent_code == col].index
        data.loc[data.code.isin(change), "code"] = col
        
    return data


def combine_survey_files(list_of_files):

    files = []
    for afile in list_of_files:
        files.append(pd.read_csv(afile))
    return pd.concat(files)


def slice_data_by_date(data: pd.DataFrame, start: str, end: str):
    mask = (data.date >= start) & (data.date <= end)
    return data[mask]


def capitalize_index(x):
    return x.title()


def aggregate_dataframe(df: pd.DataFrame,
                        groupby_columns: List[str],
                        aggregation_functions: Dict[str, Union[str, callable]],
                        index: bool = False) -> pd.DataFrame:
    """
    Aggregate specified columns in a Pandas DataFrame using given aggregation functions.

    Args:
        df (pd.DataFrame): The input DataFrame.
        groupby_columns (List[str]): List of column names to group by.
        aggregation_functions (Dict[str, Union[str, callable]]):
            A dictionary where keys are column names to aggregate,
            and values are either aggregation functions (e.g., 'sum', 'mean', 'max', 'min')
            or custom aggregation functions (callable functions).
        index (bool, optional): Whether to use the groupby columns as an index.
            Default is False.

    Returns:
        pd.DataFrame: A new DataFrame with aggregated values.
    """
    grouped = df.groupby(groupby_columns, as_index=index).agg(aggregation_functions)
    
    return grouped


def merge_dataframes_on_column_and_index(left_df: pd.DataFrame,
                                         right_df: pd.DataFrame,
                                         left_column: str,
                                         how: str = 'inner',
                                         validate: str = 'many_to_one') -> pd.DataFrame:
    """
    Merge two DataFrames where the left DataFrame is merged on a specified column and
    the right DataFrame is merged on its index.

    Args:
        left_df (pd.DataFrame): The left DataFrame to be merged.
        right_df (pd.DataFrame): The right DataFrame to be merged on its index.
        left_column (str): The column in the left DataFrame to merge on.
        how (str, optional): The type of merge to be performed ('left', 'right', 'outer', or 'inner').
            Default is 'inner'.
        validate (str, optional): Whether to perform merge validation checks.
            Default is 'many_to_one'.

    Returns:
        pd.DataFrame: A new DataFrame resulting from the merge operation.
    """

    merged_df = left_df.merge(right_df, left_on=left_column, right_index=True, how=how, validate=validate)
    return merged_df


def get_top_x_records_with_max_quantity(df: pd.DataFrame, quantity_column: str, id_column: str, x: int):
    """
    Get the top x records with the greatest quantity and their proportion to the total from a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        quantity_column (str): The name of the quantity column.
        id_column (str): The name of the ID column.
        x (int): The number of records to return.

    Returns:
        A data frame
    """
    # Sort the DataFrame by the quantity column in descending order, take the top x records, and select the ID column
    top_x_records = df.nlargest(x, quantity_column)[[id_column, quantity_column]]
    top_x_records["%"] = top_x_records[quantity_column] / top_x_records[quantity_column].sum()
    
    return top_x_records[[id_column, quantity_column, "%"]]




def count_objects_with_positive_quantity(df: pd.DataFrame, value_column: str = 'quantity',
                                         object_column: str = 'code') -> Dict[str, int]:
    """
    Count how many times each object had a quantity greater than zero in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'sample,' 'object,' and 'quantity.'
        value_column (str): The column label of the values being counted.
        object_column (str): The column label of the objects being counted.

    Returns:
        pd.Series: A Series with the count of positive quantity occurrences for each object.
    """
    # Filter the DataFrame to include rows where quantity is greater than zero
    positive_quantity_df = df[df[value_column] > 0]
    no_count_df = df[(df[value_column] == 0)]
    
    # Count the occurrences of positive quantities for each object
    object_counts = positive_quantity_df[object_column].value_counts()
    failed = object_counts / df.loc_date.nunique()
    
    # identify the objects with a zero count
    no_counts = no_count_df[object_column].value_counts()
    zeroes = no_counts[~no_counts.index.isin(object_counts.index)]
    zeroes.loc[:] = 0
    
    return pd.concat([failed, zeroes])


def calculate_rate_per_unit(df: pd.DataFrame,
                            objects_to_check: List[str],
                            column_of_interest: str = "code",
                            groupby_columns: List[str] = ['code'],
                            method: Dict[str, str] = {"pcs_m": "median", "quantity": "sum"},
                            a_label: str = "all",
                            ) -> pd.DataFrame:
    """
    Calculate the rate of object(s) for a given unit measurement. Adds the label
    'all' to each record.

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'sample,' 'object,' and 'quantity.'
        objects_to_check (List[str]): The list of objects to calculate proportions for.
        column_of_interest (str): The column label of the objects being compared.
        groupby_columns (List[str]): The columns used for the aggregation.
        method (Dict[str]): Dictionary specifying the aggregation functions for the unit_measurement.

    Returns:
        pd.DataFrame: A dataframe where index is column_of_interest and the value column is the rate
            and the label is 'all'.
    """
    # Filter the DataFrame to include rows where 'object' is in 'objects_to_check'
    filtered_df = df[df[column_of_interest].isin(objects_to_check)]
    
    # Calculate the total quantity for each object
    object_rates = filtered_df.groupby(groupby_columns, as_index=False).agg(method)
    
    # Calculate the proportion for each object
    rates = object_rates[[column_of_interest, *method.keys()]].set_index(column_of_interest, drop=True)
    rates["label"] = a_label
    
    return rates


# pieces per meter for a set of data
# # rate_per_unit_cumulative(df, cumulative_columns, object_labels, object_columns, unit_agg)
# def rate_per_unit_cumulative(df: pd.DataFrame, groupby_columns: List, object_labels: List, objects: List,
#                              agg_methods: Dict) -> pd.DataFrame:
#     """
#     Calculate cumulative rates per unit for specific objects and aggregation methods.
#
#     This function takes a DataFrame and calculates cumulative rates per unit based on
#     the specified groupby columns, object labels, objects of interest, and aggregation methods.
#
#     Args:
#         df (pd.DataFrame): The input DataFrame containing data for analysis.
#         groupby_columns (List): List of columns to group by in the DataFrame.
#         object_labels (List): List of labels to identify objects of interest.
#         objects (List): List of objects for which cumulative rates are calculated.
#         agg_methods (Dict): Dictionary specifying aggregation methods for calculating rates.
#
#     Returns:
#         pd.DataFrame: A DataFrame containing the cumulative rates per unit.
#
#     Example:
#         groupby_columns = ['Region', 'Year']
#         object_labels = ['Object A', 'Object B']
#         objects = ['A', 'B']
#         agg_methods = {'Value': 'sum', 'Count': 'count'}
#
#         cumulative_rates = rate_per_unit_cumulative(df, groupby_columns, object_labels, objects, agg_methods)
#     """
#     parent_summary = aggregate_dataframe(df, groupby_columns, agg_methods)
#
#     parent_boundary_summary = calculate_rate_per_unit(parent_summary,
#                                                       groupby_columns=groupby_columns[-1:],
#                                                       objects_to_check=df[groupby_columns[-1]].unique(),
#                                                       column_of_interest=groupby_columns[-1])
#     parent_boundary_summary.reset_index(drop=False, inplace=True)
#
#     return parent_boundary_summary

def color_gradient(val, cmap: ListedColormap = None, cmin: float = 0.0, cmax: float = .9):
    """
    Apply a color gradient to a numerical value for cell styling.

    This function takes a numerical value 'val' and applies a color gradient based on the provided
    colormap ('cmap') and the specified range defined by 'min' and 'max'. It returns a CSS style
    for cell background color.

    Args:
        val (float): The numerical value to be colored using the gradient.
        cmap (ListedColormap, optional): The colormap to use for the color gradient. Defaults to None.
        cmin (float, optional): The minimum value of the data range. Defaults to 0.0.
        cmax (float, optional): The maximum value of the data range. Defaults to 1.0.

    Returns:
        str: A CSS style string for cell background color and text color.

    Example:
        # Apply a color gradient using a custom colormap 'cmap' to the DataFrame
        df.style.applymap(color_gradient, cmap=my_colormap, min=0.0, max=100.0)
    """
    # Normalize the value to a range [0, 1]
    # min, max should be the min max for the
    # data frame in question
    normalized_val = (val - cmin) / cmax
    
    r, g, b, a = cmap(normalized_val)
    
    # Calculate the color based on the normalized value
    hex_color = f"rgba({int(r * 255)},{int(g * 255)},{int(b * 255)}, .5)"
    
    # Return the CSS style with the background color
    return f'background-color: {hex_color}; color:black'




def translate_word(x: str, amap: pd.DataFrame, lan: str):
    """
    Translate a word or phrase using a language mapping DataFrame.

    This function takes a word or phrase 'X' and attempts to translate it into another language
    specified by 'lan' using a language mapping DataFrame 'map'. If the word is found in the index
    of the mapping DataFrame, the translation is returned; otherwise, the original word is returned.

    Args:
        x (str): The word or phrase to be translated.
        amap (pd.DataFrame): A DataFrame containing language mappings.
        lan (str): The language to translate into.

    Returns:
        str: The translated word or phrase, or the original word if not found in the mapping.

    Example:
        # Create a DataFrame for language mapping
        language_map = pd.DataFrame({'English': ['apple', 'banana', 'cherry'],
                                    'French': ['pomme', 'banane', 'cerise']})

        # Translate a word into French
        translated_word = translate_word('apple', language_map, 'French')
    """
    
    if x in amap.index:
        return amap.loc[x, lan]
    else:
        return x

def translate_for_display(df: pd.DataFrame, amap: pd.DataFrame, lan: str):
    """
    Translate column names and index labels of a DataFrame for display.

    This function takes a DataFrame 'df' and translates its column names and index labels using a
    language mapping DataFrame 'map' for display in a specified language 'lan'. The translated
    column names are used as new column names in the DataFrame, and the index labels are replaced
    with their translations.

    Args:
        df (pd.DataFrame): The input DataFrame for translation.
        amap (pd.DataFrame): A DataFrame containing language mappings.
        lan (str): The target language code for translation.

    Returns:
        pd.DataFrame: The DataFrame with translated column names and index labels for display.

    Example:
        # Create a DataFrame to be translated
        data = {'apple': [1, 2, 3], 'banana': [4, 5, 6]}
        original_df = pd.DataFrame(data)

        # Create a language mapping DataFrame
        language_map = pd.DataFrame({'English': ['apple', 'banana'],
                                    'French': ['pomme', 'banane']})

        # Translate the column names and index labels for display in French
        translated_df = translate_for_display(original_df, language_map, 'French')
    """
    
    new_columns = {x: translate_word(x, amap, lan) for x in df.columns}
    df.rename(columns=new_columns, inplace=True)
    
    new_index = [translate_word(x, amap, lan) for x in df.index]
    df.loc[:, 'new_index'] = new_index
    df.set_index('new_index', drop=True, inplace=True)
    
    # either change the labels to something significant for
    # display or remove them from the data frame
    df.index.name = None
    df.columns.name = None
    
    return df

def translated_and_style_for_display(df, amap, lan, capitalize: str = 'index', gradient: bool = True):
    """
    Translate, style, and format a DataFrame for display.

    This function translates column names and index labels, applies styling, and optionally
    adds a color gradient to a DataFrame to prepare it for display in a specified language 'lan'.

    Args:
        df (pd.DataFrame): The input DataFrame to be translated and styled.
        amap (pd.DataFrame): A DataFrame containing language mappings.
        lan (str): The target language code for translation.
        capitalize (str, optional): Whether to capitalize the DataFrame. Defaults to index.
        gradient (bool, optional): Whether to apply a color gradient to the DataFrame. Defaults to True.

    Returns:
        Styler: A styled DataFrame ready for display with translated labels and styling.

    Example:
        # Create a DataFrame to be translated and styled
        data = {'apple': [1, 2, 3], 'banana': [4, 5, 6]}
        original_df = pd.DataFrame(data)

        # Create a language mapping DataFrame
        language_map = pd.DataFrame({'English': ['apple', 'banana'],
                                    'French': ['pomme', 'banane']})

        # Translate, style, and format the DataFrame for display in French
        styled_df = translated_and_style_for_display(original_df, language_map, 'French', gradient=True)
    """
    d = translate_for_display(df, amap, lan)
    d = d.style.format(**conf_.format_kwargs).set_table_styles(table_css_styles_top)
    if gradient:
        d = d.applymap(color_gradient, cmap=conf_.newcmp)
    d.applymap(lambda x: 'color: #E5E5E5' if pd.isnull(x) else '')
    d.applymap(lambda x: 'background: #E5E5E5' if pd.isnull(x) else '')
    
    if capitalize == 'index':
        return d.format_index(str.capitalize, axis=0)
    elif capitalize == 'columns':
        return d.format_index(str.capitalize, axis=1)
    elif capitalize == 'both':
        return d.format_index(str.capitalize, axis=1).format_index(str.capitalize, axis=0)
    else:
        return d


def display_tabular_data_by_column_values(df, column_one: dict, column_two: dict, index: str):
    """
    Display tabular data based on column values.

    This function filters a DataFrame 'df' to include rows where either 'column_one' or 'column_two'
    meet specified conditions. The resulting DataFrame is then set to have 'index' as the index, and
    the index name is removed for cleaner tabular display.

    Args:
        df (pd.DataFrame): The input DataFrame containing tabular data.
        column_one (dict): A dictionary specifying the column and value condition for 'column_one'.
        column_two (dict): A dictionary specifying the column and value condition for 'column_two'.
        index (str): The column to be set as the index for the resulting DataFrame.

    Returns:
        pd.DataFrame: The filtered DataFrame with 'index' as the index and the index name removed.

    """
    d = df.sort_values(by=column_one['column'], ascending=False)
    the_min_val = d.iloc[int(column_one['val'])][column_one["column"]]
    d = df[(df[column_one["column"]] >= the_min_val) | (df[column_two["column"]] >= column_two["val"])].copy()
    d.set_index(index, inplace=True, drop=True)
    d.index.name = None
    return d.sort_values(by=column_one['column'], ascending=False)

def collect_survey_data_for_report(a_func: Callable = None, **kwargs) -> pd.DataFrame:
    """
    Collect and preprocess survey data for generating a report.

    Parameters:
        a_func (Callable, optional): A custom data collection function. If provided,
            this function will be called with the provided keyword arguments (kwargs)
            to collect and preprocess survey data. It should return a pandas DataFrame
            containing the survey data.
        **kwargs: Additional keyword arguments that are passed to the data collection
            function (a_func).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the survey data for generating a report.

    If a custom data collection function (a_func) is provided, it is responsible for collecting
    and preprocessing the survey data. This function should return a pandas DataFrame.

    If a_func is not provided, the method will use the default survey data collection logic,
    combining survey files specified in the configuration (conf_.survey_files) and returning
    the resulting DataFrame.
    """
    
    if a_func is not None:
        return a_func(**kwargs)
    else:
        survey_files = conf_.survey_files
        data = combine_survey_files(survey_files)
    return data


def collect_env_data_for_report(a_func: Callable = None, **kwargs) -> tuple:
    """
    Collect environmental data for generating a report.

    Parameters:
        a_func (Callable, optional): A custom data collection function. If provided,
            this function will be called with the provided keyword arguments (kwargs)
            to collect and preprocess environmental data. It should return a pandas DataFrame
            or a tuple of DataFrames containing the required environmental data.
        **kwargs: Additional keyword arguments that are passed to the data collection
            function (a_func).

    Returns:
        Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
        A pandas DataFrame or a tuple of DataFrames containing the environmental data
        required for generating a report.

    If a custom data collection function (a_func) is provided, it is responsible for collecting
    and preprocessing the environmental data. This function should return a pandas DataFrame
    or a tuple of DataFrames (codes, beaches, land_cover, land_use, streets, river_intersect_lakes).

    If a_func is not provided, the method will use the default data collection logic, which loads
    environmental data from specified CSV files (conf_.code_data, conf_.beach_data, conf_.land_cover_data,
    conf_.land_use_data, conf_.street_data, conf_.intersection_attributes) and returns them as a tuple.
    """
    
    if a_func is not None:
        return a_func(**kwargs)
    else:
        codes = pd.read_csv(conf_.code_data).set_index("code")
        beaches = pd.read_csv(conf_.beach_data).set_index("slug")
        land_cover = pd.read_csv(conf_.land_cover_data)
        land_use = pd.read_csv(conf_.land_use_data)
        streets = pd.read_csv(conf_.street_data)
        river_intersect_lakes = pd.read_csv(conf_.intersection_attributes)
    
    return codes, beaches, land_cover, land_use, streets, river_intersect_lakes


def language_maps(func: Callable = None, **kwargs):
    """
    Collect language mapping data for generating a report.

    Parameters:
        func (Callable, optional): A custom data collection function. If provided,
            this function will be called with the provided keyword arguments (kwargs)
            to collect and preprocess language mapping data. It should return a dictionary
            containing language mapping DataFrames.
        **kwargs: Additional keyword arguments that are passed to the data collection
            function (func).


    Returns:
        Union[None, Dict[str, pd.DataFrame]]:
        A dictionary containing language mapping DataFrames, or None if custom data
        collection is not used.

    If a custom data collection function (func) is provided, it is responsible for collecting
    and preprocessing language mapping data. This function should return a dictionary where
    keys are language codes (e.g., 'fr', 'es') and values are pandas DataFrames with language
    mapping information.

    If func is not provided, the method will use the default data collection logic, which loads
    language mapping data from specified CSV files (configured in conf_.language_maps) and returns
    them as a dictionary.
    """
    if func is not None:
        return func(**kwargs)
    else:
        maps = {k: pd.read_csv(v).set_index('en') for k, v in conf_.language_maps.items()}
        return maps


def check_for_top_label(alabel: str = None, df: pd.DataFrame = None, a_map: pd.DataFrame = None) -> pd.DataFrame:
    """
    Check for the presence of a top-level label in a DataFrame and update it if necessary.

    Parameters:
        alabel (str, optional): The label to check for in the DataFrame columns.
        df (pd.DataFrame, optional): The input DataFrame to check and potentially update.
        a_map (pd.DataFrame, optional): A DataFrame containing a mapping for label conversion.

    Returns:
        pd.DataFrame: The original DataFrame (df) if the label is present, or a new DataFrame
        with the label updated based on the provided mapping (a_map).

    This function checks if the specified 'alabel' exists as a column in the input DataFrame ('df').
    If the 'alabel' is found, the original DataFrame is returned as is. If 'alabel' is not present,
    it uses the mapping from 'a_map' to update the DataFrame. The mapping is indexed to the slug variable
    in survey data frame.
    """
    if alabel in df.columns:
        return df
    else:
        new_map = a_map[alabel]
        newdf = df.merge(new_map, left_on='slug', right_index=True, validate='many_to_one')
        return newdf


def use_parent_groups_or_gfrags(df, codes, label: str = None, gfrags: bool = True, parent_group: bool = False,
                                func: Callable = None, **kwargs) -> pd.DataFrame:
    """
    Process and aggregate survey data using parent groups or (gfrags, gfoams, gcaps) as required.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing survey data.
        codes (pd.DataFrame): The DataFrame containing code information.
        label (str, optional): The label to identify parent groups or gfrags.
        gfrags (bool, optional): If True, use gfrags (gfoams, gcaps) for processing.
        parent_group (bool, optional): If True, use parent groups for processing.
        func (Callable, optional): A custom data processing function. If provided,
            this function will be called with the provided keyword arguments (kwargs)
            for data processing.
        **kwargs: Additional keyword arguments that are passed to the data processing
            function (func).

    Returns:
        pd.DataFrame: The processed and aggregated survey data DataFrame.

    This function processes survey data based on the specified options, which can include using
    parent groups, gfrags, gfoams, gcaps, or a custom data processing function.

    If 'gfrags' and 'parent_group' are both True, it uses the default 'use_gfrags_gfoams_gcaps'
    function to process and aggregate the data. If only 'gfrags' is True, it still uses the same
    function. If 'parent_group' is True, it processes the data using parent groups.
    """
    
    if func is not None:
        return func(**kwargs)
    if gfrags and parent_group:
        df = use_gfrags_gfoams_gcaps(df.copy(), codes)
    if gfrags and not parent_group:
        df = use_gfrags_gfoams_gcaps(df.copy(), codes)
    
    # the surveys need to be aggregated to the object level
    # after changeing code names there will be duplicates on
    # the columns loc_date and code. Which is not allowed.
    groupby_cols = list(set([label, *df.columns, *conf_.code_result_columns]))
    df = aggregate_dataframe(df.copy(), groupby_cols, conf_.unit_agg)
    
    return df


def add_column_to_work_data(df, key: str = 'slug', feature: str = None, amap: pd.DataFrame = None) -> pd.DataFrame:
    # Merges additional location information to the survey results.
    
    d = df.merge(amap[feature], left_on=key, right_index=True, validate='many_to_one')
    
    return d


def add_columns_to_work_data(df, keys_features) -> pd.DataFrame:
    # iterates through a dictionary of column values and mappings
    # and adds the columns to the survey data
    
    d = df.copy()
    
    for k_f in keys_features:
        d = add_column_to_work_data(d, key=k_f['key'], feature=k_f['feature'], amap=k_f['map'])
    
    d.reset_index(inplace=True, drop=True)
    return d


def report_data(a_start, df, beaches, codes, add_columns: List = None, use_gfrags: bool = True):
    """
    Prepare data for generating a report.

    Parameters:
        a_start (dict): A dictionary containing report parameters, including 'start_date', 'end_date', and 'language'.
        df (pd.DataFrame): The input DataFrame containing survey data.
        beaches (pd.DataFrame): The DataFrame containing beach information.
        codes (pd.DataFrame): The DataFrame containing code information.
        add_columns (List, optional): A list of additional columns to add to the survey data.
        use_gfrags (bool, optional): If True, use gfrags (gfoams, gcaps) for data processing.

    Returns:
        Tuple[str, str, pd.DataFrame, pd.DataFrame]:
        A tuple containing the top label, report language, the data for the report, and the full processed data.

    This function prepares data for generating a report. It takes report parameters from 'a_start' and processes
    the survey data accordingly. It can optionally add additional columns to the data and use gfrags for processing.

    The 'a_start' dictionary should include 'start_date', 'end_date', and 'language' to specify the report's data range
    and language.

    If 'use_gfrags' is True, it processes the data using gfrags (gfoams, gcaps), and if 'add_columns' is provided, it
    adds the specified columns to the survey data.

    The function returns a tuple with the top label, report language, the data specifically for the report, and the full
    processed data.
    """
    
    # the first input variable sets the limit ot the report
    # that means we are interested about the summary of this data
    # or something contained withing it. This variable is used
    # the reporting process
    top_label = [list(a_start.keys())[0], list(a_start.values())[0]]
    
    # slice the survey data by the provided date
    w_d = slice_data_by_date(df.copy(), start=a_start['start_date'], end=a_start['end_date'])
    
    # check for and add to the survey data the group
    # and label for this report if it is missing
    w_d = check_for_top_label(top_label[0], df=w_d, a_map=beaches)
    
    # use gfrags or add columns to the survey data
    # by default the feature_type and code groupname
    # is added to the survey data.
    if use_gfrags:
        w_d = use_parent_groups_or_gfrags(w_d, codes, label=top_label[0])
    
    if add_columns is not None:
        w_d = add_columns_to_work_data(w_d, add_columns)
    
    # this is the data for report
    w_df = w_d[w_d[top_label[0]].isin([top_label[1]])].copy()
    
    return top_label, a_start['language'], w_df, w_d


geo_h =  ['project', 'parent_boundary', 'feature_type',  'feature_name', 'city', 'region', 'slug']


def categorize_work_data(df, labels, columns_of_interest: List[str] = geo_h, sample_id: str = 'loc_date'):
    """Categorizes and organizes data from a pandas DataFrame based on specified column labels.
    
    This function filters the DataFrame based on the given label criteria, then rearranges and summarizes the data according to the specified columns of interest and sample ID. The function dynamically adjusts the summary columns based on the label criteria and provides a unique set of attributes for each category.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to be categorized.
    - labels (List): A two-element list where the first element is the column name to filter by and the second element is the value to filter for in that column.
    - columns_of_interest (List[str], optional): List of column names that are of interest for the summary. Defaults to `geo_h`.
    - sample_id (str, optional): The column name to be used as the sample identifier. Defaults to 'loc_date'.
    
    Returns:
    - dict: A dictionary where keys are the attributes from 'columns_of_interest' and 'sample_id', and values are unique values for each attribute in the filtered data. The key for 'sample_id' is renamed to 'samples'.

    """
    
    
    data = df[df[labels[0]] == labels[1]].copy()
    
    summaries = columns_of_interest
    
    if labels[0] == columns_of_interest[-1]:
        summaries = columns_of_interest[:-2]
    if labels[0] == columns_of_interest[-2]:
        summaries = [*columns_of_interest[:-2], columns_of_interest[-1]]
    
    new_columns = list(set([sample_id, *summaries]))
    d = data[new_columns].copy()
    
    res = {}
    for an_attribute in new_columns:
        datt = d[an_attribute].unique()
        res.update({an_attribute: datt})
    
    res['samples'] = res.pop(sample_id)
    
    return {labels[1]: res}


def a_summary_of_one_vector(df, unit_columns: List[str] = None, unit_agg: dict = None, describe: str = 'pcs_m',
                            label: str = None, total_column: str = 'quantity'):
    """
    Generate a summary of a single vector (column) within a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing data.
        unit_columns (list): A list of columns to group and aggregate the data by.
        unit_agg (str or callable): The aggregation function to apply to the grouped data.
        describe (str, optional): The name of the column to summarize (default is 'pcs_m').
        label (str, optional): A label to describe the summarized data.

    Returns:
        pd.DataFrame: A DataFrame summarizing the specified column, including common statistics and total counts.

    This function generates a summary of a single vector (column) within the input DataFrame. It aggregates
    and groups the data by 'unit_columns' using the specified 'unit_agg' function, and then provides statistics
    for the specified 'describe' column.

    The summary includes common statistics such as count, mean, std, min, 25%, 50% (median), 75%, and max.
    Additionally, it calculates the total count and returns the summary as a DataFrame.

    If a 'label' is provided, it is included in the summary as a descriptive label.
    """
    sample_totals = aggregate_dataframe(df, unit_columns, unit_agg)
    sample_summary = sample_totals[describe].describe()
    sample_summary["total"] = sample_totals[total_column].sum()
    sample_summary = pd.DataFrame(sample_summary)
    sample_summary[describe] = sample_summary[describe].astype(object)
    sample_summary.loc['count', describe] = int(sample_summary.loc['count', describe])
    sample_summary.loc['total', describe] = int(sample_summary.loc['total', describe])
    
    if label is not None:
        sample_summary['label'] = label
    
    return sample_summary


def aggregate_boundaries(df: pd.DataFrame,
                         groupby_columns: list,
                         unit_agg: dict = None,
                         group_agg: dict = None,
                         boundary_labels: list = None,
                         boundary_columns: list = None) -> pd.DataFrame:
    """
    Aggregate data from a dataframe by boundaries and groups.

    Aggregates a dataframe in two steps. First, it performs
    aggregation at the 'unit' level defined by 'unit_columns' and 'unit_agg' to obtain
    test statistics. Then, it aggregates these 'unit' statistics further at the
    'boundary' level defined by 'boundary_labels' and 'boundary_columns', and computes
    the test statistics for each boundary.

    Args:
        df (pd.DataFrame): The input DataFrame containing data to be aggregated.
        groupby_columns (list): List of columns for 'unit' level aggregation.
        unit_agg (dict): Dictionary specifying the aggregation functions for 'unit' level.
        boundary_labels (list): List of boundary labels to define 'boundaries' for further aggregation.
        boundary_columns (list): List of columns for 'boundary' level aggregation.
        group_agg (dict): Dictionary specifying the aggregation functions for 'boundary' level.

    Returns:
        pd.DataFrame: A DataFrame containing aggregated data at the 'boundary' level with
        additional 'label' column indicating the boundary label.
    """
    
    unit_aggregate = aggregate_dataframe(df, groupby_columns=groupby_columns, aggregation_functions=unit_agg)
    if boundary_labels is None:
        d = aggregate_dataframe(unit_aggregate, groupby_columns=groupby_columns[-1:], aggregation_functions=group_agg)
        d['label'] = 'all'
        return d
    
    boundary_summaries = []
    for label in boundary_labels:
        boundary_mask = unit_aggregate[groupby_columns[0]] == label
        boundary_aggregate = unit_aggregate[boundary_mask].groupby(boundary_columns, as_index=False).agg(group_agg)
        boundary_aggregate['label'] = label
        boundary_summaries.append(boundary_aggregate)
    
    return pd.concat(boundary_summaries)

def a_cumulative_report(df, feature_name: str = 'feature_type',
                        object_column: str = 'groupname',
                        sample_id: str = 'loc_date',
                        group_agg: dict = conf_.agg_groups,
                        unit_agg: dict = conf_.unit_agg,
                        table_split: list = None,
                        pivot_values: str = 'pcs_m') -> pd.DataFrame:
    """
     Generate a cumulative report by aggregating specified features and objects.

     This function creates a cumulative report by aggregating data from the input DataFrame
     based on the specified feature, object, and sample identifiers. It performs aggregation at
     both the 'unit' level (defined by feature, sample_id, and object_column) and the 'boundary'
     level (defined by feature and object_column).

     Args:
         df (pd.DataFrame): The input DataFrame containing data to be aggregated.
         feature_name (str): The column name representing the feature to be aggregated (default is 'feature_type').
         object_column (str): The column name representing the objects (default is 'groupname').
         sample_id (str): The column name representing the sample identifier (default is 'loc_date').
         group_agg (dict): Dictionary specifying the aggregation functions for 'boundary' level (default is conf_.agg_groups).
         unit_agg (dict): Dictionary specifying the aggregation functions for 'unit' level (default is conf_.unit_agg).
         pivot_values (str): The values to pivot for the resulting DataFrame (default is 'pcs_m').

     Returns:
         pd.DataFrame: A DataFrame containing the cumulative report with aggregated values.

    """
   
    unit_columns = [feature_name, sample_id, object_column]
    object_columns = [object_column]
    boundary_labels = df[feature_name].unique()
    

    
    # the parent summary
    # calling boundary_labels=None will return a summary of all parent features
    p_boundary = aggregate_boundaries(df,
                                      groupby_columns=unit_columns,
                                      unit_agg=unit_agg,
                                      boundary_labels=None,
                                      boundary_columns=object_columns,
                                      group_agg=group_agg)
    
    # the summary of the child features
    if table_split is not None:
        
        
        boundary_summaries = aggregate_boundaries(df[df[feature_name].isin(table_split)].copy(),
                                              groupby_columns=unit_columns,
                                              unit_agg=unit_agg,
                                              boundary_labels=boundary_labels,
                                              boundary_columns=object_columns,
                                              group_agg=group_agg)
    else:
        boundary_summaries = aggregate_boundaries(df,
                                              groupby_columns=unit_columns,
                                              unit_agg=unit_agg,
                                              boundary_labels=boundary_labels,
                                              boundary_columns=object_columns,
                                              group_agg=group_agg)
        
    cumulative = pd.concat([boundary_summaries, p_boundary])
    x = cumulative.pivot(columns=['label'], index=object_columns, values=[pivot_values])
    
    return x.droplevel(0, axis=1)


class ReportClass:
    """
    A class for generating and managing reports based on survey data and specified criteria.

    Parameters:
        w_df (pd.DataFrame, optional): The survey data DataFrame for report generation.
        boundaries (dict, optional): A dictionary defining the reporting boundaries, including 'start_date',
            'end_date', and 'language'.
        top_label (List, optional): A list containing two elements - [label_column, label_value].
        language (str, optional): The language in which the report is generated.
        lang_maps (pd.DataFrame, optional): A DataFrame containing language mapping data.
        mc_criteria_one (dict, optional): The first criteria for identifying objects of interest.
        mc_criteria_two (dict, optional): The second criteria for identifying objects of interest.
        ooi (str, optional): The name of the object of interest column.

    Attributes:
        w_df (pd.DataFrame): The survey data DataFrame for report generation.
        boundaries (dict): Reporting boundaries, including 'start_date', 'end_date', and 'language'.
        top_label (List): The label for the report, containing label_column and label_value.
        language (str): The language in which the report is generated.
        lang_maps (pd.DataFrame): Language mapping data.
        criteria_one (dict): The first criteria for identifying objects of interest.
        criteria_two (dict): The second criteria for identifying objects of interest.
        ooi (str): The name of the object of interest column.

    Methods:
        - features: Get a list of available features for report generation.
        - available_features: Get a list of available features based on predefined criteria.
        - inventory: Get an inventory of objects with summary statistics.
        - most_common: Find the most common objects based on criteria.
        - summarize_feature_labels: Summarize data for a specific feature.
        - the_number_of_attributes_in_a_feature: Count attributes in a feature.
        - __repr__: Return a string representation of the ReportClass instance.

    This class is designed for generating and managing reports based on survey data and customizable criteria.
    It provides various methods for data processing, aggregation, and report generation based on specified parameters.
    """
    # default arguments that define the most common objects
    # this assumes that the columns quantity and fail rate exist

    # a ranking criteria based off of the quantity column
    column_one = {
        
        'column': 'quantity',
        'val': 10
    }
    
    # a ranking criteria based off of the fail rate column
    column_two = {
        'column': 'fail rate',
        'val': 0.5
    }
    
    object_of_interest = 'code'
    
    def __init__(self, w_df: pd.DataFrame = None,
                 boundaries: dict = None,
                 top_label: List[str] = None,
                 language: str = None,
                 lang_maps: pd.DataFrame = None,
                 mc_criteria_one: dict = column_one,
                 mc_criteria_two: dict = column_two,
                 ooi=object_of_interest
                 ):
        self.w_df = w_df
        self.boundaries = boundaries
        self.top_label = top_label
        self.language = language
        self.lang_maps = lang_maps
        self.criteria_one = mc_criteria_one
        self.criteria_two = mc_criteria_two
        self.ooi = ooi
    
    @property
    def features(self):
        args = dict(df=self.w_df, labels=self.top_label, columns_of_interest=geo_h)
        some_features = categorize_work_data(**args)
        return some_features[self.top_label[1]]
    
    @property
    def available_features(self):
        available = [x for x in geo_h if x in self.features.keys()]
        return available
    
    @property
    def inventory(self, code: str = 'code', sample_id: str = 'loc_date'):
        # sum the cumulative quantity for each code and calculate the median pcs/meter
        code_totals = aggregate_dataframe(self.w_df.copy(), [code], conf_.agg_groups)
        
        # collect
        abundant = get_top_x_records_with_max_quantity(code_totals.copy(), "quantity", code,
                                                       len(code_totals.code.unique()))
        
        # identify the objects that were found in at least 50% of the samples
        # calculate the quantity per sample for each code and sample
        occurrences = aggregate_dataframe(self.w_df, [sample_id, code], {"quantity": "sum"})
        
        # count the number of times that an object was counted > 0
        # and divide it by the total number of samples
        event_counts = count_objects_with_positive_quantity(occurrences)
        
        # calculate the rate of occurrence per unit of measure
        rates = calculate_rate_per_unit(self.w_df.copy(), self.w_df.code.unique())
        
        # add the unit rates and fail rates
        abundance = merge_dataframes_on_column_and_index(abundant, rates["pcs_m"], left_column=code,
                                                         validate="one_to_one")
        abundance["fail rate"] = abundance.code.apply(lambda x: event_counts.loc[x])
        
        # this is the complete inventory with summary
        # statistics for each object
        abundance.sort_values(by="quantity", inplace=True, ascending=False)
        abundance.reset_index(inplace=True, drop=True)
        
        return abundance
    
    @property
    def most_common(self):
        # use the criteria to find the objects of interest
        mc = display_tabular_data_by_column_values(self.inventory, self.criteria_one, self.criteria_two, self.ooi)
        weight = mc[["quantity", "%"]].sum().to_dict()
        return mc, weight
    
    @property
    def a_short_description(self):
        t_q = self.inventory.quantity.sum()
        r_type, r_name = self.top_label[0], self.top_label[1]
        start, end = self.boundaries['start_date'], self.boundaries['end_date']
        n_samples = len(self.features["samples"])
        
        data = [r_type, r_name, start, end, n_samples, t_q]
        index = ['type', 'name', 'start', 'end', 'samples', 'quantity']
        columns = ['Report']
        
        return pd.DataFrame(data, index=index, columns=columns)
    
        
    
    def summarize_feature_labels(self,
                                 feature: str = None,
                                 sample_id: str = 'loc_date',
                                 location: str = 'slug',
                                 describe_column: str = 'pcs_m',
                                 unit_agg: dict = conf_.unit_agg,
                                 **kwargs):
        if feature is None:
            feature = self.available_features[0]
            print('\nThis is the default summary. A column label can be specified.')
            print(f'This summary is for {feature}')
            print('To specify a feature call class.summarize_feature_labels(<column-label>)')
            print(f'these are your choices {self.available_features}\n')
        
        unit_columns = [sample_id, location, feature]
        labels = self.features[feature]
        
        x = []
        for the_label in labels:
            d = self.w_df[self.w_df[feature] == the_label].copy()
            ds = a_summary_of_one_vector(d.copy(),
                                         unit_columns=unit_columns,
                                         unit_agg=unit_agg,
                                         describe=describe_column,
                                         label=the_label, **kwargs)
            x.append(ds)
        
        return pd.concat(x).pivot(columns='label')
    
    def the_number_of_attributes_in_a_feature(self, feature: str = None):
        
        if feature is None:
            feature = self.available_features[0]
            print('\nThis is the default attribute count. A column label can be specified.')
            print(f'This count is for {feature}')
            print('To specify call the_number_of_attributes_in_a_feature(<column-label>)')
            print(f'these are your choices {self.available_features}\n')
        labels = self.features[feature]
        
        feature_attributes = []
        for a_label in labels:
            these_attributes = categorize_work_data(self.w_df[self.w_df[feature] == a_label].copy(), self.top_label)
            summed = {k: len(v) for k, v in these_attributes[self.top_label[1]].items()}
            feature_attributes.append(summed)
        counts = pd.DataFrame(feature_attributes, index=labels)
        counts = counts[['city', 'feature_name', 'samples']]
        
        return counts

    def feature_labels(self, available_features: List[str] = None, labels_for: dict = {'feature_name': 'unique', 'city': 'unique'}):
        
        data = self.w_df.copy()
        if available_features is None:
            available_features = ['feature_type']
        f_labels = {}
        for a_feature in available_features:
            d = data[a_feature].unique()
            for item in d:
                l = data[data[a_feature] == item].agg(labels_for).to_dict()
                labels = {item: l}
                f_labels.update(labels)
        return f_labels

    def a_subreport(self, feature_of_interest: str = None, key: str = 'feature_name'):
        new_boundaries = {
            key: feature_of_interest,
            'language': self.boundaries['language'],
            'start_date': self.boundaries['start_date'],
            'end_date': self.boundaries['end_date']
        }
        top_label = [key, feature_of_interest]
        d = self.w_df[self.w_df[key] == feature_of_interest].copy()
        a_subreport = ReportClass(d, new_boundaries, top_label, new_boundaries['language'], self.lang_maps)
        return a_subreport
    
    def __repr__(self):
        return f'Report: {self.boundaries}, features: {self.available_features}'
    