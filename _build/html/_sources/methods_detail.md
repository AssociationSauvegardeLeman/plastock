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

