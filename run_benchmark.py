from __future__ import annotations
import json
from pathlib import Path
import typer
from rich import print
from src.reflexion_lab.agents import ReActAgent, ReflexionAgent
from src.reflexion_lab.reporting import build_report, save_report
from src.reflexion_lab.schemas import RunRecord
from src.reflexion_lab.utils import load_dataset, save_jsonl

app = typer.Typer(add_completion=False)


def _load_existing_records(path: Path) -> list[RunRecord]:
    if not path.exists():
        return []
    records: list[RunRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(RunRecord.model_validate_json(line))
    return records


def _run_agent_with_logs(agent, examples, agent_name: str, difficulty: str, total: int, qid_to_case: dict[str, int], log) -> list:
    records = []
    for example in examples:
        case_no = qid_to_case.get(example.qid, 0)
        log(f"[cyan]RUN[/cyan] agent={agent_name} difficulty={difficulty} case={case_no}/{total} qid={example.qid}")
        record = agent.run(example)
        records.append(record)
        log(
            f"[green]DONE[/green] agent={agent_name} difficulty={difficulty} qid={example.qid} "
            f"correct={record.is_correct} attempts={record.attempts} tokens={record.token_estimate} latency_ms={record.latency_ms}"
        )
    return records


def _run_split(examples, out_path: Path, reflexion_attempts: int, mode: str, log, resume: bool) -> None:
    react = ReActAgent()
    reflexion = ReflexionAgent(max_attempts=reflexion_attempts)

    difficulty = examples[0].difficulty if examples else "unknown"
    total = len(examples)
    qid_to_case = {example.qid: idx for idx, example in enumerate(examples, start=1)}

    react_file = out_path / "react_runs.jsonl"
    reflexion_file = out_path / "reflexion_runs.jsonl"

    existing_react_records = _load_existing_records(react_file) if resume else []
    existing_reflexion_records = _load_existing_records(reflexion_file) if resume else []

    existing_react_qids = {r.qid for r in existing_react_records}
    existing_reflexion_qids = {r.qid for r in existing_reflexion_records}

    pending_react = [e for e in examples if e.qid not in existing_react_qids]
    pending_reflexion = [e for e in examples if e.qid not in existing_reflexion_qids]

    if existing_react_records:
        log(f"[yellow]RESUME[/yellow] agent=react difficulty={difficulty} done={len(existing_react_records)} pending={len(pending_react)}")
    if existing_reflexion_records:
        log(f"[yellow]RESUME[/yellow] agent=reflexion difficulty={difficulty} done={len(existing_reflexion_records)} pending={len(pending_reflexion)}")

    new_react_records = _run_agent_with_logs(react, pending_react, "react", difficulty, total, qid_to_case, log) if pending_react else []
    new_reflexion_records = _run_agent_with_logs(reflexion, pending_reflexion, "reflexion", difficulty, total, qid_to_case, log) if pending_reflexion else []

    react_records = existing_react_records + new_react_records
    reflexion_records = existing_reflexion_records + new_reflexion_records
    all_records = react_records + reflexion_records

    save_jsonl(react_file, react_records)
    save_jsonl(reflexion_file, reflexion_records)
    report = build_report(all_records, dataset_name=out_path.name, mode=mode)
    json_path, md_path = save_report(report, out_path)
    log(f"[green]Saved[/green] {json_path}")
    log(f"[green]Saved[/green] {md_path}")
    log(json.dumps(report.summary, indent=2))

@app.command()
def main(
    dataset: str = "data/hotpot_mini.json",
    out_dir: str = "outputs/sample_run",
    reflexion_attempts: int = 3,
    resume: bool = typer.Option(True, "--resume/--no-resume"),
) -> None:
    examples = load_dataset(dataset)
    out_path = Path(out_dir)

    out_path.mkdir(parents=True, exist_ok=True)
    log_file = out_path / "run.log"

    def log(message: str) -> None:
        print(message)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(message + "\n")

    if log_file.exists() and not resume:
        log_file.unlink()

    log("=" * 72)
    log(f"[bold]Run start[/bold] resume={resume}")

    log(f"[bold]Dataset[/bold] {dataset}")
    log(f"[bold]Total examples[/bold] {len(examples)}")

    grouped = {"easy": [], "medium": [], "hard": []}
    for example in examples:
        grouped.setdefault(example.difficulty, [])
        grouped[example.difficulty].append(example)

    for difficulty in ["easy", "medium", "hard"]:
        split_examples = grouped.get(difficulty, [])
        if not split_examples:
            log(f"[yellow]SKIP[/yellow] difficulty={difficulty} reason=no examples")
            continue

        split_out = out_path / difficulty
        split_out.mkdir(parents=True, exist_ok=True)
        log(f"[bold]Start split[/bold] difficulty={difficulty} size={len(split_examples)}")
        _run_split(split_examples, split_out, reflexion_attempts, mode="ollama_remote", log=log, resume=resume)

    log("[bold]Completed all difficulty splits[/bold]")

if __name__ == "__main__":
    app()
