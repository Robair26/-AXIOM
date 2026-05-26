import subprocess
import tempfile
import os
import sys

def run_python(code, timeout=10):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True, text=True, timeout=timeout, cwd='/tmp'
        )
        return (result.stdout or result.stderr or 'No output')[:2000]
    except subprocess.TimeoutExpired:
        return 'Error: Code timed out after 10 seconds'
    except Exception as e:
        return f'Error: {str(e)}'
    finally:
        os.unlink(temp_path)

def run_bash(code, timeout=10):
    try:
        result = subprocess.run(
            code, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd='/tmp',
            env={'PATH': '/usr/local/bin:/usr/bin:/bin', 'HOME': '/tmp'}
        )
        return (result.stdout or result.stderr or 'No output')[:2000]
    except subprocess.TimeoutExpired:
        return 'Error: Command timed out'
    except Exception as e:
        return f'Error: {str(e)}'

def execute_code(code, language='python'):
    if language.lower() in ['bash', 'shell']:
        return run_bash(code)
    return run_python(code)
