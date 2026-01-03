from __future__ import annotations
import json
from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def explain_feature(index: int, rules_dir: Path):
    # concat règles dans l’ordre alphabétique
    all_rules = []
    offsets = []
    start = 0
    for fp in sorted(rules_dir.glob("*_rules.json"), key=lambda p: p.name):
        label = fp.stem.replace("_rules","")
        rules = json.loads(fp.read_text(encoding="utf-8"))
        offsets.append((label, start, start + len(rules) - 1, fp))
        start += len(rules)
        all_rules.extend(rules)

    for label, a, b, fp in offsets:
        if a <= index <= b:
            local = index - a
            rule = json.loads(Path(fp).read_text(encoding="utf-8"))[local]
            typer.echo(f"Feature #{index} -> {label} (local {local}, file {fp.name})")
            typer.echo(json.dumps(rule, ensure_ascii=False, indent=2))
            return

    typer.echo("Index hors plage.")
