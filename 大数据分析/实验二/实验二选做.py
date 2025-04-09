import numpy as np
from collections import Counter
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


# 1. 朴素KNN实现
class NaiveKNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict(self, X_test):
        predictions = []
        for x in X_test:
            # 计算欧氏距离
            distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
            # 获取最近的k个邻居的索引
            k_indices = np.argsort(distances)[:self.k]
            # 获取邻居的标签
            k_nearest_labels = self.y_train[k_indices]
            # 多数表决
            most_common = Counter(k_nearest_labels).most_common(1)
            predictions.append(most_common[0][0])
        return np.array(predictions)


# 2. 加载并准备数据
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. 数据标准化（KNN对尺度敏感）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 朴素KNN训练预测
naive_knn = NaiveKNN(k=5)
naive_knn.fit(X_train_scaled, y_train)
naive_pred = naive_knn.predict(X_test_scaled)
naive_acc = accuracy_score(y_test, naive_pred)

# 5. sklearn KNN训练预测
sklearn_knn = KNeighborsClassifier(n_neighbors=5)
sklearn_knn.fit(X_train_scaled, y_train)
sklearn_pred = sklearn_knn.predict(X_test_scaled)
sklearn_acc = accuracy_score(y_test, sklearn_pred)

# 6. 结果对比
print("\n=== 结果对比 ===")
print(f"朴素KNN准确率: {naive_acc:.4f}")
print(f"sklearn KNN准确率: {sklearn_acc:.4f}")

# 7. 预测样例对比
sample_idx = 0
print("\n=== 单样本预测对比 ===")
print(f"真实类别: {y_test[sample_idx]} ({iris.target_names[y_test[sample_idx]]})")
print(f"朴素KNN预测: {naive_pred[sample_idx]} ({iris.target_names[naive_pred[sample_idx]]})")
print(f"sklearn预测: {sklearn_pred[sample_idx]} ({iris.target_names[sklearn_pred[sample_idx]]})")

# 8. 预测概率对比（朴素实现无此功能）
print("\n=== 预测概率 ===")
print("sklearn预测概率:")
print(sklearn_knn.predict_proba(X_test_scaled[sample_idx:sample_idx + 1]))