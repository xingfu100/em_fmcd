"""Check syntax and English comments/docstrings without starting a GUI."""
import ast
import io
from pathlib import Path
import re
import tokenize

root = Path(__file__).resolve().parents[1]
for path in sorted((root / "src").glob("*.py")):
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT and re.search(r"[\u4e00-\u9fff]", token.string):
            raise AssertionError(f"Non-English comment: {path.name}:{token.start[0]}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if re.search(r"[\u4e00-\u9fff]", ast.get_docstring(node) or ""):
                raise AssertionError(f"Non-English docstring: {path.name}")
    print(f"PASS: {path.name}")
print("Syntax and Chinese-character comment checks passed; GUI behavior was not tested.")
