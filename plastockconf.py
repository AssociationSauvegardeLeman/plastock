name_zones = {1:"ligne d'eau", 2:"plage seche"}

name_particles = {
    "fbr":"fibre rouge",
    "fbb":"fibre bleu",
    "fbj":"fibre jaune",
    "fbt":"fibre transparent",
    "fbn":"fibre noire",
    "fba":"fibre autre",
    "frr":"particule rigide rouge",
    "frb":"particule rigide bleu",
    "frj":"particule rigide jaune",
    "frt":"particule rigide transparent",
    "frn":"particule rigide noire",
    "fra":"particule rigide autre",
    "fsr":"particule souple rouge",
    "fsb":"particule souple bleu",
    "fsj":"particule souple jaune",
    "fst":"particule souple transparent",
    "fsn":"particule souple noire",
    "fsa":"particule souple autre",
}

name_frequentation = {
    1:"Faible",
    2:"Moyenne",
    3:"Elevée"
}

freq_ord = ['Faible', 'Moyenne', 'Élévée']

name_situation = {
    1: "Campagne",
    2: "Urbain"
}

particle_groups = {
    "fibres":"Fibre",
    "fdure":"Particule rigide",
    "souple":"Particule souple"
}

name_substrate = {
    1:"Sables fins",
    2:"Sables grossiers",
    3:"Graviers",
    4:"Cailloux"
}

name_distance = {
    1: "< 100 m",
    2: "100 - 500 m",
    3: "500 - 1000 m",
    4: "> 1000 m"
}

# colors
zone_palette = {"plage-seche":"darkgoldenrod","ligne-d'eau":"lightseagreen"}

region_palette = {"GE":"darkgoldenrod","VD":"lightseagreen"}

substrate_colors = {
    1:"wheat",
    2:"burlywood",
    3:"lightslategrey",
    4:"darkslategrey"
}

header_row = {'selector': 'th:nth-child(1)', 'props': 'background-color: #FFF; white-space: nowrap; word-break: keep-all;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': 'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 14px; padding:6px;'}
t_data = {'selector': 'td', 'props': 'padding:4px; text-align: center;'}
caption_bottom = {
    'selector': 'caption',
    'props': 'caption-side: bottom; font-size:14px; text-align: left; margin-top:14px;'
}
caption_top = {'selector': 'caption','props': 'caption-side: top; font-size:12px; text-align: left; margin-top:12px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row, t_data, caption_bottom]
table_css_styles_top = [even_rows, odd_rows, table_font, t_data, header_row, caption_top]

# the formatting for pd.styler
format_kwargs = dict(precision=2, thousands="'", decimal=",")

# these are the columns and methods used to aggregate the data at the sample level
# the sample level is the lowest level of aggregation. The sample level the collection of all
# the records that share the same loc_date. The loc_date is the unique identifier for each survey.
unit_agg = {
    "quantity":"sum",
    "pcs_m": "sum"
}

# Once the data is aggregated at the sample level, it is aggregated at the feature level. The pcs/m or pcs_m
# column can no longer be summed. We can only talk about the median, average or distribution of the pcs/m for the
# samples contained in each feature. The quantity column can still be summed. The median is used for reporting
# purposes. The median is less sensitive to outliers than the average. The median is also more intuitive than the
# average.
agg_groups = {
    "quantity":"sum",
    "pcs_m": "median"
}
