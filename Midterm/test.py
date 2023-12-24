import datetime
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class RelojDigital(QWidget):
    def __init__(self):
        super().__init__()

        # Crear label encargado de mostrar la hora
        self.label_timer = QLabel()
        self.label_timer.setFont(QFont("Times", 50))

        # Crear layout vertical para nuestro label
        layout = QVBoxLayout()
        layout.addWidget(self.label_timer)
        self.setLayout(layout)

        # Crear nuestro QTimer encargado de actualizar el tiempo cada 1 segundo
        timer = QTimer(self)
        timer.timeout.connect(self.mostrar_hora)
        timer.setInterval(1000)
        timer.start()

        # Definir título y tamaño ventana
        self.setWindowTitle("Reloj Digital con QTimer")
        self.setGeometry(100, 100, 250, 100)

        # Ejecutar el método para mostrar hora por primera vez
        self.mostrar_hora()

        # Mostrar ventana
        self.show()

    def mostrar_hora(self):
        # Obtener hora actual
        hora_actual = datetime.datetime.now().time()
        # Actualizar texto del label
        self.label_timer.setText(hora_actual.strftime("%H:%M:%S %p"))


if __name__ == '__main__':
    app = QApplication([])
    form = RelojDigital()
    sys.exit(app.exec())
