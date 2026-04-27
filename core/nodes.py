from core.state import AgentState
from tools.sandbox import run_code_tool

def strategist_node(state: AgentState) -> dict:
    return {
        'current_test_case': 'mock_input',
        'loop_count': state.get('loop_count', 0) + 1
    }

def executor_node(state: AgentState) -> dict:
    result = run_code_tool(
        code_string=state['target_code'],
        language=state['language'],
        test_case_input=state.get('current_test_case', ''),
        time_limit=state.get('time_limit', 2.0)
    )
    return {
        'execution_result': result,
        'test_history': [state.get('current_test_case', '')]
    }

def evaluator_node(state: AgentState) -> dict:
    result = state.get('execution_result', {})
    if result.get('exit_code') != 0 or result.get('status') == "timeout":
        return {'status': 'bug_found'}
    else:
        return {'status': 'passed'}
