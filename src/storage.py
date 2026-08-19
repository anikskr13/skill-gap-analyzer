import json
from pathlib import Path
from analyzer import GapReport

def save_report(gap_report: GapReport, file_name: str):
    Path("output").mkdir(exist_ok=True)

    file_path = Path("output") / file_name

    with open(file_path,"w", encoding="utf-8") as f:
        json.dump(gap_report.model_dump(), f, indent=4)

    print(f"Skill Gap Report saved -> {file_path}")

def load_report(file_name: str) -> GapReport:
    file_path = Path("output") / file_name
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return GapReport(**data)
