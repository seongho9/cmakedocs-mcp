
from bs4 import BeautifulSoup
from bs4.element import NavigableString

import json
from markdownify import markdownify as md
import re

from utils import get_page

from fastmcp import FastMCP

# Initialize FastMCP server for CMake commands
mcp = FastMCP(name="CMakeCommands")

@mcp.tool
def cmake_command_help() -> str:
    """help function for cmake_command()
    """
    with open('commands.txt') as f:
        command_list_str:str = f.read()
        
    help_dict = {
        "description" : "This function search cmake commands. Such as, add_executable(), add_library()",
        "command list" : command_list_str
    }
    
    return json.dumps(help_dict, ensure_ascii=False)

@mcp.tool
def cmake_command(command: str, version: str = "3.2") -> str:
    """search cmake command
    Args:
        command: cmake command for search
        version: cmake version
    """
    ret = {
        "command": command,
        "contents": "",
    }
    
    html_str = get_page(f"/v{version}/command/{command}.html")
    soup = BeautifulSoup(html_str, 'html.parser')
    
    # command ID 찾기 (하이픈으로 변경)
    contents = soup.find(id=command.replace("_", "-"))
    
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
