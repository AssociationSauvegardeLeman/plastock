data/end_pipe/macro_current.csv
data/end_pipe/pstock_beaches_current.csv
data/end_pipe/codes.csv
data/end_pipe/lac_leman_regions.csv
data/end_pipe/asl_beaches.csv
data/end_pipe/u_pstk.csv
data/end_pipe/iqaasl.csv
data/end_pipe/hist_leman.csv
data/end_pipe/swt_all.csv
data/end_pipe/long_form_micro.csv
data/end_pipe/geo_long_form.csv
data/end_pipe/micro_results.csv

resources/maps/annex_map_regions.jpeg
resources/maps/chapter_three_map.jpg.jpeg
resources/maps/chapter_two_map.jpg.jpeg
resources/maps/regions_map.jpeg

setvariables
plastockconf
plastock
reportclass

! removed set variables by assigning values to plastockconf !
setvariables

* format_kwargs
* unit_agg
* table_css_styles

plastockconf

name_zones, name_frequentation, name_situation
name_substrate, name_distance, table_css_styles, table_css_styles_top

plastock 

add_table_to_page, capitalize_x_tick_labels, capitalize_x_and_y_axis_labels,
capitalize_legend_components, attribute_summary

reportclass
use_gfrags_gfoams_gcaps
language_maps
ReportClass
translated_and_style_for_display
a_cumulative_report
a_summary_of_one_vector
