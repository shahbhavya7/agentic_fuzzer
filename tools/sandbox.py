import subprocess
import time
import os

def run_code_tool(code_string: str, language: str, test_case_input: str, time_limit: float = 2.0) -> dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace_dir = os.path.join(base_dir, 'workspace')
    os.makedirs(workspace_dir, exist_ok=True)
    
    file_ext = '.cpp' if language == 'cpp' else '.py'
    temp_file_name = f'temp{file_ext}'
    temp_file_path = os.path.join(workspace_dir, temp_file_name)
    exe_file_path = os.path.join(workspace_dir, 'temp.exe')
    
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(code_string)
        
    result = {
        'stdout': '',
        'stderr': '',
        'execution_time_seconds': 0.0,
        'exit_code': 0,
        'status': 'success'
    }
    
    try:
        if language == 'cpp':
            compile_cmd = ['g++', temp_file_name, '-o', 'temp.exe']
            compile_process = subprocess.run(compile_cmd, cwd=workspace_dir, capture_output=True, text=True)
            if compile_process.returncode != 0:
                result['exit_code'] = 1
                result['stderr'] = compile_process.stderr
                result['status'] = 'error'
                return result
            
            run_cmd = [exe_file_path]
            
        elif language == 'python':
            run_cmd = ['python', temp_file_name]
        else:
            result['status'] = 'error'
            result['stderr'] = f"Unsupported language: {language}"
            result['exit_code'] = 1
            return result
        
        start_time = time.time()
        try:
            exec_process = subprocess.run(
                run_cmd,
                cwd=workspace_dir,
                input=test_case_input,
                text=True,
                capture_output=True,
                timeout=time_limit
            )
            execution_time = time.time() - start_time
            
            result['stdout'] = exec_process.stdout
            result['stderr'] = exec_process.stderr
            result['execution_time_seconds'] = execution_time
            result['exit_code'] = exec_process.returncode
            if exec_process.returncode != 0:
                result['status'] = 'error'
                
        except subprocess.TimeoutExpired as e:
            execution_time = time.time() - start_time
            result['status'] = 'timeout'
            result['execution_time_seconds'] = execution_time
            result['stdout'] = e.stdout if e.stdout else ''
            result['stderr'] = e.stderr if e.stderr else ''
            result['exit_code'] = -1
            
    finally:
        for path in [temp_file_path, exe_file_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
                    
    return result
