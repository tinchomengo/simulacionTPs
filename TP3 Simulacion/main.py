import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PyQt6.uic import loadUi
from simulacion import simulacion
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('./interfazSimuladorAutos.ui', self)
        self.show()
        self.pushButton.clicked.connect(self.simularAutos)

    

    def simularAutos(self):
        print("Simulando autos")
        condicional1 = self.auto0.value() +self.auto1.value()+self.auto2.value()+self.auto3.value()+self.auto4.value() == 100
        condicional2 = self.compacto.value() +self.mediano.value()+self.lujo.value() == 100
        condicional3 = self.comision1.value() +self.comision2.value() == 100
        condicional4 = (self.tarifa1.value()) +self.tarifa2.value()+self.tarifa3.value() == 100
        condicional5 = (self.valor_i.value() + self.valor_j.value()) <= self.semanas.value()
        if(condicional1 and condicional2 and condicional3 and condicional4 and condicional5):
            print("Condiciones correctas")
            # Estructura tupla ((probAutos), (probCategoria), (probComision), (probTarifa), probSorteo, (valor_i, valor_j), semanas)
            tupla_probs = (((self.auto0.value(),0), (self.auto1.value(),1), (self.auto2.value(),2), (self.auto3.value(),3), (self.auto4.value(),4)), ((self.compacto.value(),"compacto"), (self.mediano.value(),"mediano"), (self.lujo.value(),"de lujo")), ((self.comision1.value(),400), (self.comision2.value(),500)), ((self.tarifa1.value(),1000), (self.tarifa2.value(),1500), (self.tarifa3.value(),2000)), ((self.probGanar.value(),"Gana el sorteo"),(100-self.probGanar.value(),"No gana el sorteo")), ((self.valor_i.value(), self.valor_j.value())), self.semanas.value())
            simulacion(tupla_probs)
        else:
            print("Condiciones incorrectas")


    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())    