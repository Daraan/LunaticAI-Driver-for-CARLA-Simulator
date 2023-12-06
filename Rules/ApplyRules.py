import json
import random
import time


class RuleInterpreter:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.functions = json.load(file)

    def execute_all_functions(self, driver, matrix, i_car, j_car, tm):
        results = {}
        for function_name, function_data in self.functions.items():
            if 'logic' in function_data:
                logic = compile(function_data['logic'], '', 'exec')
                local_vars = locals().copy()
                exec(logic, globals(), local_vars)
                func_result = locals()[function_name](driver, matrix, i_car, j_car, tm)
                results[function_name] = func_result if func_result is not None else "No return value"
        return results
