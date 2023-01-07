import sys
from PyQt5.QtWidgets import QApplication
from window import Window

def main():
    app = QApplication(sys.argv)

    # Create an instance of the Window class
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
