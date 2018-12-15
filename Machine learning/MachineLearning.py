from sklearn import tree
from sklearn import datasets

# Very simple machine learning example
# The point of this script is to show some
# kind of example regarding how models are
# trained how to make predictions

# Each array is a bunch of coordinates
features = [[63,64,65,66], [64,65,66,67], [62,63,64,65],[50,51,52,53], [51,52,53,54]]

# Map some names to the arrays
labels = [60, 60, 60, 50, 50]
classifier = tree.DecisionTreeClassifier()

# fit = Find Patterns in Data
classifier = classifier.fit(features, labels)

# predict which name the array [65,66,67,68] most likely would have
print(classifier.predict([[65,66,67,68]]))

# result is 60
