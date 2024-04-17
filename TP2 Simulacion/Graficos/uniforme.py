import matplotlib.pyplot as plt
import numpy as np

def histograma_uniforme(data, dist, cant_intervalos):
    # Plot histogram
    plt.figure(figsize=(7,4))
    plt.hist(data, bins=cant_intervalos, edgecolor='black')
    plt.title('Histograma Distribucion Uniforme')
    plt.ylabel('Frecuencia Observadas')
    plt.xlabel('Intervalos')

    # Show interval limits and frequencies
    for i in range(len(dist[0])):
        lower, upper = dist[0][i]
        freq = dist[1][i]
        plt.text((lower + upper) / 2, freq, f"{lower:.4f}\n{upper:.4f}\n({freq})", ha='center', va='bottom')

    plt.show()
