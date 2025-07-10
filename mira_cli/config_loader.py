import configparser
from pathlib import Path
from mira_cli.utils import console

# 설정 파일 (config.ini)을 로드하는 함수
def load_config():
    config = configparser.ConfigParser()
    # config.ini 파일 경로 설정 (현재 파일의 부모 디렉토리의 부모 디렉토리)
    config.read(Path(__file__).parent.parent / 'config.ini')
    return {
        "BACKEND_API_URL": config['backend']['api_url'],
        "WEB_UI_URL": config['frontend']['web_ui_url']
    }

# 설정 데이터 로드
config_data = load_config()
# 백엔드 API URL
BACKEND_API_URL = config_data["BACKEND_API_URL"]
# 웹 UI URL
WEB_UI_URL = config_data["WEB_UI_URL"]
