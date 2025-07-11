import click
import webbrowser
from mira_cli.shell import MIRAShell
from mira_cli.config_loader import WEB_UI_URL
from mira_cli.backend_api import (
    get_node_details,
    get_relationships_details,
    search_code_graph,
    analyze_impact_backend,
    find_tech_debt_backend,
    generate_docs_backend,
    refactor_suggestions_backend
)
from mira_cli.utils import console

# MIRA CLI의 메인 그룹 정의
@click.group()
def MIRA():
    """MIRA AI CLI"""
    pass

# 대화형 셸 시작 명령어
@MIRA.command()
def shell():
    """MIRA AI 대화형 셸을 시작합니다."""
    MIRAShell().cmdloop()

# CLI 버전 표시 명령어
@MIRA.command()
def version():
    """CLI 버전을 표시합니다."""
    console.print("MIRA CLI 버전: 0.1.0")

# 웹 UI 시각화 도구 열기 명령어
@MIRA.command()
def visualize():
    """웹 UI를 브라우저에서 엽니다."""
    console.print(f"웹 UI를 엽니다: {WEB_UI_URL}")
    webbrowser.open(WEB_UI_URL)

# 노드 세부 정보 조회 명령어
@MIRA.command()
@click.argument('node_id')
def get_node(node_id):
    """
    ID로 특정 노드의 세부 정보를 가져옵니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 노드 세부 정보를 직접 출력하는 기능 추가 고려
    """
    console.print(f"노드 ID '{node_id}' 세부 정보를 요청합니다. 결과는 웹 UI에서 확인하세요.")
    get_node_details(node_id)

# 노드 관계 조회 명령어
@MIRA.command()
@click.argument('node_id')
def get_relationships(node_id):
    """
    ID로 특정 노드의 관계를 가져옵니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 관계 세부 정보를 직접 출력하는 기능 추가 고려
    """
    console.print(f"노드 ID '{node_id}' 관계를 요청합니다. 결과는 웹 UI에서 확인하세요.")
    get_relationships_details(node_id)

# 코드 그래프 검색 명령어
@MIRA.command()
@click.argument('query_text')
def search(query_text):
    """
    코드 그래프에서 노드와 관계를 검색합니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 검색 결과를 직접 출력하는 기능 추가 고려
    """
    console.print(f"검색 쿼리: '{query_text}'를 요청합니다. 결과는 웹 UI에서 확인하세요.")
    search_code_graph(query_text)

# 코드 변경 영향 분석 명령어
@MIRA.command()
@click.argument('file_path')
def analyze_impact(file_path):
    """
    지정된 파일의 변경 사항이 코드베이스에 미치는 영향을 분석합니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 영향 분석 결과를 직접 출력하는 기능 추가 고려
    """
    console.print(f"'{file_path}' 영향 분석을 요청합니다. 결과는 웹 UI에서 확인하세요.")
    analyze_impact_backend(file_path)

# 기술 부채 식별 명령어
@MIRA.command()
@click.argument('file_path')
def find_tech_debt(file_path):
    """
    지정된 파일에서 기술 부채를 식별합니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 기술 부채 식별 결과를 직접 출력하는 기능 추가 고려
    """
    console.print(f"'{file_path}' 기술 부채 식별을 요청합니다. 결과는 웹 UI에서 확인하세요.")
    find_tech_debt_backend(file_path)

# 문서 생성 명령어
@MIRA.command()
@click.argument('file_path')
def generate_docs(file_path):
    """
    지정된 파일에 대한 문서를 생성합니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 문서 생성 결과를 직접 출력하는 기능 추가 고려
    """
    console.print(f"'{file_path}' 문서 생성을 요청합니다. 결과는 웹 UI에서 확인하세요.")
    generate_docs_backend(file_path)

# 리팩토링 제안 명령어
@MIRA.command()
@click.argument('file_path')
def refactor_suggestions(file_path):
    """
    지정된 파일에 대한 리팩토링 제안을 제공합니다. (결과는 웹 UI에서 확인)
    TODO: CLI에서 리팩토링 제안 결과를 직접 출력하는 기능 추가 고려
    """
    console.print(f"'{file_path}' 리팩토링 제안을 요청합니다. 결과는 웹 UI에서 확인하세요.")
    refactor_suggestions_backend(file_path)