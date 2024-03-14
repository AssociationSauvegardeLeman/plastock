# Conclusion

## Microplastiques

### Stock de microplastiques sur les plages du Léman

Pour extrapoler à l’ensemble des plages du Léman, la superficie a été estimée sur la base d’orthophotos et en se référant à la liste des plages de la CIPEL. Cette liste a été adaptée car certaines plages sont uniquement des espaces de baignade dépourvues de grèves "naturelles" (enrochements, dalles en pierres ou en béton, etc.).

De plus, trois plages faisant partie de l’étude ont été rajoutées à la liste globale. Il s’agit d’une plage semi-privée à Crans, de la plage de la Pichette sur la commune de Corseaux et de la plage de l’Empereur à Noville (Grangettes). Au total, la superficie des 90 plages retenues correspond à 68’399 m² pour un linéaire de 12'688 m. Selon cette estimation, la contamination plastique s'élève à 524'346'734 particules sur les plages du Léman en se basant sur la moyenne pondérée et 1'232’071'187 sans pondération. La valeur pondérée correspond à une interprétation des résultats sur la base de l’étude de Constant et al. 2019 qui a déterminé des coefficients d’identification pour chaque forme de particule. Ils sont respectivement de 0.37 pour les fibres, de 0.5 pour les particules rigides et de 0.74 pour les particules souples. Ces coefficients ont donc été appliqués aux données du projet pour avoir un aperçu des résultats.

### Comparaison avec d'autres études

Avec le tableau ci-dessous, il est visible que les abondances mesurées dans le cadre de l’étude Pla’stock sont largement supérieures à la moyenne mesurée en 2014 sur le Léman et les autre lac Suisse. La comparaison avec la Méditerranée est encore plus flagrante.

:::{card} Etudes précedentes
:margin: 3
<b>Tableau 5.3: </b>Comparaison avec d’autres études ayant comptabilisé des microplastiques sur les plages.
+++

{glue}`previous_studies`

:::



### Prédiction des abondances
Rajouter les éléments de prédiction par grille bayésienne


Source : solid-waste-team

prior : beta(1,1)
Les résultats présentés ci-dessus correspondent à ce qui a été réellement mesuré sur le terrain. Ce sont donc les valeurs de référence et de comparaison pour faire le lien avec les études précédentes. Aujourd'hui, certains outils mathématiques, tel que l'approximation par grille bayésienne, permettent d'établir une prédiction des abondances réelles sur les plages du Léman. 


Mise en œuvre : Implique la définition d'une grille de valeurs de paramètres et le calcul de la vraisemblance des données observées à chaque point de cette grille. En multipliant par la probabilité a priori et en normalisant, on obtient la distribution a posteriori. Cela peut être fait pour chaque condition séparément ou pour toutes les conditions ensemble, bien que cela soit plus intensif en termes de calcul.


## Macroplastiques


### Estimation du stock sur les plages du Léman

Pour extrapoler à l’ensemble des plages du Léman, la longueur a été estimée sur la base d’orthophotos et en se référant à la liste des plages de la CIPEL. Cette liste a dû être adaptée car certaines plages sont uniquement des espaces de baignade dépourvues de grèves sableuses ou avec des galets (enrochements, dalles en pierres ou en béton…). A l’inverse, 3 plages faisant partie de l’étude ont été rajoutées. Il s’agit d’une plage semi-privée à Crans, de la plage de la Pichette sur la commune de Corseaux et de la plage de l’Empereur à Noville (Grangettes). 
Sur les 12'688 m de plages publiques, en extrapolant la moyenne de 3,42 pièces par mètre recensés dans le cadre du projet Pla’stock, il y aurait 43'392 morceaux de plastiques sur les plages publiques du Léman.

### Comparaison avec d’autres études

Les résultats de Pla’stock suggèrent que les quantités de certains déchets sauvages sont en baisse. Dans l’ensemble, l’étude fait état d’une valeur médiane de 2 pcs/m contre 3,7 à 4,4 pcs/m dans le passé. Cette réduction est conforme aux conclusions de 2020 - 2021 mais plus importante que prévue (SLR - IQAASL). A noter que l’effort de collecte adopté par les première et troisième études est comparable à celui consenti par Pla’stock.

:::{card} Résultats précédents
:margin: 3
<b>Tableau 5.9</b> Comparaison des résultats des campagnes de collecte de déchets sauvages au bord du Léman entre 2015 et 2022, déchets par mètre de rivage, nombre d’échantillons et nombre total de déchets récoltés.
^^^

{glue}`table_ten`

:::

Les déchets dont la concentration sur les plages a le plus fortement diminué sont ceux liés à la consommation personnelle (mégots de cigarettes, emballages de snacks et bouchons de bouteilles en plastique). La diminution marquée de la densité de cotons-tiges en plastique (0,03 pcs/m contre 0,13 pcs/m) est inattendue et pourrait être attribuée à l’interdiction de la vente de ces articles en France.

Sur la base des différentes sessions d’échantillonnage de ces dernières années, il est possible de prédire les abondances qui seront retrouvées sur les plages du Léman. Deux outils permettent de calculer ces prédictions : random forest et bayesian grid.

::::{grid} 1 1 2 2
:::{grid-item-card} Random forest

Tableau : prédictions random forest
+++
<b>Tableau XXX</b>  Prédiction du nombre de pièce par mètre linéaire avec Random forest
:::

:::{grid-item-card} Grid approximation

Tableau :prédictions grid approx
+++
<b>Tableau XXX</b>  Prédiction du nombre de pièce par mètre linéaire avec approximation Bayésienne par Grille
:::

:::{grid-item-card} extrapolation des résulats

Tableau : stock

+++
<b>Tableau XXX</b> Déchets présents sur les plages du Léman


:::
::::


## Discussion générale

En conclusion à cette étude, une grande disparité d’abondance est observable entre les différentes plages et ce, tant pour les micro que les macroplastiques. Une pareille étude à l’échelle de la plage montrerait certainement une même hétérogénéité au vu de l’importance des zones d’accumulations. Parmi les variables testées, et bien que des variations soient visibles, aucune ne se démarque comme déterminante de la pollution plastique. Pour autant, une plage de sable, à proximité d’un parking et avec une forte fréquentation risque d’être plus fortement impactée qu’une plage de galets isolée. 
Les comparaisons avec des études antérieures montrent une nette augmentation des concentrations en microplastiques depuis l’étude de De Alencastro et Faure en 2014. A l’inverse, les abondances en macroplastiques tendent à diminuer légèrement. Cette évolution sera intéressante à suivre lors de futures études.
Au niveau des microplastiques identifiés, les fibres anthropiques sont largement dominantes. Ceci démontre le rôle important de l’abrasion des textiles comme apport de microplastiques dans l’environnement. 
Pour les macroplastiques, un point à relever est l’importance fragmentation observée sur les déchets récoltés. En effet, plus de la moitié des objets triés n’étaient plus identifiables. Parmi les éléments les plus fréquemment rencontrés, se retrouvent les mégots, les emballages alimentaires et les pellets industriels.
Des tests sont actuellement en cours dans le cadre d’un travail de Master avec l’Université de Genève. 
Ouverture: Plus ample études à mener sur la courantologie car variables testées influences de manière negligeable. Des tests sur les apports des principaux cours d'eau sont en cours dans le cadre d'un travail de master avec l'UNIGE. Il serait également intéressant de pouvoir tester l’influence des vents et des courants sur la distribution des plastiques autour du lac. L’exemple des Grangettes et du Bouveret, où l’effet combiné de la proximité du Rhône et de contre-courants ramenant les déchets vers les rives montre bien l’influence que peuvent avoir ces variables.
