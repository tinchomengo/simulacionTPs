import matplotlib.pyplot as plt
import numpy as np
n1 = [
    0.4975, 0.4273, 0.0834, 0.0582, -0.1656, 0.8311, 0.7507, 0.2226, 0.8990, 0.3273,
    0.4980, 0.4976, 1.0258, 0.4172, 0.6951, 0.0087, 0.5550, 0.4522, 0.4590, 0.4912,
    0.3574, 0.5264, 1.0106, 0.4850, 0.6221, 0.3373, 0.5037, 0.5351, 0.5091, 0.5874,
    0.3732, 0.9715, 0.3730, 0.2491, 0.2513, 0.3106, 0.5768, 0.2915, 0.4114, -0.1216,
    0.8670, 0.6220, 0.6179, 0.3439, 0.0433, 0.3564, 0.2460, 0.3710, 0.5154, 0.4303,
    0.1732, 0.2159, 0.4271, 0.4877, 0.3279, 0.3914, 0.5229, 0.3091, 0.4095, 0.0758,
    0.5085, 0.4267, 0.4640, 0.6480, 0.6313, 0.0714, -0.4518, 0.2514, 0.0987, 0.5943,
    0.0560, 0.5009, 0.6267, 0.4210, 0.6251, 0.2493, 0.4693, 0.9025, 0.2702, 1.0351,
    0.4598, 0.5570, 0.6567, 0.5674, 0.2940, 0.1242, 0.3576, 0.2370, 0.2455, 0.4760,
    0.4631, 0.8600, 0.7391, 0.4521, -0.2763, 0.4678, -0.0478, 0.5435, 0.4651, 0.4736
]

n2 = [
    0.8397, 0.3657, 0.3403, 0.8037, 0.8440, 0.6343, -0.0066, 0.0605, 0.5315, 0.5130,
    0.8979, 0.4378, 0.6432, 0.7268, 0.6830, 0.4895, 0.7841, 0.7239, 0.1575, 0.8122,
    0.7478, 0.2740, 0.8205, 0.6315, 0.6659, -0.0633, 0.4603, 0.9654, 0.2695, 0.4214,
    0.3932, 0.4423, 0.6313, 0.4026, 0.2435, 0.3172, 0.8236, 0.4738, 0.8912, 0.5759,
    0.2621, 0.0997, 0.5930, 0.7242, 0.2799, 0.4825, 0.2630, 0.6300, 0.4347, 0.8267,
    0.3231, 0.6219, 0.8264, 0.4482, 0.5020, 1.0734, 0.5208, 0.6461, 0.7253, 0.6936,
    0.7837, 0.7856, 0.7888, 0.6552, 0.2226, 0.6017, 0.5535, 0.1781, -0.1239, 0.3447,
    0.1632, 0.7307, 0.7248, 0.4847, 0.6960, 0.2783, 0.4907, 0.6308, 0.7748, 0.2918,
    0.7424, 0.7805, 0.4923, 0.7414, 0.8632, 0.2543, 1.2551, 0.5246, 0.8008, 0.1179,
    0.2255, 0.6116, 0.0256, 0.1258, 0.5753, 0.0955, 0.5616, 0.1598, 0.7046, 0.3092
]

intervalos=15

# Genera datos con distribución normal
media1 = np.mean(n1)
desviacion_estandar1 = np.std(n1)
datos1 = np.random.normal(media1, desviacion_estandar1, 1000)

media2 = np.mean(n2)
desviacion_estandar2 = np.std(n2)
datos2 = np.random.normal(media2, desviacion_estandar2, 1000)

# Histograma
plt.hist(datos1, bins=intervalos, alpha=0.5, label='n1')
plt.hist(datos2, bins=intervalos, alpha=0.5, label='n2')
plt.title('Histograma Distribución Normal')
plt.xlabel('Valores')
plt.ylabel('Frecuencia')
plt.legend()
plt.show()