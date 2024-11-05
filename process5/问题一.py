import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 给定的数据
"""data = np.array([
    13.5377, 11.6923, 11.6501, 12.7950, 13.6715, 14.0347, 13.8884, 14.4384, 12.8978, 12.9699,
    14.8339, 12.5664, 16.0349, 12.8759, 11.7925, 13.7269, 11.8529, 13.3252, 12.7586, 12.8351,
    10.7412, 13.3426, 13.7254, 14.4897, 13.7172, 12.6966, 11.9311, 12.2451, 13.3192, 13.6277,
    13.8622, 16.5784, 12.9369, 14.4090, 14.6302, 13.2939, 12.1905, 14.3703, 13.3129, 14.0933,
    13.3188, 15.7694, 13.7147, 14.4172, 13.4889, 12.2127, 10.0557, 11.2885, 12.1351, 14.1093
])"""


"""data = np.array([
    14.1363, 16.5326, 13.9109, 15.0859, 14.3844, 13.5977, 16.4193, 15.6966, 13.8520, 15.1873,
    15.0774, 14.2303, 15.0326, 13.5084, 15.7481, 13.5776, 15.2916, 15.8351, 15.1049, 14.9175,
    13.7859, 15.3714, 15.5525, 14.2577, 14.8076, 15.4882, 15.1978, 14.7563, 15.7223, 13.0670,
    13.8865, 14.7744, 16.1006, 13.9384, 15.8886, 14.8226, 16.5877, 15.2157, 17.5855, 14.5610,
    14.9932, 16.1174, 16.5442, 17.3505, 14.2352, 14.8039, 14.1955, 13.8342, 14.3331, 13.2053
])"""

"""data = np.array([
    20.8404, 19.3997, 17.8616, 20.1240, 22.9080, 19.7275, 19.6462, 20.0335, 20.0229, 19.0208,
    19.1120, 20.4900, 19.1604, 21.4367, 20.8252, 21.0984, 19.1764, 18.6663, 19.7380, 18.8436,
    20.1001, 20.7394, 21.3546, 18.0391, 21.3790, 19.7221, 18.4229, 21.1275, 18.2498, 19.4664,
    19.4555, 21.7119, 18.9278, 19.8023, 18.9418, 20.7015, 20.5080, 20.3502, 19.7143, 17.9974,
    20.3035, 19.8059, 20.9610, 18.7922, 19.5314, 17.9482, 20.2820, 19.7009, 19.1686, 20.9642
])"""

"""data = np.array([
    10.7494, 12.7447, 10.6988, 11.8836, 10.4862, 11.2877, 9.4434, 11.5510, 10.5771, 12.5106,
    10.8101, 9.8395, 10.3013, 11.4359, 11.7964, 11.0032, 12.9151, 11.2942, 9.9469, 11.1640,
    9.9671, 13.3774, 11.8328, 11.8967, 10.3288, 11.3656, 11.6098, 10.2222, 11.6478, 10.7172,
    10.6767, 12.5261, 10.3054, 11.5047, 12.1867, 14.5267, 10.3521, 9.9351, 10.6824, 12.1522,
    11.7665, 11.1685, 10.5381, 10.5991, 11.7907, 10.8876, 13.6173, 9.2316, 12.7690, 9.8535
])"""

"""data = np.array([
    10.1832, 10.5152, 9.4680, 8.8258, 8.9358, 9.5554, 10.3919, 9.6794, 8.9333, 8.4349,
    8.9702, 10.2614, 11.6821, 9.8078, 11.6035, 9.8441, 8.7493, 10.0125, 10.9337, 9.9155,
    10.9492, 9.0585, 9.1243, 9.7259, 11.2347, 10.2761, 9.0520, 6.9708, 10.3503, 11.6039,
    10.3071, 9.8377, 9.5162, 11.5301, 9.7704, 9.7388, 9.2589, 9.5430, 9.9710, 10.0983,
    10.1352, 9.8539, 9.2880, 9.7510, 8.4938, 10.4434, 9.4922, 11.2424, 10.1825, 10.0414
])"""

"""data = np.array([
    19.2658, 19.7635, 21.0001, 18.3298, 20.3271, 19.0556, 20.9111, 20.2398, 19.9755, 19.9292,
    19.9692, 22.0237, 18.3358, 20.4716, 21.0826, 18.6782, 20.5946, 19.3096, 18.0512, 17.5137,
    20.2323, 17.7416, 19.4100, 18.7872, 21.0061, 20.9248, 20.3502, 19.3484, 21.0205, 20.5812,
    20.4264, 22.2294, 19.7219, 20.0662, 19.3491, 20.0000, 21.2503, 21.1921, 20.8617, 17.8076,
    19.6272, 20.3376, 20.4227, 20.6524, 20.2571, 19.9451, 20.9298, 18.3882, 20.0012, 17.6807
])"""
"""data = np.array([
    18.0799, 17.3088, 18.8979, 17.4954, 16.9851, 18.3999, 17.3709, 17.4393, 16.6019, 19.5763,
    17.0515, 18.4494, 17.8681, 16.7294, 17.5289, 17.0700, 16.7962, 20.1778, 17.7449, 17.5191,
    18.4115, 18.1006, 17.8528, 17.6174, 18.1370, 17.8232, 17.7461, 19.1385, 18.1644, 18.3275,
    18.6770, 18.8261, 19.0078, 18.6487, 17.7081, 15.8679, 16.5714, 15.5031, 18.7477, 18.6647,
    18.8577, 18.5362, 15.8763, 18.8257, 18.3018, 19.1454, 17.9791, 18.4413, 17.7270, 18.0852
])"""

"""data = np.array([
    19.8810, 18.3955, 18.5323, 19.3086, 17.5306, 18.0953, 21.4245, 20.8779, 18.4417, 18.7901,
    19.3232, 19.1034, 18.8751, 18.7661, 19.1922, 18.7117, 19.9594, 19.9407, 18.6886, 17.3011,
    18.2159, 19.5632, 20.4790, 17.9430, 18.1777, 19.3501, 18.6842, 19.7873, 18.4300, 19.6076,
    17.1946, 19.1136, 18.1392, 18.7159, 18.9058, 17.1641, 19.4286, 18.1241, 17.9743, 18.8822,
    20.8586, 18.0953, 19.7847, 18.9133, 19.3362, 20.0360, 17.9640, 19.3199, 18.0913, 19.6992
])"""
# 给定的数据
data = np.array([
    20.8404, 19.3997, 17.8616, 20.1240, 22.9080, 19.7275, 19.6462, 20.0335, 20.0229, 19.0208,
    19.1120, 20.4900, 19.1604, 21.4367, 20.8252, 21.0984, 19.1764, 18.6663, 19.7380, 18.8436,
    20.1001, 20.7394, 21.3546, 18.0391, 21.3790, 19.7221, 18.4229, 21.1275, 18.2498, 19.4664,
    19.4555, 21.7119, 18.9278, 19.8023, 18.9418, 20.7015, 20.5080, 20.3502, 19.7143, 17.9974,
    20.3035, 19.8059, 20.9610, 18.7922, 19.5314, 17.9482, 20.2820, 19.7009, 19.1686, 20.9642
])



# 计算均值、方差和最值
mean = np.mean(data)
variance = np.var(data)
min_value = np.min(data)
max_value = np.max(data)

# 计算概率分布
kde = stats.gaussian_kde(data)

# 打印结果
print("均值:", mean)
print("方差:", variance)
print("最小值:", min_value)
print("最大值:", max_value)

# 绘制概率密度函数图像
x = np.linspace(np.min(data), np.max(data), 100)
y = kde.evaluate(x)

plt.figure()
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('Probability Density Function')
plt.show()
