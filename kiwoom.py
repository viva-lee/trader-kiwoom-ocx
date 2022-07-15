from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom() class start.")
        
        # 초기 세팅 함수들 바로 실행
        self.get_ocx_instance()
        self.event_slots()
        self.signal_login_commConnect()
        
        self.login_event_loop = QEventLoop() # 로그인 요청용 이벤트 루프
        
    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot) # 로그인 관련 이벤트
        
    def login_slot(self, err_code):
        print(errors(err_code)[1])
        
        self.login_event_loop.exit()