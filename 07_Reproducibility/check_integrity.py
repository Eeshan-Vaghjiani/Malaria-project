"""Check the downloaded pack before editing it. Uses Python's standard library."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'07_Reproducibility/file_manifest.json').read_text(encoding='utf-8'))
problems=[]
for item in manifest['files']:
    path=root/item['path']
    if not path.exists(): problems.append('Missing: '+item['path'])
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
        problems.append('Changed: '+item['path'])
if problems:
    print('\n'.join(problems))
    raise SystemExit('Files differ from the delivered snapshot. This is expected after deliberate edits; inspect the listed changes.')
print(f"Integrity check passed for {len(manifest['files'])} files.")
