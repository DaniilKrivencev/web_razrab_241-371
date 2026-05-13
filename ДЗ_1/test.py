import subprocess
import pytest
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

INTERPRETER = sys.executable

def run_script(filename, input_data=None):
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    input_str = '\n'.join(input_data if input_data else [])
    if input_str:
        input_str += '\n'
        
    proc = subprocess.run(
        [INTERPRETER, filename],
        input=input_str,
        capture_output=True,
        text=True,
        check=False,
        encoding='utf-8',
        env=env
    )
    if proc.returncode != 0:
        # If script failed, return stderr for debugging or empty if expected
        # But we usually test stdout. Let's print stderr to stdout if valid?
        # Or just return concatenated output?
        # For now, stick to stdout, but print stderr if debug needed.
        if proc.stderr:
            sys.stderr.write(f"Error running {filename}: {proc.stderr}\n")
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50'])
    ]
}

def test_hello_world():
    assert run_script('hello.py') == 'Hello, World!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

def test_division():
    output = run_script('division.py', ['3', '5']).split('\n')
    assert output == ['0', '0.6']

def test_loops():
    output = run_script('loops.py', ['3']).split('\n')
    assert output == ['0', '1', '4']

def test_print_function():
    assert run_script('print_function.py', ['5']) == '12345'

def test_second_score():
    assert run_script('second_score.py', ['5', '2 3 6 6 5']) == '5'

def test_nested_list():
    input_data = ['5', 'Гарри', '37.21', 'Берри', '37.21', 'Тина', '37.2', 'Акрити', '41', 'Харш', '39']
    output = run_script('nested_list.py', input_data).split('\n')
    # Order might vary if logic differs, but task asked for alphabetical.
    # Expected: Берри first, then Гарри (alphabetical)
    # Check if sorting works for Cyrillic/English mix?
    # Actually names are Cyrillic in example input.
    # 'Берри' < 'Гарри'? Yes, Б < Г.
    assert output == ['Берри', 'Гарри']

def test_lists():
    input_cmds = [
        '12',
        'insert 0 5',
        'insert 1 10',
        'insert 0 6',
        'print',
        'remove 6',
        'append 9',
        'append 1',
        'sort',
        'print',
        'pop',
        'reverse',
        'print'
    ]
    expected = [
        '[6, 5, 10]',
        '[1, 5, 9, 10]',
        '[9, 5, 1]'
    ]
    assert run_script('lists.py', input_cmds).split('\n') == expected

def test_swap_case():
    assert run_script('swap_case.py', ['Www.MosPolytech.ru']) == 'wWW.mOSpOLYTECH.RU'

def test_split_and_join():
    assert run_script('split_and_join.py', ['this is a string']) == 'this-is-a-string'

def test_minion_game():
    # Example input from task
    assert run_script('minion_game.py', ['BANANA']) == 'Стюарт 12'

def test_is_leap():
    assert run_script('is_leap.py', ['2000']) == 'True'
    assert run_script('is_leap.py', ['1990']) == 'False'

def test_happiness():
    input_data = ['3 2', '1 5 3', '3 1', '5 7']
    assert run_script('happiness.py', input_data) == '1'
