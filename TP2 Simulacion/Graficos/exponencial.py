import matplotlib.pyplot as plt

def grafico_exponencial(data, dist, cant_intervalos):
    # Graficar histograma
    plt.figure(figsize=(7,4))
    plt.hist(data, bins=cant_intervalos, edgecolor='black')
    plt.title('Histograma Distribucion Exponencial')
    plt.ylabel('Frecuencia Observadas')
    plt.xlabel('Intervalos')

    # Mostrar límites de intervalos y frecuencias
    for i in range(len(dist[0])):
        lower, upper = dist[0][i]
        freq = dist[1][i]
        plt.text((lower + upper) / 2, freq, f"{lower:.4f}\n{upper:.4f}\n({freq})", ha='center', va='bottom')

    plt.show()
