import time
import logging
import os
from dotenv import load_dotenv
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError

# --- 사용자 정보 ---
# !! 중요 !!: 스크립트에 비밀번호를 직접 저장하는 것은 매우 위험합니다. (Windows 자격 증명 관리자 등을 사용하는 것이 안전합니다.)
# 알빠노
load_dotenv('user-example.env')
userid = os.getenv('userid')
password = os.getenv('password')

# 창 제목
window_title = "INHA CLOUDHUB"

while True:
    try:
        # 1. "INHA CLOUDHUB" 창에 연결 시도
        logging.info(f"'{window_title}' 창에 연결을 시도합니다...")
        app = Application(backend="uia").connect(title=window_title, timeout=10)

        # 2. 창 핸들 얻기 및 활성화
        dlg = app.window(title=window_title)
        logging.info("창을 찾았습니다. 활성화합니다.")
        dlg.set_focus()
        time.sleep(0.5)

        # 3. UI 요소 식별 및 상호작용
        logging.info("UI 요소 자동 입력을 시작합니다...")

        # 4. '확인' 버튼 찾기
        try:
            # inspect.exe를 활용해 해당 요소 찾기
            check_button = dlg.child_window(title="확인", control_type="Button")
            check_button.wait('visible enabled', timeout=60) # 시간 확보
            logging.info("'확인' 버튼 찾음. 클릭 시도...")
            check_button.click_input()
            logging.info("'확인' 버튼 클릭 완료.")
        except ElementNotFoundError:
            logging.critical("'확인' 버튼을 찾을 수 없습니다. Inspect.exe로 정확한 AutomationId, ControlType을 확인하세요.")
            exit()
        except Exception as e:
            logging.critical(f"'확인' 버튼 처리 중 예상치 못한 오류: {e}")
            exit()

        # --- ID 필드 ---
        try:
            logging.info("ID 필드를 찾습니다...")
            id_field = dlg.child_window(auto_id="username", control_type="Edit")
            id_field.wait('visible enabled', timeout=15)
            logging.info("ID 필드 찾음. 값 입력 시도...")
            id_field.type_keys(userid, with_spaces=True)
            logging.info(f"ID 입력 완료: {userid}")
            time.sleep(0.5)
        except ElementNotFoundError:
            logging.critical("오류: ID 필드('username')를 찾을 수 없습니다.")
            logging.critical("Inspect.exe 로 정확한 AutomationId 와 ControlType 을 확인하세요.")
            exit()
        except Exception as e:
            logging.critical(f"ID 필드 처리 중 예상치 못한 오류: {e}")
            exit()

        # --- 비밀번호 필드 ---
        try:
            logging.info("비밀번호 필드를 찾습니다...")
            password_field = dlg.child_window(auto_id="password", control_type="Edit")
            password_field.wait('visible enabled', timeout=15)
            logging.info("비밀번호 필드 찾음. 값 입력 시도...")
            password_field.type_keys(password, with_spaces=True)
            logging.info("비밀번호 입력 완료.")
            time.sleep(0.5)
        except ElementNotFoundError:
            logging.critical("오류: 비밀번호 필드('password')를 찾을 수 없습니다.")
            logging.critical("Inspect.exe 로 정확한 AutomationId 와 ControlType 을 확인하세요.")
            exit()
        except Exception as e:
            logging.critical(f"비밀번호 필드 처리 중 예상치 못한 오류: {e}")
            exit()

        # --- 로그인 버튼 ---
        try:
            logging.info("로그인 버튼을 찾습니다...")
            login_button = dlg.child_window(auto_id="submit", control_type="Button")
            login_button.wait('visible enabled', timeout=15)
            logging.info("로그인 버튼 찾음. 클릭 시도...")
            login_button.click_input()
            logging.info("로그인 버튼 클릭 완료.")
        except ElementNotFoundError:
            logging.critical("오류: 로그인 버튼('submit' 또는 '로그인' 텍스트)을 찾을 수 없습니다.")
            logging.critical("Inspect.exe 로 정확한 AutomationId, Name, ControlType 을 확인하세요.")
            exit()
        except Exception as e:
            logging.critical(f"로그인 버튼 처리 중 예상치 못한 오류: {e}")
            exit()

        logging.info("자동 로그인 스크립트 실행 완료.")

    except Exception as e:
        # 창을 찾지 못했거나 연결 중 다른 오류 발생 시
        logging.warning(f"자동화 스크립트 실행 중 오류 발생: {e}")