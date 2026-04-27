import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import AgentState
from core.models import TestCase
from tools.sandbox import run_code_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7)
structured_llm = llm.with_structured_output(TestCase)

def strategist_node(state: AgentState) -> dict:
    system_prompt = SystemMessage(content="You are an expert algorithmic security researcher. Your goal is to generate adversarial test cases to break the provided code or cause a Time Limit Exceeded error. Do not write code; only output the raw test case input.")
    
    human_prompt_content = f"""Target Code:
{state.get('target_code')}

Language: {state.get('language')}
Time Limit: {state.get('time_limit')} seconds

Previous Test Cases (Do not repeat these):
{state.get('test_history', [])}

Generate the next adversarial test case to break this code or cause a timeout."""

    human_prompt = HumanMessage(content=human_prompt_content)
    
    result = structured_llm.invoke([system_prompt, human_prompt])
    
    print(f"\n[Strategist Reasoning]: {result.reasoning}")
    
    return {
        'current_test_case': result.input_data,
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
