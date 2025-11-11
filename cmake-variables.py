
from bs4 import BeautifulSoup
from bs4.element import NavigableString

import json

from markdownify import markdownify as md
import re

from utils import get_page
from fastmcp import FastMCP

# Initialize FastMCP server for CMake variables
mcp = FastMCP(name="CMakeVariables")

@mcp.tool
def cmake_variables_help() -> str:
    """help function for cmake_variables()
    """
    with open('variables.txt') as f:
        variable_list:str = f.read()
        
    help_dict = {
        "description" : "This function search cmake variables. Such as, CMAKE_CXX_STANDARD, CMAKE_INCLUDE_PATH",
        "command list" : variable_list
    }
    
    return json.dumps(help_dict, ensure_ascii=False)

@mcp.tool
def get_variables(variable: str, version: str = "3.2") -> str:
    """search cmake variable
    Args:
        command: cmake variable for search
        version: cmake version
    """
    var = variable.replace("<","").replace(">","")
    ret = {
        "variable": variable,
        "contents": "",
    }
    
    html_str = get_page(f"/v{version}/variable/{var}.html")
    soup = BeautifulSoup(html_str, 'html.parser')
    
    # command ID 찾기 (하이픈으로 변경)
    contents = soup.find(id=var.replace("_", "-").lower())
    
    if contents is None:
        return json.dumps(ret, ensure_ascii=False)
    
    # 1. 링크 제거 (contents 안에서만)
    for link in contents.find_all('a'):
        link.unwrap()
    
    # 2. <p> 태그 내부의 모든 텍스트 노드에서 개행 제거
    for paragraph in soup.find_all('p'):
        for element in paragraph.descendants:
            if isinstance(element, NavigableString):
                parent = element.parent
                if parent and parent.name != 'code':
                    cleaned = ' '.join(str(element).split())
                    if cleaned:
                        element.replace_with(cleaned)
    
    # 3. Markdown 변환
    markdown = md(str(contents))
    
    # 4. 추가 정리 (선택사항)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    ret["contents"] = markdown.replace('\\', '')

    return json.dumps(ret, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()
