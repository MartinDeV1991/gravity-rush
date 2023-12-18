import ast

class NodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_stack = []
        self.indentation = 0

    def print_with_indentation(self, text):
        print(' ' * self.indentation + text)

    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.print_with_indentation(f'Class {node.name}:')
        self.indentation += 4
        self.generic_visit(node)
        self.indentation -= 4
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self.print_with_indentation(f'Def {node.name}():')
        self.indentation += 4
        self.generic_visit(node)
        self.indentation -= 4

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'self':
                method_name = node.func.attr
                if len(self.class_stack) > 0:
                    class_name = self.class_stack[-1]
                    self.print_with_indentation(f'Calling {class_name}.{method_name}()')
        self.generic_visit(node)

def process_file(filename):
    with open(filename, 'r') as f:
        code = f.read()
        tree = ast.parse(code)

    visitor = NodeVisitor()
    visitor.visit(tree)

def print_class_structure(file_list):
    for filename in file_list:
        print(f'File: {filename}')
        process_file(filename)
        print()

file_list = ['entities.py', 'projectile.py']
print_class_structure(file_list)
