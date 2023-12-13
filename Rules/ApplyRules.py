import builtins
import importlib
import json


class RuleInterpreter:
    def __init__(self, filename):
        self.functions = self.load_functions(filename)
        self.load_required_imports()

    def load_required_imports(self):
        required_imports = self.functions.pop("required_imports", [])
        for name in required_imports:
            setattr(builtins, name, importlib.import_module(name))

    @staticmethod
    def load_functions(filename):
        file_extension = filename.split('.')[-1].lower()
        if file_extension == 'json':
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            raise ValueError("Unsupported file format. Please provide a JSON file.")

    def execute_all_functions(self, driver, matrix, i_car, j_car, tm):
        results = {}
        for function_name, function_data in self.functions.items():
            try:
                logic = compile(function_data['logic'], '', 'exec')
                local_vars = {**locals().copy(), **function_data.get('optional_parameters', {})}
                exec(logic, globals(), local_vars)
                func = local_vars.get(function_name)
                if callable(func):
                    func_result = func(driver, matrix, i_car, j_car, tm)
                    results[function_name] = func_result if func_result is not None else "No return value"
            except Exception as e:
                results[function_name] = f"Error executing function: {e}"
        return results
