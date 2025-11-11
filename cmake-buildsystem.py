
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import json
from markdownify import markdownify as md
import re

from utils import get_page
from fastmcp import FastMCP

# Initialize FastMCP server for CMake buildsystem
mcp = FastMCP(name="CMakeBuildsystem")

@mcp.tool
def cmake_buildsystem_help() -> str:
    """help function for cmake_buildsystem()
    """
    with open('buildsystem.json') as f:
        variable_list:str = f.read()
        
    help_dict = {
        "description" : "This function search cmake variables. Such as, CMAKE_CXX_STANDARD, CMAKE_INCLUDE_PATH",
        "command list" : variable_list
    }
    
    return json.dumps(help_dict, ensure_ascii=False)

@mcp.tool
def get_buildsystem(index: str, version: str = "3.2") -> str:
    """search buildsystem document by index.
    build system is : \
        A CMake buildsystem is a set of high-level logical targets (executables, libraries, or custom commands) with explicit dependencies that determine build order and regeneration rules. \
        Targets propagate build specifications and usage requirements (include directories, compile definitions, link libraries) transitively through INTERFACE_* properties with visibility control (PRIVATE, PUBLIC, INTERFACE) to simplify dependency management
    Args:
        index: document index that want to get
        version: cmake version
    """
    
    ret = {
        "index": index,
        "contents": "",
    }
    
    html_str = get_page(f"/v{version}/manual/cmake-buildsystem.7.html")
    soup = BeautifulSoup(html_str, 'html.parser')
    
    # command ID 찾기 (하이픈으로 변경)
    contents = soup.find(id=index.replace(" ", "-").lower())
    
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