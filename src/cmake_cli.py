import requests
from bs4 import BeautifulSoup
import json
cmake_root: str = "https://cmake.org/cmake/help"

command_line_tools: list[dict[str,str]] = \
[
    {
        "contents":"cmake",
        "description":"\
            The \"cmake\" executable is the CMake command-line interface.\
            It may use to configure projects in scripts."
    },
    {
        "contents":"ctest",
        "description":"\
            The \"ctest\" executable iis the CMake test driver program.\
            CMake-generated build trees created for projects that use the ENABLE_TESTING and ADD_TEST commands have testing support.\
            This program will run the tests and report results."
    },
    {
        "contents":"cpack",
        "description":"\
            The \"cpack\" executable is the CMake packaging program.\
            CMake-generated build trees created for projects that use the INSTALL_* commands have packaging support.\
            This program will generate the package."     
    }
]

def get_page(path: str) -> str:
    """Fetch a page and return raw HTML content"""
    res = requests.get(f"{cmake_root}/{path}")
    res.encoding = 'utf-8'
    return res.text


def get_command_tools_basic(contents: str, version: str) -> str:
    ret = {
        "command": contents,
        "synopsis" : [],
        "description" : ""
    }
    
    path = {
        "cmake" : "manual/cmake.1.html",
        "ctest" : "manual/ctest.1.html",
        "cpack" : "manual/cpack.1.html"
    }
    
    contents = get_page(f"v{version}/{path[contents]}")
    
    soup = BeautifulSoup(contents, 'html.parser')
    
    # Synopsis
    synopsis = soup.select_one('#synopsis pre')
    if synopsis is None:
        return json.dumps(ret, ensure_ascii=False)
    
    synopsis_list =  synopsis.get_text().split("\n")
    for content in synopsis_list:
        ret["synopsis"].append(content)
    
    # Description
    desc = soup.select('#description > p')
    if desc is None:
        return json.dumps(ret, ensure_ascii=False)
    
    # ret["description"] = description[1].get_text()    
    for item in desc:
        ret["description"] += f"{item.get_text()}\n"
    
    ret["description"] = ret["description"].replace('\n',' ')
    return json.dumps(ret, ensure_ascii=False, indent=2)

def get_command_tools_options_basic(contents: str, version: str) -> str:
    
    ret = {
        "command": contents,
        "options" : []
    }
        
    path = {
        "cmake" : "manual/cmake.1.html",
        "ctest" : "manual/ctest.1.html",
        "cpack" : "manual/cpack.1.html"
    }
    
    contents = get_page(f"v{version}/{path[contents]}")
    soup = BeautifulSoup(contents, 'html.parser')
    
    options_head = soup.select('#options > dl > dt')
    options_body = soup.select('#options > dl > dd')
    if options_head is None or options_body is None:
        return json.dumps(ret, ensure_ascii=False)
    
    for idx in range(len(options_head)):
        option = {
            "command" : "",
            "description" : ""
        }
        option["command"] = options_head[idx].get_text()
        option["description"] = options_body[idx].select('p')[0].get_text()

        ret["options"].append(option)
        
    return json.dumps(ret, ensure_ascii=False, indent=2)

def get_command_tools_option_detail(contents: str, version: str, option: str) -> str:
    
    ret = {
        "command": contents,
        "option": option,
        "description" : ""
    }
        
    path = {
        "cmake" : "manual/cmake.1.html",
        "ctest" : "manual/ctest.1.html",
        "cpack" : "manual/cpack.1.html"
    }
    
    contents = get_page(f"v{version}/{path[contents]}")
    soup = BeautifulSoup(contents, 'html.parser')
    
    options_head = soup.select('#options > dl > dt')
    options_body = soup.select('#options > dl > dd')
    if options_head is None or options_body is None:
        return json.dumps(ret, ensure_ascii=False)
    
    for idx in range(len(options_head)):
        
        if option in options_head[idx].get_text():
            ret["description"] = options_body[idx].get_text().replace("\n", " ")
            break
    
    return json.dumps(ret, ensure_ascii=False, indent=2)
    
if __name__ == "__main__":
    item = get_command_tools_options_basic("cmake", "3.2")
    #item = get_command_tools_option_detail("cmake", "3.2", "-C <initial-cache>")
    print(item)