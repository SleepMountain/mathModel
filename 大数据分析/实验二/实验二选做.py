from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.inspection import DecisionBoundaryDisplay
import time
import timeit  # 更精确的时间测量

# 加载数据
iris = load_iris(as_frame=True)
X = iris.data[["sepal length (cm)", "sepal width (cm)"]]
y = iris.target.values
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=0)

# 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# 朴素KNN实现（优化版）
class NaiveKNN:
    def __init__(self, n_neighbors=5, weights='uniform'):
        self.n_neighbors = n_neighbors
        self.weights = weights

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        predictions = []
        for x in X:
            # 向量化计算距离
            distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))

            # 获取最近的k个邻居
            nearest_indices = np.argpartition(distances, self.n_neighbors)[:self.n_neighbors]
            nearest_labels = self.y_train[nearest_indices]

            if self.weights == 'uniform':
                counts = np.bincount(nearest_labels)
                pred = np.argmax(counts)
            else:
                nearest_distances = distances[nearest_indices]
                weights = 1 / (nearest_distances + 1e-8)
                weighted_counts = np.zeros(len(np.unique(self.y_train)))
                for label, weight in zip(nearest_labels, weights):
                    weighted_counts[label] += weight
                pred = np.argmax(weighted_counts)

            predictions.append(pred)
        return np.array(predictions)


# 创建分类器
naive_knn = NaiveKNN(n_neighbors=11, weights='uniform')
sklearn_knn = KNeighborsClassifier(n_neighbors=11, weights='uniform')

# 训练模型
naive_knn.fit(X_train_scaled, y_train)
sklearn_knn.fit(X_train_scaled, y_train)


# 更精确的时间测量（重复多次取平均）
def measure_time(clf, X, repetitions=10):
    def predict():
        return clf.predict(X)

    return timeit.timeit(predict, number=repetitions) / repetitions


# 测量预测时间
naive_time = measure_time(naive_knn, X_test_scaled)
sklearn_time = measure_time(sklearn_knn, X_test_scaled)

# 进行预测
y_pred_naive = naive_knn.predict(X_test_scaled)
y_pred_sklearn = sklearn_knn.predict(X_test_scaled)

# 评估性能
print("\n性能对比:")
print(f"sklearn KNN准确率: {accuracy_score(y_test, y_pred_naive):.4f}, 平均预测时间: {naive_time:.6f}秒")
print(f"朴素KNN准确率: {accuracy_score(y_test, y_pred_sklearn):.4f}, 平均预测时间: {sklearn_time:.6f}秒")
print(f"sklearn比朴素实现快 {sklearn_time / naive_time:.1f}倍")

# 可视化决策边界（仅展示部分数据点以加快速度）
_, axs = plt.subplots(ncols=2, figsize=(16, 6))

# 为可视化准备网格数据（减少网格点数以加快速度）
xx, yy = np.meshgrid(
    np.linspace(X_test_scaled[:, 0].min() - 1, X_test_scaled[:, 0].max() + 1, 50),
    np.linspace(X_test_scaled[:, 1].min() - 1, X_test_scaled[:, 1].max() + 1, 50),
)
grid = np.c_[xx.ravel(), yy.ravel()]

# 朴素KNN决策边界（只计算部分点）
start = time.time()
naive_preds = naive_knn.predict(grid).reshape(xx.shape)
print(f"\nsklearn KNN绘制决策边界用时: {time.time() - start:.2f}秒")

axs[0].contourf(xx, yy, naive_preds, alpha=0.5)
axs[0].scatter(X_train_scaled[::2, 0], X_train_scaled[::2, 1], c=y_train[::2], edgecolors='k')
axs[0].set_title(f"sklearn KNN (预测时间: {naive_time:.4f}s)")

# sklearn KNN决策边界（只计算部分点）
start = time.time()
sklearn_preds = sklearn_knn.predict(grid).reshape(xx.shape)
print(f"朴素KNN绘制决策边界用时: {time.time() - start:.2f}秒")

axs[1].contourf(xx, yy, sklearn_preds, alpha=0.5)
axs[1].scatter(X_train_scaled[::2, 0], X_train_scaled[::2, 1], c=y_train[::2], edgecolors='k')
axs[1].set_title(f"朴素KNN (预测时间: {sklearn_time:.4f}s)")

plt.tight_layout()
plt.show()