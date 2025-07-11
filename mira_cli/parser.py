# 코드 파싱 및 백엔드 전송을 담당하는 모듈

import os
from pathlib import Path
import requests
from rich.progress import Progress, SpinnerColumn, TextColumn
from tree_sitter_language_pack import get_language, get_parser
import fnmatch # glob 스타일 패턴 매칭을 위해 추가
import json # JSON 디버깅을 위해 추가

from mira_cli.config_loader import BACKEND_API_URL
from mira_cli.utils import console


# Tree-sitter 노드를 사용자 정의 AST 노드 형식으로 변환
def convert_to_ast_node(sitter_node):
    if not sitter_node:
        return None

    node_value = ""
    if sitter_node.is_named and sitter_node.text:
        node_value = sitter_node.text.decode('utf-8')

    ast_node = {
        "type": sitter_node.type,
        "value": node_value,
        "startPosition": {"row": sitter_node.start_point[0], "column": sitter_node.start_point[1]},
        "endPosition": {"row": sitter_node.end_point[0], "column": sitter_node.end_point[1]},
        "children": []
    }

    for child in sitter_node.children:
        ast_node["children"].append(convert_to_ast_node(child))
    
    return ast_node

# .gitignore 파일에서 무시 패턴을 로드
def load_gitignore_patterns(base_path):
    """
    .gitignore 파일에서 패턴을 읽어옵니다.
    """
    gitignore_path = Path(base_path) / ".gitignore"
    patterns = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # .gitignore 패턴을 fnmatch에 맞게 조정
                    if line.startswith('/'):
                        line = line[1:] # 루트 기준 패턴
                    elif line.startswith('**/'):
                        pass # 그대로 사용
                    else:
                        line = '**/' + line # 모든 하위 디렉토리에서 매칭
                    patterns.append(line)
    return patterns

# 파일 경로가 무시 패턴에 해당하는지 확인
def is_ignored(file_path, base_path, ignore_patterns):
    """
    파일 경로가 무시 패턴에 해당하는지 확인합니다.
    """
    relative_path = str(file_path.relative_to(base_path))
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
    return False

# 코드베이스를 파싱하고 백엔드로 전송
def parse_codebase_and_send_to_backend(path):
    console.print(f"[bold green]'{path}'[/bold green] 파싱을 시작합니다...")

    # .gitignore 패턴 로드
    ignore_patterns = load_gitignore_patterns(path)
    # 추가적인 기본 제외 패턴 (가상 환경, 빌드 디렉토리 등)
    # TODO: 이 기본 제외 패턴들을 설정 파일 등을 통해 사용자 정의 가능하도록 개선 고려
    default_ignore_patterns = [
        'venv/', 'venv/**',
        '__pycache__/', '__pycache__/**',
        '.git/', '.git/**',
        '.idea/', '.idea/**',
        '*.pyc', '*.class', '*.jar', '*.war', '*.ear', # 컴파일된 파일
        'node_modules/', 'node_modules/**', # JavaScript 프로젝트
        'build/', 'build/**', # 빌드 디렉토리
        'dist/', 'dist/**', # 배포 디렉토리
        'target/', 'target/**', # Maven/Gradle 빌드 디렉토리
        '*.log', '*.tmp', '*.temp', # 로그 및 임시 파일
        'config.ini', # 설정 파일
        'requirements.txt', # 의존성 파일 (파싱 대상 아님)
        'pyproject.toml', # 프로젝트 설정 파일 (파싱 대상 아님)
        'README.md', # README 파일 (파싱 대상 아님)
        'tests/', 'tests/**', # 테스트 파일 (파싱 대상 아님)
    ]
    ignore_patterns.extend(default_ignore_patterns)

    # 파일 확장자별 언어 매핑
    language_map = {
        '.java': 'java',
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.c': 'c',
        '.cpp': 'cpp',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.rb': 'ruby',
        '.cs': 'c_sharp',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.xml': 'xml',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.md': 'markdown',
        '.sh': 'bash',
        '.sql': 'sql',
        '.vue': 'vue',
        '.svelte': 'svelte',
        '.jsx': 'javascript', # JSX는 JavaScript 파서 사용
        '.tsx': 'typescript', # TSX는 TypeScript 파서 사용
    }

    parsers = {}

    # 파일 확장자에 따른 파서 가져오기
    def _get_parser(file_extension):
        lang_name = language_map.get(file_extension)
        if not lang_name:
            return None, None

        if lang_name not in parsers:
            try:
                parser = get_parser(lang_name) # type: ignore
                parsers[lang_name] = parser
            except Exception as e:
                console.print(f"[bold red]언어 파서 로드 오류 ({lang_name}):[/bold red] {e}")
                return None, None
        return parsers[lang_name], lang_name

    all_files_to_parse = []
    # 디렉토리 순회하며 파싱할 파일 목록 생성
    for root, dirs, files in os.walk(path):
        # 제외 디렉토리 처리
        dirs[:] = [d for d in dirs if not is_ignored(Path(root) / d, Path(path), ignore_patterns)]

        for file in files:
            file_path = Path(root) / file
            if not is_ignored(file_path, Path(path), ignore_patterns):
                all_files_to_parse.append(file_path)

    all_parsed_successfully = True
    # 파싱 진행률 표시
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("[green]파일 파싱 및 백엔드 전송 중...", total=len(all_files_to_parse))
        for file_path in all_files_to_parse:
            file_extension = file_path.suffix
            parser, lang_name = _get_parser(file_extension)

            if not parser:
                console.print(f"[yellow]지원되지 않는 파일 형식 또는 파서 로드 실패: {file_path}[/yellow]")
                progress.update(task, advance=1)
                continue

            try:
                with open(file_path, 'rb') as f:
                    source_code = f.read()
                
                tree = parser.parse(source_code)
                root_sitter_node = tree.root_node
                
                ast_node = convert_to_ast_node(root_sitter_node)
                
                parse_result = {
                    "filePath": str(file_path),
                    "language": lang_name,
                    "rootNode": ast_node
                }
                
                response = requests.post(f"{BACKEND_API_URL}/parser/parse", json=parse_result)
                # TODO: 디버깅용 코드. 실제 배포 시에는 제거하거나 로깅 시스템으로 대체
                console.print(f"Sending JSON for {file_path}:\n{json.dumps(parse_result, indent=2)}")
                response.raise_for_status()
                # console.print(f"리[bold green]'{file_path}' 파싱 결과 전송 성공:[/bold green] {response.text}")
            except requests.exceptions.ConnectionError:
                console.print("[bold red]오류:[/bold red] 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
                return False # 연결 오류 시 즉시 중단
            except requests.exceptions.HTTPError as e:
                console.print(f"[bold red]오류:[/bold red] 백엔드에서 오류 응답: {e.response.status_code} - {e.response.text}")
                all_parsed_successfully = False
            except Exception as e:
                console.print(f"[bold red]예상치 못한 오류 발생:[/bold red] {e}")
                all_parsed_successfully = False
            progress.update(task, advance=1)
    return all_parsed_successfully