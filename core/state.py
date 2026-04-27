from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    target_code: str
    language: str
    time_limit: float
    test_history: Annotated[list[str], operator.add]
    current_test_case: str
    execution_result: dict
    status: str
    loop_count: int
