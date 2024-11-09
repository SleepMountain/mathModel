import numpy as np
import matplotlib.pyplot as plt

coeffs = [0, 0, -0.000006, 0.082150, 453.912015]

poly_func = np.poly1d(coeffs)

x = np.linspace(0, 28799, 1000)  # 生成1000个点，以获得更平滑的曲线

y = poly_func(x)

plt.figure(figsize=(12, 6))
plt.plot(x, y, label='Polynomial Function')
plt.title('Plot of the Polynomial Function')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()