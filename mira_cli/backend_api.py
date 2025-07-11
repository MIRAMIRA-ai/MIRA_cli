import requests
from rich.console import Console
from mira_cli.config_loader import BACKEND_API_URL, WEB_UI_URL
import webbrowser

console = Console()

# 백엔드로 쿼리를 전송하는 함수
def send_query_to_backend(query):
    try:
        response = requests.post(f"{BACKEND_API_URL}/query", json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return None
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")
        return None

# 특정 노드의 세부 정보를 백엔드에 요청하고 웹 UI를 여는 함수
def get_node_details(node_id):
    try:
        # TODO: 백엔드로부터 노드 세부 정보를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.get(f"{BACKEND_API_URL}/graph/node/{node_id}").raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/node/{node_id}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")

# 특정 노드의 관계 정보를 백엔드에 요청하고 웹 UI를 여는 함수
def get_relationships_details(node_id):
    try:
        # TODO: 백엔드로부터 관계 세부 정보를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.get(f"{BACKEND_API_URL}/graph/relationships/{node_id}").raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/relationships/{node_id}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")

# 코드 그래프 검색을 백엔드에 요청하고 웹 UI를 여는 함수
def search_code_graph(query_text):
    try:
        # TODO: 백엔드로부터 검색 결과를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.get(f"{BACKEND_API_URL}/graph/search", params={"query": query_text}).raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/search?query={query_text}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")

# 코드 변경 영향 분석을 백엔드에 요청하고 웹 UI를 여는 함수
def analyze_impact_backend(file_path):
    try:
        # TODO: 백엔드로부터 영향 분석 결과를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.get(f"{BACKEND_API_URL}/analysis/impact", params={"filePath": file_path}).raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/analyze-impact?filePath={file_path}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")

# 기술 부채 식별을 백엔드에 요청하고 웹 UI를 여는 함수
def find_tech_debt_backend(file_path):
    try:
        # TODO: 백엔드로부터 기술 부채 식별 결과를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.get(f"{BACKEND_API_URL}/analysis/tech-debt", params={"filePath": file_path}).raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/tech-debt?filePath={file_path}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")

# 문서 생성을 백엔드에 요청하고 웹 UI를 여는 함수
def generate_docs_backend(file_path):
    try:
        # TODO: 백엔드로부터 문서 생성 결과를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.post(f"{BACKEND_API_URL}/generation/docs", json={"filePath": file_path}).raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/docs?filePath={file_path}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")

# 리팩토링 제안을 백엔드에 요청하고 웹 UI를 여는 함수
def refactor_suggestions_backend(file_path):
    try:
        # TODO: 백엔드로부터 리팩토링 제안 결과를 직접 받아와 CLI에 출력하는 기능 추가 고려
        requests.post(f"{BACKEND_API_URL}/generation/refactor-suggestions", json={"filePath": file_path}).raise_for_status()
        console.print("요청 성공. 웹 UI를 엽니다.")
        webbrowser.open(f"{WEB_UI_URL}/refactor-suggestions?filePath={file_path}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")
