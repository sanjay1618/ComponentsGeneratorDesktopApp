import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from views.left_panel import LeftPanel
from views.right_panel import RightPanel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Components Generator')
        self.setGeometry(100, 100, 1100, 700)

        main_layout = QHBoxLayout()

        # Initialize panels clearly
        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.right_panel, 3)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
