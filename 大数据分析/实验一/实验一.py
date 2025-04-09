from sklearn.datasets import load_iris #下载数据集
from sklearn import tree #导入包

iris = load_iris() #加载数据集
X, y = iris.data, iris.target #加载数据集
clf = tree.DecisionTreeClassifier() #建立空模型
clf = clf.fit(X, y) #构建决策树
tree.plot_tree(clf) #绘制决策树
print(clf.predict([[5.1, 3.5, 4, 0.2]])) #使用决策树
