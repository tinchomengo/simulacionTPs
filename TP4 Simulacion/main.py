import sys
import excel
from PyQt6.QtWidgets import *
from PyQt6.uic import *
from simulacion import simulacion
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('./TP4.ui', self)
        self.show()
        self.ejecutar.clicked.connect(self.simularPlaya)

    

    def simularPlaya(self):
        print("Simulando ejercicio")

        condicional1 = self.pequenos.value() +self.grandes.value()+self.utilitarios.value() == 100
        condicional2 = self.unaHoras.value() +self.dosHoras.value()+self.tresHoras.value() <= 100
        if(condicional1 and condicional2):
            tupla_datos = (self.tiempoSimulacion.value(),self.nroIteraciones.value(),self.horaGuardado.value(),self.llegada.value(),((self.pequenos.value(),"Pequeños"), (self.grandes.value(),"Grandes"), (self.utilitarios.value(),"Utilarios")), ((self.unaHoras.value(),60), (self.dosHoras.value(),120), (self.tresHoras.value(),180),((100-self.tresHoras.value()+self.unaHoras.value()+self.dosHoras.value()),240)),self.tiempoCobro.value())
            datos=simulacion(tupla_datos)
            print("\n")
            print("Condiciones correctas")
            print("Iteraciones simuladas: ",datos[0])
            print("\n")
            print("Todos los coches: ",datos[2])
            print("Contadores guardados:",datos[1])
            excel.mostrar_excel(datos[0],datos[2])
        else:
            print("Condiciones incorrectas")


    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())    