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

header_row = {'selector': 'th:nth-child(1)', 'props': f'background-color: #FFF;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': f'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 14px; padding:10px;'}
caption_bottom = {'selector': 'caption','props': 'caption-side: bottom; font-size:16px; text-align: left; margin-top:15px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row, caption_bottom]

