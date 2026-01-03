import typer
from .parsing import app as parsing_app
from .prototypes import app as proto_app
from .train import app as train_app
from .explain import app as explain_app
from .jdm import fetch_vocabulary

app = typer.Typer()

app.add_typer(parsing_app, name="parse")
app.add_typer(proto_app, name="rules")
app.add_typer(train_app, name="ml")
app.add_typer(explain_app, name="explain")

@app.command()
def cache(vocab_path: str, cache_dir: str, rel_id: int = 6, delay: float = 0.4):
    from pathlib import Path
    fetch_vocabulary(Path(vocab_path), Path(cache_dir), rel_id, delay)
