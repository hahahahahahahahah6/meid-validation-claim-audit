"""Offline documentation and Python source inspection."""
import ast
import os
import re
from pathlib import Path

from .phrases import GENERIC_NAMES, MEIDVALIDATION, NOMEIDVALIDATION


def normalize(text):
    text = text.lower().replace("n't", " not").replace('-', ' ')
    return ' '.join(text.split())


def _patterns(phrases):
    return [(p, re.compile(r'(?<!\w)' + re.escape(p) + r'(?!\w)'))
            for p in sorted(phrases, key=lambda x: (-len(x), x))]

YES = _patterns(MEIDVALIDATION)
NO = _patterns(NOMEIDVALIDATION)


def documentation_claims(text):
    lines = []
    fence = None
    for line in text.splitlines():
        m = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line[m.end():].strip():
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        lines.append(line)
    yes = no = False
    for paragraph in re.split(r'\n\s*\n', '\n'.join(lines)):
        normalized = normalize(paragraph)
        for _, pattern in NO:
            normalized, count = pattern.subn(' ', normalized)
            no |= bool(count)
        yes |= any(pattern.search(normalized) for _, pattern in YES)
    return yes, no


def source_evidence(source):
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return False
    imports = {}
    bound = set()
    definitions = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split('.')[0]
                imports[name] = alias.name if alias.asname else alias.name.split('.')[0]
                if alias.name == 'stdnum.meid' and not alias.asname:
                    imports[name] = 'stdnum'
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            for alias in node.names:
                imports[alias.asname or alias.name] = (node.module or '') + '.' + alias.name
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                bound.update(x.id for x in ast.walk(target) if isinstance(x, ast.Name))
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars:
                    bound.update(x.id for x in ast.walk(item.optional_vars) if isinstance(x, ast.Name))
    shadow = bound | definitions

    def resolve(node):
        if isinstance(node, ast.Name):
            return imports.get(node.id, '') if node.id not in shadow else ''
        if isinstance(node, ast.Attribute):
            base = resolve(node.value)
            return base + '.' + node.attr if base else ''
        return ''

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if isinstance(fn, ast.Name):
            target = resolve(fn)
            if target in ('stdnum.meid.validate', 'stdnum.meid.is_valid'):
                return True
            if target and target.rsplit('.', 1)[-1] in GENERIC_NAMES and target.rsplit('.', 1)[-1] not in definitions:
                return True
        elif isinstance(fn, ast.Attribute):
            root = fn.value
            while isinstance(root, ast.Attribute):
                root = root.value
            if isinstance(root, ast.Name) and root.id in imports and root.id in shadow:
                continue
            if fn.attr in GENERIC_NAMES and fn.attr not in definitions:
                return True
            if fn.attr in ('validate', 'is_valid') and resolve(fn.value) == 'stdnum.meid':
                return True
    return False


def audit(root, ignore=()):
    root = Path(root)
    if root.is_symlink() or not root.is_dir() or not os.access(str(root), os.R_OK | os.X_OK):
        raise OSError('root is not a readable directory: ' + str(root))
    prefixes = [str(x).replace('\\', '/').strip('/') for x in ignore]
    def ignored(rel):
        return any(rel == x or rel.startswith(x + '/') for x in prefixes if x)
    yes = no = prod = test = False
    for directory, dirs, files in os.walk(str(root), followlinks=False, onerror=lambda e: (_ for _ in ()).throw(e)):
        base = Path(directory)
        dirs[:] = [d for d in dirs if not (base / d).is_symlink() and not ignored((base / d).relative_to(root).as_posix())]
        for name in files:
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() or ignored(rel):
                continue
            parts = path.relative_to(root).parts
            if (rel == 'README.md' or ('docs' in parts[:-1] and path.suffix == '.md')):
                a, b = documentation_claims(path.read_text(encoding='utf-8'))
                yes |= a
                no |= b
            if path.suffix != '.py' or any(x in parts[:-1] for x in ('fixtures', 'docs', 'examples')):
                continue
            evidence = source_evidence(path.read_text(encoding='utf-8'))
            is_test = 'tests' in parts[:-1] or name.startswith('test_') or name.endswith('_test.py')
            if is_test:
                test |= evidence
            else:
                prod |= evidence
    findings = []
    if yes and not prod:
        findings.append({'id': 'documented-meid-validation-claim-false', 'severity': 'MEDIUM' if test else 'HIGH', 'message': 'Documented claim has ' + ('test-only' if test else 'no production') + ' evidence.'})
    if no and prod:
        findings.append({'id': 'documented-no-meid-validation-claim-false', 'severity': 'HIGH', 'message': 'Documented denial conflicts with production evidence.'})
    return findings
