import ast
import importlib.util
import sys

from flask import request


def verify_imports(script_path):
    allowed_modules = {'requests', 'json'}

    with open(script_path, 'r') as file:
        tree = ast.parse(file.read())

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ''
            for alias in node.names:
                imports.add(module + '.' + alias.name)

    result = imports - allowed_modules

    if not len(result) == 0:
        raise Exception(f'You are not allowed to import {result}')


class ScriptLoader:
    __module = None

    def is_loaded(self) -> bool:
        return self.__module is not None

    def load_script(self, path: str, module_name: str | None = None) -> tuple[bool, str]:
        try:
            verify_imports(path)
            spec = importlib.util.spec_from_file_location(module_name, path)
            self.__module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = self.__module
            spec.loader.exec_module(self.__module)
            return True, ''

        except Exception as e:
            print(f'Error: {e}')
            return False, str(e)

    def unloadScript(self):
        self.__module = None

    def quitScript(self):
        self.__module = None
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def get_home_page(self):
        module = self.__module
        res = module.home_page('https://www.google.com')
        return res
