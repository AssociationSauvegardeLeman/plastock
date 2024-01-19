# DATA README

The historical data of all the beach litter surveys on Lac Léman. This data was collected and or maintained by hammerdirt. Over the years different organizations have done beach litter surveys using the MLW system. There was no official _maintainer_ of the data. The role was assumed by hammerdirt, a local association from Montreux, Switzerland.

The data uses the MLW codes from ([Guidance on Monitoring Marine Litter](https://mcc.jrc.ec.europa.eu/documents/201702074014.pdf)). The code definitions have been translated to french and german, new codes have been added that represent items that are found regularly but are not in the original code base. 

## Data files and description

__This concerns only the contents of the end_pipe file__

1. data/end_pipe/asl_beaches.csv: GPS and location specific details

2. data/end_pipe/city_map.csv: maps beach name to city

3. data/end_pipe/codes.csv: code definitions and matrerial data

4. data/end_pipe/de_labels.csv: converts common english labels to german

5. data/end_pipe/fr_labels.csv: converts common english labels to french

6. data/end_pipe/hist_leman.csv: the historical data for lac leman

7. data/end_pipe/lac_leman_regions.csv: maps the beach name to a region

8. data/end_pipe/micro_results.csv: the cleaned survey results of the microplastics in wide form

9. data/end_pipe/macro_current.csv: the litter survey results

10. data/end_pipe/macro_data_linearm.csv: the data used in the previous results chapter (aggregated to linear meters)

11. data/end_pipe/macro_data_msquared.csv: the data used in the Macro dechets chapter (aggregated to m²)

12. data/end_pipe/long_form_micro.csv: The cleaned survey results of the microplastics in long form

13. data/end_pipe/pstock_beaches_current.csv: Maps beach name to feature variables

14. data/end_pipe/swt_all.csv: The 2023 survey results from Saint Sulpice

## Resources

### Maps and images

1. resources/maps/annex_map_regions.jpeg: Map with cummulative totals by region and points for min and max values.

2. resources/maps/chapter_two_map.jpg.jpeg: Chapter two Map of average pcs of trash per meter squared

3. resources/maps/chapter_three_map.jpg.jpeg: Chapter three map of average pcs of trach per meter of shore line

4. resources/maps/regions_map.jpeg: Display of the survey locations and the regions they are assigned to.

### Map data:

1. resources/maps/plastock_lm.csv: the data to make the chapter three maps (plastock results)

2. resources/maps/plastock_mq.csv: the data to make the chpater two maps

3. resources/maps/previous_results.csv: the data to make the chapter three maps (previous results)

## shape files

1. resources/shape_files/leleman.shp: Shape file of the outline of Le Léman
2. resources/shape_files/plastock_beaches.shp: Shape file of survey location points