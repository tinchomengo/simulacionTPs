import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
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
            tupla_datos = (self.tiempoSimulacion.value(),self.nroIteraciones.value(),self.horaGuardado.value(),self.llegada.value(),self.pequenos.value(), self.grandes.value(), self.utilitarios.value(), self.unaHoras.value(), self.dosHoras.value(), self.tresHoras.value(),self.tiempoCobro.value())
            simulacion(tupla_datos)
            print("Condiciones correctas")
        else:
            print("Condiciones incorrectas")


    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())    