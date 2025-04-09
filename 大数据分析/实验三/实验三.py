import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

# 内容1：数据生成与基本流程
np.random.seed(42)
N = 20  # 数据点数量
x = np.linspace(0, 2 * np.pi, N).reshape(-1, 1)
y_real = np.sin(x)
y = y_real + np.random.normal(0, 0.1, size=(N, 1))


# 内容2：两种多项式回归实现方式对比
def method_1(x, k):
    """手动构造高阶项"""
    X = np.zeros((len(x), k))
    for j in range(k):
        X[:, j] = np.power(x[:, 0], j + 1)
    return X


def method_2(x, k):
    """使用sklearn的PolynomialFeatures"""
    poly = PolynomialFeatures(degree=k, include_bias=False)
    return poly.fit_transform(x)


# 内容3：观察过拟合现象
plt.figure(figsize=(15, 10))
for i, k in enumerate([1, 3, 5, 7, 9, 15], 1):
    # 使用两种方法构建特征（结果相同）
    X_method1 = method_1(x, k)
    X_method2 = method_2(x, k)

    # 训练模型
    reg = linear_model.LinearRegression()
    reg.fit(X_method1, y)
    y_pre = reg.predict(X_method1)

    # 绘制结果
    plt.subplot(2, 3, i)
    plt.scatter(x, y, c='k', label='Noisy Data')
    plt.plot(x, y_real, 'r', label='True Function')
    plt.plot(x, y_pre, 'b', label=f'Degree {k}')
    plt.ylim(-1.5, 1.5)
    plt.legend()
    plt.title(f'Polynomial Degree = {k}')

plt.tight_layout()
plt.show()

# 内容4：自动选择最佳k值（交叉验证法）
k_candidates = range(1, 10)
scores = []

for k in k_candidates:
    model = make_pipeline(
        PolynomialFeatures(degree=k, include_bias=False),
        linear_model.LinearRegression()
    )
    # 使用5折交叉验证的负均方误差（取绝对值后即为MSE）
    score = -np.mean(cross_val_score(model, x, y,
                                     scoring='neg_mean_squared_error', cv=5))
    scores.append(score)

best_k = k_candidates[np.argmin(scores)]
print(f"最佳多项式阶数: {best_k}")

# 可视化验证结果
plt.figure(figsize=(10, 5))
plt.plot(k_candidates, scores, 'bo-')
plt.xlabel('Polynomial Degree')
plt.ylabel('Cross-Validation MSE')
plt.title('Optimal Polynomial Degree Selection')
plt.axvline(best_k, color='r', linestyle='--')
plt.show()