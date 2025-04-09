# 数据生成与预处理
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)
X = StandardScaler().fit_transform(X)

# 原始数据可视化
plt.scatter(X[:, 0], X[:, 1], s=10)
plt.title("Raw Data")
plt.show()

from sklearn.cluster import DBSCAN
import numpy as np

# 参数实验
params = [
    {'eps': 0.3, 'min_samples': 5},  # 默认参数
    {'eps': 0.3, 'min_samples': 15},  # 增大min_samples
    {'eps': 0.5, 'min_samples': 10}  # 增大eps
]

for param in params:
    db = DBSCAN(**param).fit(X)
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    plt.scatter(X[:, 0], X[:, 1], c=labels, s=10, cmap='viridis')
    plt.title(f"eps={param['eps']}, min_samples={param['min_samples']}\nClusters={n_clusters}")
    plt.show()

    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=3).fit(X)
    kmeans_labels = kmeans.predict(X)

    # 对比可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.scatter(X[:, 0], X[:, 1], c=db.labels_, s=10, cmap='viridis')  # DBSCAN
    ax1.set_title("DBSCAN (Clusters=3)")
    ax2.scatter(X[:, 0], X[:, 1], c=kmeans_labels, s=10, cmap='viridis')  # KMeans
    ax2.set_title("KMeans (k=3)")
    plt.show()

    # 自动选择最佳eps（k距离曲线法）
    from sklearn.neighbors import NearestNeighbors

    neigh = NearestNeighbors(n_neighbors=15)
    nbrs = neigh.fit(X)
    distances, _ = nbrs.kneighbors(X)
    k_dist = np.sort(distances[:, -1])
    plt.plot(k_dist)
    plt.axhline(y=0.3, color='r', linestyle='--')  # 建议eps取曲线拐点
    plt.title("K-Distance Curve for Eps Selection")
    plt.show()