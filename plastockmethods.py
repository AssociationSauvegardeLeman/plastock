name_the_zones = {1:"ligne-d'eau", 2:"plage-seche"}

name_the_particles = {
    "fbr":"fibre rouge",
    "fbb":"fibre bleu",
    "fbj":"fibre jaune",
    "fbt":"fibre transparent",
    "fbn":"fibre noire",
    "fba":"fibre autre",
    "frr":"fragment rigide rouge",
    "frb":"fragment rigide bleu",
    "frj":"fragment rigide jaune",
    "frt":"fragment rigide transparent",
    "frn":"fragment rigide noire",
    "fra":"fragment rigide autre",
    "fsr":"fragment souple rouge",
    "fsb":"fragment souple bleu",
    "fsj":"fragment souple jaune",
    "fst":"fragment souple transparent",
    "fsn":"fragment souple noire",
    "fsa":"fragment souple autre",
}

frequentation_name = {
    1:"faible",
    2:"moyenne",
    3:"élévée"
}

situation_name = {
    1: "campagne",
    2: "urbain"
}

particle_groups = {
    "fibres":"fibre",
    "fdure":"fragment rigide",
    "souple":"fragment souple"
}

name_the_substrate = {
    1:"sable fin",
    2:"sable grosssier",
    3:"gravier",
    4:"galet"
}

name_the_distance = {
    1: "< 100m",
    2: "100 - 500m",
    3: "500 - 1000m",
    4: "> 1000m"
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
table_font = {'selector': 'tr', 'props': 'font-size: 12px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row]
