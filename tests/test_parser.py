import pytest
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
import shutil
import json

from mira_cli.parser import parse_codebase_and_send_to_backend

@pytest.fixture
def temp_codebase(tmp_path):
    # 임시 코드베이스 디렉토리 생성
    codebase_path = tmp_path / "test_codebase"
    codebase_path.mkdir()

    # 더미 Python 파일 생성
    (codebase_path / "complex_python.py").write_text("""class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        if self.name:
            print(f"Hello, {self.name}!")
        else:
            print("Hello, stranger!")

def calculate_sum(a, b):
    return a + b

# A comment
variable = calculate_sum(10, 20)
""")
    # 더미 Java 파일 생성
    (codebase_path / "ComplexJava.java").write_text("""package com.example.app;

import java.util.List;
import java.util.ArrayList;

public class ComplexJava {
    private String message;

    public ComplexJava(String msg) {
        this.message = msg;
    }

    public void printMessage() {
        System.out.println(this.message);
    }

    public static int sumList(List<Integer> numbers) {
        int total = 0;
        for (int num : numbers) {
            total += num;
        }
        return total;
    }

    public static void main(String[] args) {
        ComplexJava obj = new ComplexJava("Hello from Java!");
        obj.printMessage();

        List<Integer> nums = new ArrayList<>();
        nums.add(1);
        nums.add(2);
        nums.add(3);
        System.out.println("Sum: " + sumList(nums));
    }
}
""")
    # 지원되지 않는 파일 형식 (파싱 건너뛰는지 확인)
    (codebase_path / "unsupported.txt").write_text("This is a text file.")

    yield codebase_path

    # 테스트 후 임시 코드베이스 삭제
    shutil.rmtree(codebase_path)

def test_parse_codebase_and_send_to_backend(temp_codebase):
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "Success"
        mock_post.return_value = mock_response

        # parse_codebase_and_send_to_backend 함수 호출
        success = parse_codebase_and_send_to_backend(str(temp_codebase))

        # 함수가 성공적으로 실행되었는지 확인
        assert success is True

        # requests.post가 예상대로 호출되었는지 확인
        # Python 파일과 Java 파일에 대해 각각 한 번씩 호출되어야 함
        assert mock_post.call_count == 2

        # 호출된 인자 확인 (예시)
        calls = mock_post.call_args_list
        assert any("complex_python.py" in call.kwargs['json']['filePath'] for call in calls)
        assert any("ComplexJava.java" in call.kwargs['json']['filePath'] for call in calls)

        # AST 노드 구조가 올바른지 대략적으로 확인 (더미 데이터이므로 깊은 검증은 어려움)
        for call in calls:
            json_data = call.kwargs['json']
            print(f"--- Parsed Data for {json_data['filePath']} ---")
            print(json.dumps(json_data, indent=2)) # JSON 형식으로 예쁘게 출력
            assert "filePath" in json_data
            assert "language" in json_data
            assert "rootNode" in json_data
            assert "type" in json_data['rootNode']
            assert "children" in json_data['rootNode']
