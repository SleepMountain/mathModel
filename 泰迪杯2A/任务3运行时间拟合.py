import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

file_path = r'D:\桌面\竞赛\泰迪杯2\A\A题-自动化生产线数据分析\附件1\任务3 运行时间.xlsx'
data = pd.read_excel(file_path)


time = data['时间'].values
abnormal_total = data['异常总数'].values


degree = 5
coeffs = np.polyfit(time, abnormal_total, degree)
poly_func = np.poly1d(coeffs)


spline_func = UnivariateSpline(time, abnormal_total, s=1)  # s 是平滑参数，可以根据需要调整

plt.scatter(time, abnormal_total, label='Data')


x_fit_spline = np.linspace(min(time), max(time), 100)
y_fit_spline = spline_func(x_fit_spline)
plt.plot(x_fit_spline, y_fit_spline, color='red', label='Spline Interpolation')


plt.title('Abnormal Total Over Time')
plt.xlabel('Time')
plt.ylabel('Abnormal Total')
plt.legend()
plt.show()


print('多项式回归系数:')
for i, coeff in enumerate(coeffs):
    print(f'a{i} = {coeff:.6f}')


poly_function_str = ' + '.join([f'{coeff:.6f} * x^{i}' for i, coeff in enumerate(coeffs)])
print(f'多项式回归函数: f(x) = {poly_function_str}')