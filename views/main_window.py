from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout
)
from left_panel import LeftPanel
from right_panel import RightPanel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HTML + CSS Page Generator')
        self.setGeometry(100, 100, 1000, 600)

        main_layout = QHBoxLayout()

        self.left_panel = LeftPanel(self)
        main_layout.addWidget(self.left_panel, 1)

        self.right_panel = RightPanel(self)
        main_layout.addWidget(self.right_panel, 3)

        self.setLayout(main_layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
