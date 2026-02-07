"""
MCP-style trace tracking for tool calls.
Records every tool invocation with inputs, outputs, timing, and status.
"""

import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ToolCall:
    """Single MCP-style tool invocation record."""
    tool_name: str
    inputs: Dict[str, Any]
    output: Any = None
    status: str = "pending"  # pending | success | error
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0.0
    error: Optional[str] = None


class MCPTrace:
    """Tracks a sequence of tool calls for display in the UI."""

    def __init__(self):
        self.calls: List[ToolCall] = []

    def start_call(self, tool_name: str, inputs: Dict[str, Any]) -> int:
        """Register a new tool call. Returns its index."""
        call = ToolCall(tool_name=tool_name, inputs=inputs)
        self.calls.append(call)
        return len(self.calls) - 1

    def end_call(self, index: int, output: Any, error: Optional[str] = None):
        """Finalize a tool call with its output or error."""
        call = self.calls[index]
        call.output = output
        call.duration_ms = round((time.time() - call.timestamp) * 1000, 1)
        call.status = "error" if error else "success"
        call.error = error

    def get_calls(self) -> List[ToolCall]:
        """Return all recorded tool calls."""
        return self.calls

    def reset(self):
        """Clear all recorded calls."""
        self.calls = []
