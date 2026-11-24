
import ast
import os
import re


class SourceAuditor:

    def __init__(self, target_path: str, /) -> None:
        self.target_path = target_path

    @property
    def target_path(self) -> str:
        return self._target_path

    @target_path.setter
    def target_path(self, value: str) -> None:
        if not os.path.exists(value):
            raise FileNotFoundError(
                f"Target path '{value}' does not exist."
            )
        self._target_path = value

    def audit_module_structure(
        self,
        file_contents: str,
        /,
        *,
        max_line_length: int = 79
    ) -> dict:

        tree = ast.parse(file_contents)

        # Requirement 1: top-level function spacing
        spacing_violations = []

        functions = [
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
        ]

        for i in range(len(functions) - 1):
            first = functions[i]
            second = functions[i + 1]

            if second.decorator_list:
                start_line = second.decorator_list[0].lineno
            else:
                start_line = second.lineno

            blank_lines = start_line - first.end_lineno - 1

            if blank_lines < 2:
                spacing_violations.append(second.name)

        # Requirement 2: line rules
        lines = file_contents.splitlines()

        line_length_violations = []
        trailing_whitespace_violations = []
        colon_spacing_violations = []

        for line_number, line in enumerate(lines, start=1):

            # Line length
            if len(line) > max_line_length:
                line_length_violations.append(line_number)

            # Trailing whitespace
            if line.strip() and re.search(r"[ \t]+$", line):
                trailing_whitespace_violations.append(line_number)

            # Annotation colon without following space
            if re.search(r"\w+:\w", line):
                colon_spacing_violations.append(line_number)

        return {
            "spacing_violations": spacing_violations,
            "line_length_violations": line_length_violations,
            "trailing_whitespace_violations":
                trailing_whitespace_violations,
            "colon_spacing_violations":
                colon_spacing_violations
        }

    def verify_sdist_layout(
        self,
        directory_path: str,
        /
    ) -> bool:

        # Directory must exist
        if not os.path.isdir(directory_path):
            return False

        # Required files
        setup_path = os.path.join(directory_path, "setup.py")
        readme_path = os.path.join(directory_path, "README.txt")

        if not os.path.isfile(setup_path):
            return False

        if not os.path.isfile(readme_path):
            return False

        # Read setup.py
        with open(setup_path, encoding="utf-8") as file:
            setup_source = file.read()

        try:
            tree = ast.parse(setup_source)
        except SyntaxError:
            return False

        # Find py_modules = [...]
        module_names = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id == "py_modules"
                        and isinstance(node.value, (ast.List, ast.Tuple))
                    ):
                        for item in node.value.elts:
                            if isinstance(item, ast.Constant):
                                module_names.append(item.value)

        # At least one module must exist
        for module_name in module_names:
            module_file = os.path.join(
                directory_path,
                module_name + ".py"
            )

            if os.path.isfile(module_file):
                return True

        return False


if __name__ == "__main__":
    assert not SourceAuditor(__file__).audit_module_structure(
        open(__file__, encoding="utf-8").read()
    )["spacing_violations"], \
        "Self-audit failed: spacing violations found."

    print(
        "Self-audit passed: no top-level function spacing violations."
    )
if __name__ == "__main__":
    auditor = SourceAuditor(__file__)

    print(
        auditor.verify_sdist_layout(
            "test_package"
        )
    )
