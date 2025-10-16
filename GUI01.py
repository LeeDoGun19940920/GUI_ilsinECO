import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QPixmap
from datetime import datetime

class MainWindow(QWidget): 
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("측정 결과 확인 화면")
        self.setGeometry(0, 0, 2030, 1180) 
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        #main_layout.setSpacing()
        self.setLayout(main_layout)

        prime_container_widget = QGroupBox("부품 좌표 측정 시스템")
        prime_container_widget.setStyleSheet("QGroupBox { font-weight: bold; font-size: 30px; border: 1px solid gray; border-radius: 5px; margin-top: 15px; } " \
        "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; }")
        control_layout = QHBoxLayout() 
        prime_container_widget.setLayout(control_layout)

        self.time_widget = QLabel()
        self.time_widget.setAlignment(Qt.AlignCenter)
        self.time_widget.setStyleSheet("font-size: 20px;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        minConf_layout = QHBoxLayout()
        minConf_widget = QLabel("Min Conf.")
        minConf_widget.setStyleSheet("font-size: 20px;") 
        minConf_layout.addWidget(minConf_widget) 
        self.minConfEdit_widget = QLineEdit() 
        self.minConfEdit_widget.setFixedSize(50, 25)
        self.minConfEdit_widget.setStyleSheet("font-size: 12px;")
        minConf_layout.addWidget(self.minConfEdit_widget)

        trigInterval_layout = QHBoxLayout()
        trigInterval_widget = QLabel("trigInterval 간격")
        trigInterval_widget.setStyleSheet("font-size: 20px;") 
        trigInterval_layout.addWidget(trigInterval_widget)
        self.trigInterval_edit_widget = QLineEdit()
        self.trigInterval_edit_widget.setFixedSize(50, 25)
        self.trigInterval_edit_widget.setStyleSheet("font-size: 12px;")
        trigInterval_layout.addWidget(self.trigInterval_edit_widget)
        ms_widget = QLabel("ms")
        ms_widget.setStyleSheet("font-size: 20px;") 
        trigInterval_layout.addWidget(ms_widget)

        startButton_widget = QPushButton("측정 시작")
        startButton_widget.setFixedSize(150, 50) 
        startButton_widget.setStyleSheet("QPushButton { font-weight: bold; font-size: 20px; background-color: #4CAF50; color: white; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")

        # 4개의 위젯을 최상단 컨테이너 위젯에 추가
        control_layout.addStretch(0)
        control_layout.addWidget(self.time_widget)
        control_layout.addStretch(1)
        control_layout.addLayout(minConf_layout)
        control_layout.addStretch(4)
        control_layout.addLayout(trigInterval_layout)
        control_layout.addStretch(1)
        control_layout.addWidget(startButton_widget)
        control_layout.addStretch(0)

        main_layout.addWidget(prime_container_widget)

        camera_group_box = QGroupBox()
        camera_group_box.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; }")
        camera_layout = QHBoxLayout()
        camera_group_box.setLayout(camera_layout)

        left_camera_frame = QFrame()
        left_camera_frame.setFrameShape(QFrame.StyledPanel)
        left_camera_frame.setStyleSheet("background-color: #e0e0e0; border: 1px solid gray;")
        left_camera_layout = QVBoxLayout()
        left_camera_frame.setLayout(left_camera_layout)
        left_camera_layout.setSpacing(0)
        left_camera_label = QLabel("LEFT CAMERA IMAGE", alignment = Qt.AlignHCenter)
        left_camera_label.setStyleSheet("font-size: 25px;")
        left_camera_layout.addWidget(left_camera_label)
        left_camera_layout.setContentsMargins(0, 0, 0, 0)

        self.left_image_display = QLabel("No Image Loaded", alignment=Qt.AlignCenter)
        self.left_image_display.setStyleSheet("font-size: 25px; color: #bdc3c7;")
        left_camera_layout.addWidget(self.left_image_display, 1)

        self.left_image_display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding 
        )
        self.left_image_display.setMinimumSize(1, 1)

        right_camera_frame = QFrame()
        right_camera_frame.setFrameShape(QFrame.StyledPanel)
        right_camera_frame.setStyleSheet("background-color: #e0e0e0; border: 1px solid gray;")
        right_camera_layout = QVBoxLayout()
        right_camera_frame.setLayout(right_camera_layout)
        right_camera_layout.setSpacing(0)
        right_camera_label = QLabel("RIGHT CAMERA IMAGE", alignment = Qt.AlignHCenter)
        right_camera_label.setStyleSheet("font-size: 25px;")
        right_camera_layout.addWidget(right_camera_label)
        right_camera_layout.setContentsMargins(0, 0, 0, 0)

        self.right_image_display = QLabel("No Image Loaded", alignment=Qt.AlignCenter)
        self.right_image_display.setStyleSheet("font-size: 25px; color: #bdc3c7;")
        right_camera_layout.addWidget(self.right_image_display, 1)

        self.right_image_display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.right_image_display.setMinimumSize(1, 1)

        camera_layout.addWidget(left_camera_frame)
        camera_layout.addWidget(right_camera_frame)
        main_layout.addWidget(camera_group_box, 2) 
        
         # 이미지 불러오기 위한 밑작업
        self.imgFolder_path = r"C:\Users\USINGTECH\Desktop\imgs\V_BODY1_L"
        self.L_imgFile_path = r"C:\Users\USINGTECH\Desktop\imgs\V_BODY1_L\V_BODY1_L_1.JPEG"
        self.R_imgFile_path = r"C:\Users\USINGTECH\Desktop\imgs\V_BODY1_R\V_BODY1_R_1.JPEG"
        self.L_saveFolder_path = r"C:\Users\USINGTECH\Desktop\imgs\V_BODY1_L\newImg"
        self.R_saveFolder_path = r"C:\Users\USINGTECH\Desktop\imgs\V_BODY1_R\newImg"

        self.left_pixmap = QPixmap() # Load 된 Img 저장 할 객체 생성
        self.right_pixmap = QPixmap()

        startButton_widget.clicked.connect(self.button_push)

        self.result_table = QTableWidget()
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels(["측정 일시", "부품명", "Conf.", "X", "Y", "Z", "R", "소요시간(ms)"])
        self.result_table.setStyleSheet(
            "QTableWidget { font-size: 15px; gridline-color: #d0d0d0; } "
            "QHeaderView::section { font-size: 20px; }"
        )

        self.result_table.setRowCount(6)
        for row in range(0): # 데이터가 들어 갈 때 각 행 마다 데이터 값이 표시된다
            self.result_table.setItem(row, 0, QTableWidgetItem())
            self.result_table.setItem(row, 1, QTableWidgetItem())
            self.result_table.setItem(row, 2, QTableWidgetItem())
            self.result_table.setItem(row, 3, QTableWidgetItem())
            self.result_table.setItem(row, 4, QTableWidgetItem())
            self.result_table.setItem(row, 5, QTableWidgetItem())
            self.result_table.setItem(row, 6, QTableWidgetItem())
            self.result_table.setItem(row, 7, QTableWidgetItem())
        
        row_height = 50
        for row in range(self.result_table.rowCount()):
            self.result_table.setRowHeight(row, row_height)

        main_layout.addWidget(self.result_table, 1)

    def update_time(self) :
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        self.time_widget.setText(f"현재시간\n{current_time}")

    # 이미지 출력 후 새폴더에 저장 
    def button_push(self) :
        print("Img Display")

        self.left_pixmap = self.load_img(self.L_imgFile_path, self.left_image_display)
        self.right_pixmap = self.load_img(self.R_imgFile_path, self.right_image_display)
        
        self.resizeEvent(None)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not self.left_pixmap.isNull():
            save_path_L = os.path.join(self.L_saveFolder_path, f"L_img_{timestamp}.JPEG") # 새로운 폴더에 이미지 저장 후 주소값 대입
            if self.left_pixmap.save(save_path_L, "JPEG"):
                print(f"왼쪽 이미지 저장 성공: {save_path_L}")
            else:
                print(f"왼쪽 이미지 저장 실패: {save_path_L}")
        
        if not self.right_pixmap.isNull():
            save_path_R = os.path.join(self.R_saveFolder_path, f"R_img_{timestamp}.JPEG")
            if self.right_pixmap.save(save_path_R, "JPEG"):
                print(f"오른쪽 이미지 저장 성공: {save_path_R}")
            else:
                print(f"오른쪽 이미지 저장 실패: {save_path_R}")
    
    # 이미지 출력시 Resize
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        if not self.left_pixmap.isNull():
            self.left_image_display.setPixmap(self.left_pixmap.scaled(
                self.left_image_display.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

        if not self.right_pixmap.isNull():
            self.right_image_display.setPixmap(self.right_pixmap.scaled(
                self.right_image_display.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    # 이미지 출력 실패시 
    def load_img(self, file_path, label):
        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            label.setText(f"ERROR: Image not found\n({os.path.basename(file_path)})")
            label.setPixmap(QPixmap()) 
            return QPixmap()

        label.setText("") 

        return pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())