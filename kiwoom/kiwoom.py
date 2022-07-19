from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Kiwoom() class start.")
        
        ################################
        # event loop를 실행하기 위한 변수
        self.login_event_loop = QEventLoop() # 로그인 요청용 이벤트 루프
        ################################
        
        ################################
        # 계좌 관련된 변수
        self.account_num = None # 계좌번호 담아줄 변수
        self.deposit = 0 # 예수금
        self.use_money = 0 # 실제 투자금
        self.use_money_percent = 0.5 # 예수금에서 사용할 비율
        self.output_deposit = 0 # 출력가능 금액
        ################################
        
        ################################
        # 요청 스크린 번호
        self.screen_my_info = "2000" # 계좌 관련 스크린 번호
        ################################
        
        ################################
        # 초기 세팅 함수들 바로 실행
        self.get_ocx_instance() # ocx 방식을 파이썬이 사용할 수 있게 변환해 주는 함수
        self.event_slots() # 키움과 연결하기 위한 시그널/슬롯 모음
        self.signal_login_commConnect() # 로그인 요청 함수
        self.get_account_info() # 계좌번호 가져오기
        self.detail_account_info() # 예수금 요청 시그널 포함
        ################################
        
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1") # 레지스트리에 저장된 api 모듈 불러오기
        
    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot) # 로그인 관련 이벤트
        
    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()") # 로그인 요청 시그널
        
        self.login_event_loop.exec_() # 이벤트 루프 실행
        
    def login_slot(self, err_code):
        print(errors(err_code)[1])
        
        self.login_event_loop.exit() # 로그인 처리 완료 시 이벤트 루프 종료
        
    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO") # 계좌번호 반환
        account_num = account_list.split(";")[0]
        
        self.account_num = account_num
        print("계좌번호 : %s" % account_num)
        
    def detail_account_info(self, sPrevNext="0"):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, Qstring, int, QString)", "예수금상세현황요청", "opw00001", sPrevNext, self.screen_my_info)