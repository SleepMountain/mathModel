from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 加载数据集
iris = load_iris()
X, y = iris.data, iris.target

# 创建包含标准化和KNN的管道
clf = Pipeline([
    ('scaler', StandardScaler()),  # 标准化数据
    ('knn', KNeighborsClassifier(n_neighbors=11))  # KNN分类器
])

# 训练模型
clf.fit(X, y)

# 进行预测
sample = [[5.1, 3.5, 4, 0.2]]
prediction = clf.predict(sample)
prediction_proba = clf.predict_proba(sample)

print(f"预测类别: {prediction}")
print(f"类别概率: {prediction_proba}")
print(f"类别名称: {iris.target_names[prediction[0]]}")