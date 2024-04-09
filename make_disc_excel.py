import json
import pandas as pd

compiler_name_1 = "nvc24.3"
compiler_name_2 = "cray17"

include_errors = True

def load_test_data(json_file):
    """
    Load test data from the JSON file, including both summary and detailed test results.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data['summary'], data['runs']

def compare_detailed_results(runs1, runs2, include_errors):
    """
    Compare detailed compilation and runtime results, optionally including only error messages.
    """
    discrepancies = []
    for test_name, runs in runs1.items():
        for index, run in enumerate(runs):
            if test_name in runs2 and len(runs2[test_name]) > index:
                comp_result1 = run.get('compilation', {}).get('result', -1)
                runtime_result1 = run.get('runtime', {}).get('result', -1)
                comp_result2 = runs2[test_name][index].get('compilation', {}).get('result', -1)
                runtime_result2 = runs2[test_name][index].get('runtime', {}).get('result', -1)

                row = [test_name, index + 1, comp_result1, runtime_result1, comp_result2, runtime_result2]

                if include_errors:
                    comp_errors1 = run.get('compilation', {}).get('errors', '')
                    runtime_errors1 = run.get('runtime', {}).get('errors', '')
                    comp_errors2 = runs2[test_name][index].get('compilation', {}).get('errors', '')
                    runtime_errors2 = runs2[test_name][index].get('runtime', {}).get('errors', '')
                    row.extend([comp_errors1, runtime_errors1, comp_errors2, runtime_errors2])

                discrepancies.append(row)

    return discrepancies

def generate_excel(detailed_discrepancies, output_file, include_errors):
    """
    Generate an Excel file with a sheet for 'Detailed Discrepancies', optionally including error messages.
    """
    columns = [
        'Test Name', 'Run Index', 
        f'{compiler_name_1} Compile Result', f'{compiler_name_1} Run Result', 
        f'{compiler_name_2} Compile Result', f'{compiler_name_2} Run Result'
    ]
    if include_errors:
        columns.extend([
            f'{compiler_name_1} Compile Errors', f'{compiler_name_1} Run Errors',
            f'{compiler_name_2} Compile Errors', f'{compiler_name_2} Run Errors'
        ])

    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        pd.DataFrame(detailed_discrepancies, columns=columns).to_excel(writer, sheet_name=f'{compiler_name_1} vs {compiler_name_2}', index=False)

json_file_compiler_1 = 'results_nvc_24_3.json'
json_file_compiler_2 = 'results_cray_17.json'
summary1, runs1 = load_test_data(json_file_compiler_1)
summary2, runs2 = load_test_data(json_file_compiler_2)

detailed_discrepancies = compare_detailed_results(runs1, runs2, include_errors)

generate_excel(detailed_discrepancies, 'compiler_discrepancies8.xlsx', include_errors)
