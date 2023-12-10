import sys
import cv2 as cv
import os
from time import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from login import loging_in
import subprocess
import win32gui
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from pictures import pictuter, pictuter4, pictuter8
import buttons
#from main import run


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Chrome")
        self.resize(300, 150)
        self.center()
        self.Flag2 = True
        
        # Create the main widget and set a QVBoxLayout
        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        # Create a scrollable area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a widget to contain the label and add it to the scrollable area
        content_widget = QWidget(scroll_area)
        scroll_area.setWidget(content_widget)

        # Set a QVBoxLayout for the content widget
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Align to the top and center

        # Create the description label
        desc_label = QLabel('DONT FORGET TO READ\n"PLEASE_READ_ME.docx"')
        desc_label.setFont(QFont("Arial", 14))  # Set the font size and type
        desc_label.setStyleSheet("color: red;")

        # Add the description label to the content layout
        content_layout.addWidget(desc_label)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)

        self.login_button = QPushButton("Loging in", self)
        self.login_button.clicked.connect(self.show_login_window)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        layout.addWidget(self.login_button)
        layout.addWidget(self.quit_button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.login = ""
        self.password = ""
        self.key1 = ""
        self.key2 = ""

        stylesheet = """
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 white, stop:1 #FFC0CB);
            }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 white, stop:1 #ADD8E6);
                color: black;
            }
        """
        self.setStyleSheet(stylesheet)

    def closeEvent(self, event):
        quit_box = QMessageBox.question(
            self, "Quit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No
        )
        if quit_box == QMessageBox.Yes:
            self.Flag2 = False
            event.accept()
        else:
            event.ignore()

    def show_login_window(self):
        self.login_button.hide()
        self.quit_button.hide()

        login_widget = QWidget(self)
        login_layout = QVBoxLayout(login_widget)
        login_layout.addSpacing(10)  # Add spacing between the elements

        self.login_label = QLabel("Login:", self)
        login_input = QLineEdit(self)
        self.password_label = QLabel("Password:", self)
        password_input = QLineEdit(self)
        password_input.setEchoMode(QLineEdit.Password)
        self.key1_label = QLabel("Personal key:", self)
        key1_input = QLineEdit(self)        
        self.key2_label = QLabel("Repeat personal key:", self)
        key2_input = QLineEdit(self)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_action)

        login_layout.addWidget(self.login_label)
        login_layout.addWidget(login_input)
        login_layout.addWidget(self.password_label)
        login_layout.addWidget(password_input)
        login_layout.addWidget(self.key1_label)
        login_layout.addWidget(key1_input)
        login_layout.addWidget(self.key2_label)
        login_layout.addWidget(key2_input)
        login_layout.addWidget(self.login_button)

        # Create the result label and add it to the layout
        self.result_label = QLabel(self)
        login_layout.addWidget(self.result_label)

        # Add spacer item for vertical spacing
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        login_layout.addItem(spacer_item)

        login_widget.setLayout(login_layout)
        self.setCentralWidget(login_widget)

        # Save references to login and password inputs
        
        self.login_input = login_input
        self.password_input = password_input
        self.key1_input = key1_input
        self.key2_input = key2_input

    def login_action(self):
        self.login = self.login_input.text()
        self.password = self.password_input.text()
        self.key1 = self.key1_input.text()
        self.key2 = self.key2_input.text()
        self.id = ''.join(subprocess.check_output('wmic diskdrive get model, SerialNumber').decode().split())
        global lf
        out, lf = loging_in(self.login, self.password, self.id, self.key1, self.key2)

        if lf:
            self.login_label.hide()
            self.login_input.hide()
            self.password_label.hide()
            self.password_input.hide()
            self.key1_label.hide()
            self.key1_input.hide()
            self.key2_label.hide()
            self.key2_input.hide()
            self.login_button.hide()
            self.result_label.setText(out + '\nChoose FS/PRP window and assign\nvalues for F-keys (if needed):\n')
            self.result_label.setStyleSheet("color: green;")
            self.show_continue_button()
        else:
            self.result_label.setText(out)
            self.result_label.setStyleSheet("color: red;")
            self.show_quit_button()

    def show_continue_button(self):
        self.run_button = QPushButton("Run cheat", self)
        self.run_button.clicked.connect(self.continue_action)  # Updated connection to continue_action

        self.stop_button = QPushButton("Stop cheat", self)
        self.stop_button.clicked.connect(self.stop_action)

        self.comboBox = QComboBox(self)
        self.comboBox_pic = QComboBox(self)

        # Get the names of open windows
        open_windows = []
        win32gui.EnumWindows(lambda hwnd, window_list: window_list.append(win32gui.GetWindowText(hwnd)), open_windows)
        open_windows = [window for window in open_windows if window]  # Remove empty window names
        self.comboBox.addItems(open_windows)

        choose_pic = ['4', '8', '8 + reverse']
        self.comboBox_pic.addItems(choose_pic)
        self.comboBox_pic_label = QLabel("Choose mode:", self)

        login_layout = self.centralWidget().layout()
        login_layout.addWidget(self.run_button)
        login_layout.addWidget(self.stop_button)
        login_layout.addWidget(self.comboBox)
        login_layout.addWidget(self.comboBox_pic_label)
        login_layout.addWidget(self.comboBox_pic)

        # Add labels and line edits
        self.labels = []
        self.line_edits = []
        for i in range(1, 6):
            label = QLabel(f"F{i}:")
            line_edit = QLineEdit(self)
            line_edit.setValidator(QIntValidator())  # Restrict input to integers
            login_layout.addWidget(label)
            login_layout.addWidget(line_edit)
            self.labels.append(label)
            self.line_edits.append(line_edit)

    def show_quit_button(self):
        # Check if the "Quit" button already exists
        if not hasattr(self, "quit_button"):
            self.quit_button = QPushButton("Quit", self)
            self.quit_button.clicked.connect(self.close)

            login_layout = self.centralWidget().layout()
            login_layout.addWidget(self.quit_button)

    def continue_action(self):
        selected_window = self.comboBox.currentText()
        wincap = WindowCapture(selected_window)
        try:
            self.Flag2 = True
            show = 'Running...'
            self.show_result_label(show)

            # Read the values from line edits and validate them
            values = []
            for line_edit in self.line_edits:
                value = line_edit.text()
                if not value:
                    value = 0
                else:
                    try:
                        value = int(value)
                        if value < 0:
                            raise ValueError
                    except ValueError:
                        value = -1
                        line_edit.setText("Invalid input. Enter >= 0, reenter and rerun.")
                        line_edit.setStyleSheet("color: red;")
                values.append(int(value))

            # Access the values as f1, f2, f3, f4, f5 variables
            #print(values)
            f1, f2, f3, f4, f5 = values
            

            def run(wincap, flag=False, flag2=False, f1=0, f2=0, f3=0, f4=0, f5=0, loop_time=time(), pic_flag='4'):
                if pic_flag == '4':
                    pictures = pictuter4
                    acc = 0.6
                elif pic_flag == '8':
                    pictures = pictuter8
                    acc = 0.7
                else:
                    pictures = pictuter
                    acc = 0.8
                hsv_filter = HsvFilter(116, 129, 0, 179, 255, 255, 0, 0, 255, 0)
                vision_limestone = Vision(pictures)
                start_time = loop_time
                current_time = start_time
                counter_f1, counter_f2, counter_f3, counter_f4, counter_f5 = 0, 0, 0, 0, 0
                while flag and flag2:
                    screenshot, screenshot_s = wincap.get_screenshot()
                    processed_image = vision_limestone.apply_hsv_filter(screenshot, hsv_filter)
                    rectangles = vision_limestone.find(processed_image, acc)
                    output_image = vision_limestone.draw_rectangles(processed_image, rectangles)

                    #cv.imshow('Captured', screenshot)
                    #cv.imshow('Matches', output_image)

                    #cv.imshow('Captured1', screenshot_s)

                    #print('FPS {}'.format(1 / (time() - loop_time)))
                    # loop_time = time()
                    elapsed_time = time() - current_time
                    #print(elapsed_time, current_time)
                    #print(f1 * counter_f1)
                    #print(f2 * counter_f2)
                    #print(f3 * counter_f3)
                    #print(f4 * counter_f4)
                    #print(f5 * counter_f5)

                    if elapsed_time >= f1 * counter_f1 and f1 != 0 and f1 != -1:
                        buttons.press_f1()
                        #print('f1')
                        counter_f1 += 1

                    if elapsed_time >= f2 * counter_f2 and f2 != 0 and f2 != -1:
                        buttons.press_f2()
                        #print('f2')
                        counter_f2 += 1

                    if elapsed_time >= f3 * counter_f3 and f3 != 0 and f3 != -1:
                        buttons.press_f3()
                        #print('f3')
                        counter_f3 += 1

                    if elapsed_time >= f4 * counter_f4 and f4 != 0 and f4 != -1:
                        buttons.press_f4()
                        #print('f4')
                        counter_f4 += 1

                    if elapsed_time >= f5 * counter_f5 and f5 != 0 and f5 != -1:
                        buttons.press_f5()
                        #print('f5')
                        counter_f5 += 1

                    flag2 = self.Flag2

                    if cv.waitKey(1) == ord('q'):
                        cv.destroyAllWindows()
                        flag = False
                        return 0
            
            pic_flag = self.comboBox_pic.currentText()
            run(wincap, lf, self.Flag2, f1, f2, f3, f4, f5, time(), pic_flag)
        except:
            #run(wincap, lf, self.Flag2, f1, f2, f3, f4, f5)
            show = 'ERROR. CHOOSE FS WINDOW.'
            self.show_result_label(show)

    def show_result_label(self, text):
        self.result_label.setText(text)

    def stop_action(self):
        self.Flag2 = False
        show = "Pause..."
        self.show_result_label(show)

    def center(self):
        frame_geometry = self.frameGeometry()
        desktop_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(desktop_center)
        self.move(frame_geometry.topLeft())


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
