import asyncio
import importlib.util
from fastmcp import FastMCP

# Import subservers using importlib for files with hyphens
def import_module_from_file(file_path, module_name):
    """Import a module from a file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import subservers
commands_module = import_module_from_file("cmake-commands.py", "cmake_commands")
variables_module = import_module_from_file("cmake-variables.py", "cmake_variables")
buildsystem_module = import_module_from_file("cmake-buildsystem.py", "cmake_buildsystem")

commands_mcp = commands_module.mcp
variables_mcp = variables_module.mcp
buildsystem_mcp = buildsystem_module.mcp

# Create main server
mcp = FastMCP(name="CMakeDocumentation")

async def setup_server():
    """Setup the main server by importing all subservers with prefixes"""
    await mcp.import_server(commands_mcp, prefix="commands")
    await mcp.import_server(variables_mcp, prefix="variables")
    await mcp.import_server(buildsystem_mcp, prefix="buildsystem")

if __name__ == "__main__":
    # Run setup and then start the server
    asyncio.run(setup_server())
    mcp.run(transport="http", host="127.0.0.1", port=18080)