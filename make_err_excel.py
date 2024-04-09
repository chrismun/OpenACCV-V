import json
import pandas as pd

def extract_failing_tests(json_file):
    """
    Extracts failing tests and their errors from the specified JSON file.

    Parameters:
    - json_file (str): Path to the JSON file containing test results.

    Returns:
    - Tuple[pd.DataFrame, pd.DataFrame]: Two DataFrames, the first with detailed failing tests info and the second with aggregated info per test.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    detailed_failing_tests = []
    aggregated_failing_tests = {}

    for test_name, runs in data.get('runs', {}).items():
        for run in runs:
            compilation_result = run.get('compilation', {}).get('result', 0)
            runtime_result = run.get('runtime', {}).get('result', 0)

            if compilation_result != 0 or runtime_result != 0:
                detailed_failing_tests.append({
                    'Test Name': test_name,
                    'Compilation Error': run.get('compilation', {}).get('errors', '').strip(),
                    'Runtime Error': run.get('runtime', {}).get('errors', '').strip(),
                    'Compilation Result': compilation_result,
                    'Runtime Result': runtime_result
                })

                if test_name not in aggregated_failing_tests:
                    aggregated_failing_tests[test_name] = {
                        'Compilation Error': run.get('compilation', {}).get('errors', '').strip(),
                        'Runtime Error': run.get('runtime', {}).get('errors', '').strip(),
                        'Compilation Result': str(compilation_result),
                        'Runtime Result': str(runtime_result)
                    }
                else:
                    if run.get('compilation', {}).get('errors'):
                        aggregated_failing_tests[test_name]['Compilation Error'] += " | " + run.get('compilation', {}).get('errors', '').strip()
                    if run.get('runtime', {}).get('errors'):
                        aggregated_failing_tests[test_name]['Runtime Error'] += " | " + run.get('runtime', {}).get('errors', '').strip()
                    aggregated_failing_tests[test_name]['Compilation Result'] += " | " + str(compilation_result)
                    aggregated_failing_tests[test_name]['Runtime Result'] += " | " + str(runtime_result)

    detailed_df = pd.DataFrame(detailed_failing_tests)
    aggregated_df = pd.DataFrame(aggregated_failing_tests.values(), index=aggregated_failing_tests.keys()).reset_index().rename(columns={'index': 'Test Name'})
    
    return detailed_df, aggregated_df


json_file = 'results_gcc_13_2.json'
detailed_failing_tests_df, aggregated_failing_tests_df = extract_failing_tests(json_file)

excel_writer = pd.ExcelWriter('failing_tests_gcc_13_2.xlsx', engine='xlsxwriter')
detailed_failing_tests_df.to_excel(excel_writer, sheet_name='Detailed Failing Tests', index=False)
aggregated_failing_tests_df.to_excel(excel_writer, sheet_name='Aggregated Failing Tests', index=False)
excel_writer.close()  
