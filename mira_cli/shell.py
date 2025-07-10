import cmd
import os
import requests

# 파서 및 설정 로더 임포트
from mira_cli.parser import parse_codebase_and_send_to_backend
from mira_cli.config_loader import BACKEND_API_URL
from mira_cli.utils import console

# MIRA 대화형 셸 클래스
class MIRAShell(cmd.Cmd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 코드베이스 파싱 여부 플래그
        self._parsed_codebase = False

    # 셸 시작 시 표시되는 소개 메시지
    intro = """
███╗   ███╗██╗██████╗  █████╗ 
████╗ ████║██║██╔══██╗██╔══██╗
██╔████╔██║██║██████╔╝███████║
██║╚██╔╝██║██║██╔══██╗██╔══██║
██║ ╚═╝ ██║██║██║  ██║██║  ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
MIRA 셸에 오신 것을 환영합니다! 도움말을 보려면 'help' 또는 '?'를 입력하세요. 종료하려면 'exit'를 입력하세요."""
    # 셸 프롬프트
    prompt = 'mira> '

    # 'exit' 명령어 처리
    def do_exit(self, arg):
        '셸을 종료합니다.'
        console.print("안녕히 가세요!")
        return True

    # EOF (Ctrl+D) 처리
    def do_EOF(self, arg):
        'Ctrl+D로 셸을 종료합니다.'
        return self.do_exit(arg)

    # 파싱된 데이터 초기화 명령어
    def do_clear_parsed_data(self, arg):
        '파싱된 코드베이스 데이터를 초기화합니다.'
        self._parsed_codebase = False
        console.print("파싱된 코드베이스 데이터가 초기화되었습니다.")

    # 알 수 없는 명령어 또는 자연어 쿼리 처리
    def default(self, line):
        '명령어를 찾을 수 없을 때 또는 자연어 쿼리를 처리합니다.'
        console.print(f"'{line}' 쿼리를 분석 중입니다...")
        
        # 코드베이스가 아직 파싱되지 않았다면 자동 파싱 시작
        if not self._parsed_codebase:
            console.print("코드베이스가 아직 파싱되지 않았습니다. 파싱을 시작합니다.")
            path = os.getcwd()
            console.print(f"현재 디렉토리: {path}를 코드베이스 루트로 사용합니다.")
            
            # 코드베이스 파싱 및 백엔드 전송
            if parse_codebase_and_send_to_backend(path):
                self._parsed_codebase = True
                console.print("코드베이스 파싱 및 전송 완료.")
            else:
                console.print("코드베이스 파싱 및 전송에 실패했습니다. 쿼리를 처리할 수 없습니다.")
                return

        try:
            print("쿼리 전송 중...") # TODO: 진행률 표시기 (Progress bar) 추가 고려
            # 백엔드 API로 쿼리 전송
            response = requests.post(f"{BACKEND_API_URL}/query", json={"query": line})
            response.raise_for_status()
            
            result = response.json()
            
            if result:
                print("쿼리 처리 완료. 결과는 웹 UI에서 확인하세요.") # TODO: CLI에서 쿼리 결과 직접 출력 기능 추가
            else:
                print("쿼리 결과가 없습니다. 웹 UI를 확인하세요.")

        except requests.exceptions.ConnectionError:
            print("오류: 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        except requests.exceptions.HTTPError as e:
            print(f"오류: 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
