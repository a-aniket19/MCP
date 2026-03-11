from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

# In-memory history store
history = []

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together"""
    result = a + b
    history.append(f"{a} + {b} = {result}")
    return result

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    result = a - b
    history.append(f"{a} - {b} = {result}")
    return result

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together"""
    result = a * b
    history.append(f"{a} * {b} = {result}")
    return result

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    result = a / b
    history.append(f"{a} / {b} = {result}")
    return result

@mcp.resource("calculator://history")
def get_history() -> str:
    """Returns the history of all calculations performed"""
    if not history:
        return "No calculations yet."
    return "\n".join(history)

@mcp.tool()
def get_history() -> str:
    """Returns the history of all calculations performed"""
    if not history:
        return "No calculations yet."
    return "\n".join(history)

if __name__ == "__main__":
    mcp.run()