import importlib.util
import json
import xml.etree.ElementTree as ET

import yaml

class RuleInterpreter:
    """
    This is a second way of implementing rules from files and not via the Rule interface.
    """
    def __init__(self, filename):
        self.filename = filename
        self.functions = self.load_functions(filename)

    def load_functions(self, filename):
        file_extension = filename.split('.')[-1].lower()
        if file_extension == 'json':
            with open(filename, 'r') as file:
                return json.load(file)
        elif file_extension in ['yaml', 'yml']:
            with open(filename, 'r') as file:
                return yaml.safe_load(file)
        elif file_extension == 'py':
            return self.load_py_functions(filename)
        elif file_extension == 'xml':
            return self.load_xml_functions(filename)
        else:
            raise ValueError("Unsupported file format. Please provide a JSON, YAML, Python, or XML file.")

    @staticmethod
    def load_py_functions(filepath):
        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return {func: getattr(module, func) for func in dir(module) if callable(getattr(module, func))}

    @staticmethod
    def load_xml_functions(filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        functions = {}
        for func in root.findall('function'):
            name = func.get('name')
            logic = func.find('logic').text
            params = [param.text for param in func.find('parameters')]
            opt_params = {opt_param.tag: opt_param.text for opt_param in func.find('optional_parameters')}
            functions[name] = {'logic': logic, 'parameters': params, 'optional_parameters': opt_params}
        return functions

    def execute_all_functions(self, driver, matrix, i_car, j_car, tm):
        results = {}
        for function_name, function_data in self.functions.items():
            try:
                if isinstance(function_data, dict):
                    logic = compile(function_data['logic'], '', 'exec')
                    local_vars = {**locals().copy(), **function_data.get('optional_parameters', {})}
                    exec(logic, globals(), local_vars)
                    func = local_vars.get(function_name)
                else:
                    func = function_data

                if callable(func):
                    func_result = func(driver, matrix, i_car, j_car, tm)
                    results[function_name] = func_result if func_result is not None else "No return value"
            except Exception as e:
                results[function_name] = f"Error executing function: {e}"
                raise
        return results
