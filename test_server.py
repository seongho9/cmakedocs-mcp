import asyncio
import importlib.util
from fastmcp import Client

# Import main server
def import_module_from_file(file_path, module_name):
    """Import a module from a file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

async def test_server():
    """Test the unified CMake MCP server"""
    main_module = import_module_from_file("cmake_mcp_main.py", "cmake_mcp_main")

    # Setup the server
    await main_module.setup_server()

    async with Client(main_module.main_mcp) as client:
        print("=" * 80)
        print("Testing CMake Documentation MCP Server")
        print("=" * 80)

        # Test ping
        print("\n1. Testing server ping...")
        await client.ping()
        print("✓ Server is alive!")

        # List all tools
        print("\n2. Listing all available tools...")
        tools = await client.list_tools()
        print(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")

        # Test a command tool
        print("\n3. Testing commands_cmake_command_help tool...")
        result = await client.call_tool("commands_cmake_command_help", {})
        result_text = str(result.content[0].text) if hasattr(result, 'content') else str(result)
        print(f"✓ Result preview: {result_text[:200]}...")

        print("\n" + "=" * 80)
        print("All tests passed successfully!")
        print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_server())