import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QTimer
from datetime import datetime

class MainWindow(QWidget): # 파이썬에서 "상속"을 의미하는 문법; MainWindow 클래스가 자식 클래스, QWidget이 부모 클래스 이다;
    def __init__(self): # self == MainWindow 클래스형 객체; 할당 된 메모리 공간에 객체를 load
        super().__init__()  # 자식클래스형 객체에서 창의 크기, 위치, 배경색 등 수많은 기본 속성들을 초기화 하기 위해서 , 부모 클래스의 생성자 호출을 한다;
                            # __init__() == 특정 클래스형 객체를 생성 할 때 가장 먼저 자동으로 호출어야 하는 생성자;
                            # 자바에서는 부모 클래스의 생성자를 자식 클래스의 생성자 내부에서 호출(super() 또는 super(3))하는 방식이라면,
                            # 파이썬에서는 자식 클래스의 초기화 메소드 내부에서 super().__init__()을 호출하는 방식;
                            # super(): 각 메모리 영역에 공간 할당과 메모리 공간 초기화(load)가 하나의 메소드에서 일어남 -> JAVA ;
                            # super().__init__() : 각 메모리 영역에 공간 할당과 메모리 공간 초기화(load)가 서로 다른 메소드에서 순차적으로 일어남 -> PYTHON;
        self.setWindowTitle("측정 결과 확인 화면")
        self.setGeometry(0, 0, 2030, 1180) 
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout() # QVBoxLayout class 호출, 생성된 객체 주소값을 reference valiable에 대입;
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(15) 
        self.setLayout(main_layout)

        # 최상단 widget 틀 제작
        prime_container_widget = QGroupBox("부품 좌표 측정 시스템")
        prime_container_widget.setStyleSheet("QGroupBox { font-weight: bold; font-size: 25px; border: 1px solid gray; border-radius: 5px; margin-top: 15px; } " \
        "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; }")
        control_layout = QHBoxLayout() 
        prime_container_widget.setLayout(control_layout) # 주소값을 인자로 전달 해줌으로써 widget내의 정렬방식을 설정;

        # 현재 시간 widget 생성
        self.time_widget = QLabel() # QTimer 이벤트에 의해 값이 계속 업데이트되어야 함;
        self.time_widget.setAlignment(Qt.AlignCenter)
        self.time_widget.setStyleSheet("font-size: 20px;") 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Min Conf 입력 widget 생성
        minConf_layout = QHBoxLayout()
        minConf_widget = QLabel("Min Conf.")
        minConf_widget.setStyleSheet("font-size: 17px;") 
        minConf_layout.addWidget(minConf_widget) # addWidget() 는 layout 클래스에 정의 된 method;
        self.minConfEdit_widget = QLineEdit() # 나중에 "측정 시작" 버튼 클릭 시 사용자가 입력한 값을 읽어와야 함;
        self.minConfEdit_widget.setFixedSize(50, 25)
        self.minConfEdit_widget.setStyleSheet("font-size: 12px;")
        minConf_layout.addWidget(self.minConfEdit_widget)

        # trigInterval 간격 입력 widget 생성
        trigInterval_layout = QHBoxLayout()
        trigInterval_widget = QLabel("trigInterval 간격")
        trigInterval_widget.setStyleSheet("font-size: 17px;") 
        trigInterval_layout.addWidget(trigInterval_widget)
        self.trigInterval_edit_widget = QLineEdit()
        self.trigInterval_edit_widget.setFixedSize(50, 25)
        self.trigInterval_edit_widget.setStyleSheet("font-size: 12px;") # QLineEdit 글꼴 크기 변경;
        trigInterval_layout.addWidget(self.trigInterval_edit_widget)
        ms_widget = QLabel("ms")
        ms_widget.setStyleSheet("font-size: 17px;") 
        trigInterval_layout.addWidget(ms_widget)

        # 측정 시작 버튼 widget 생성
        startButton_widget = QPushButton("측정 시작")
        startButton_widget.setFixedSize(150, 50) 
        startButton_widget.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; background-color: #4CAF50; color: white; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")

        # 지금까지 생성 된 모든 widget을 최상단 layout에 추가
        control_layout.addStretch(0)
        control_layout.addWidget(self.time_widget)
        control_layout.addStretch(3)
        control_layout.addLayout(minConf_layout)
        control_layout.addStretch(3)
        control_layout.addLayout(trigInterval_layout)
        control_layout.addStretch(1)
        control_layout.addWidget(startButton_widget)
        control_layout.addStretch(0)

        main_layout.addWidget(prime_container_widget)

        # 카메라 이미지 그룹
        camera_group_box = QGroupBox() # total camera widget(container);
        camera_group_box.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; }")
        camera_layout = QHBoxLayout()
        camera_group_box.setLayout(camera_layout)
        
        # 왼쪽 카메라 이미지 프레임
        left_camera_frame = QFrame() # left camera widget(component);
        left_camera_frame.setFrameShape(QFrame.StyledPanel)
        left_camera_frame.setStyleSheet("background-color: #e0e0e0; border: 1px solid gray;")
        left_camera_layout = QVBoxLayout()
        left_camera_frame.setLayout(left_camera_layout)
        left_camera_label = QLabel("LEFT CAMERA IMAGE", alignment=Qt.AlignCenter)
        left_camera_label.setStyleSheet("font-size: 16px;")
        left_camera_layout.addWidget(left_camera_label)
        
        # 오른쪽 카메라 이미지 프레임
        right_camera_frame = QFrame()
        right_camera_frame.setFrameShape(QFrame.StyledPanel)
        right_camera_frame.setStyleSheet("background-color: #e0e0e0; border: 1px solid gray;")
        right_camera_layout = QVBoxLayout()
        right_camera_frame.setLayout(right_camera_layout)
        right_camera_label = QLabel("RIGHT CAMERA IMAGE", alignment=Qt.AlignCenter)
        right_camera_label.setStyleSheet("font-size: 16px;")
        right_camera_layout.addWidget(right_camera_label)

        # left , right camera widget을 container widget에 삽입
        camera_layout.addWidget(left_camera_frame)
        camera_layout.addWidget(right_camera_frame)
        main_layout.addWidget(camera_group_box, 1) # 2개의 widget 사이 공간 설정;

        # 측정 결과 테이블
        # 측정 결과가 나올 때마다 data update가 필요
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels(["측정 일시", "부품명", "Conf.", "X", "Y", "Z", "R", "소요시간(ms)"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 테이블 전체 글꼴 크기 변경
        self.result_table.setStyleSheet("QTableWidget { font-size: 16px; gridline-color: #d0d0d0; }")

        # 더미 데이터 추가
        self.result_table.setRowCount(5)
        for row in range(5):
            self.result_table.setItem(row, 0, QTableWidgetItem())
            self.result_table.setItem(row, 1, QTableWidgetItem())
            self.result_table.setItem(row, 2, QTableWidgetItem())
            self.result_table.setItem(row, 3, QTableWidgetItem())
            self.result_table.setItem(row, 4, QTableWidgetItem())
            self.result_table.setItem(row, 5, QTableWidgetItem())
            self.result_table.setItem(row, 6, QTableWidgetItem())
            self.result_table.setItem(row, 7, QTableWidgetItem())
        # table widget을 self
        main_layout.addWidget(self.result_table)

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_widget.setText(f"현재시간\n{current_time}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow() # 클래스 호출시 파이썬은 MainWindow 클래스는 인스턴스화를 진행을 위해 heap 영역 및 stack 영역에 메모리 할당을 한다;
                          # 메소드나 클래스 변수(다른 언어의 'static'과 유사한 개념)가 모두 객체로 취급되어 힙(heap) 영역에 로드된다. == method area를 미사용 한다;
                          # 파이썬에서도 자바의 new 키워드처럼 힙(heap) 메모리에 객체를 로드하는 객체화 과정이 일어난다. 
                          # 단, 자바처럼 "new"라는 키워드를 명시적으로 사용하지 않고 내부적으로 숨겨져 있는 __new__()를 사용한다;
                          # "MainWindow()"와 같이 클래스 이름을 메소드 함수처럼 호출하는 하면, 내부적으로 1. "__new__()"라는 명시되지 않은 내부 메소드가 호출된다. 그 후 초기화를 위한 메모리 공간 할당이 일어난다.
                          # 2. heap, stack 영역에 memory 공간 할당 후 명시 된 def __init__(self) 구간을 자동으로 찾아내서 실행한다;
                          # Python은 생성자 호출을 사용하는 Java 처럼 Constructor Ovaerloading이 있을 수 없다. class 이름 호출 방식을 사용하는 Python의 입장에서는 하나의 "__init__"
                          # 메소드를 이용해서 여러개의 객체 생성을 해야 한다. __init__ 메소드 수정 방식을 사용해야 하며, 하나의 클래스에 하나의 __init__ 메소드만 존재 가능하다.
    window.show()
    sys.exit(app.exec())

    # 특정 객체에 해당하는 값이 들어가지는 위젯이 필요한 경우, self.을 붙여 인스턴스 속성으로 관리하는 것;
    # JAVA에서의 Instance 변수를 PYHON에서 표현 할 때, self.valiable name으로 정의한다;
    # 대신에 동일한 클래스에서 사용할 때 self.valiable name 으로 정의한다. JAVA에서의 this.valiable name 과 100000% 동일하다.
    # 만약 외부 클래스에서 instance valiable에 접근하고 싶을 경우 JAVA와 동일하게 reference.valiable name 형식으로 사용한다.
    # ex) Cat c = new Cat(3), Cat b = new Cat(4), public Cat(int tall) -> c.tall, b.tall == JAVA