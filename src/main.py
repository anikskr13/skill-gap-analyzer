# =================================================================
# IMPORTS AND ENCODING FIX
# =================================================================

import sys
sys.stdout.reconfigure(encoding="utf-8")  # fix emoji rendering on Windows

import argparse
from pathlib import Path
from extractor import read_document, parse_resume, parse_job_description
from analyzer import compare, GapReport
from storage import save_report


# =================================================================
# CLI ARGUMENT PARSER
# =================================================================

def get_args():
    parser = argparse.ArgumentParser(description="Skill Gap Analyzer")
    parser.add_argument("--resume", type=str, help="Path to resume file (PDF/DOCX)")
    parser.add_argument("--skills", type=str, help="comma separated skills")
    parser.add_argument("--jd", type=str, help="Path to JD file")
    return parser.parse_args()


# =================================================================
# FORMATTED TERMINAL OUTPUT
# =================================================================

def print_report(report: GapReport):
    print("\n============================================")
    print("         SKILL GAP ANALYSIS REPORT")
    print("============================================")
    print(f"Candidate  : {report.candidate_name or 'Unknown'}")
    print(f"Target Role: {report.target_role or 'Unknown'}")

    print("\nMatched Skills:")
    for skill in report.matched_skills:
        print(f"  ✅ {skill}")

    print("\nMissing Skills:")
    for gap in report.gaps:
        print(f"  ❌ [{gap.priority.upper()}]  {gap.skill_name} — {gap.reason}")

    print(f"\nExperience Gap : {report.experience_gap or 'Not specified'}")
    print(f"Verdict        : {report.verdict}")
    print("============================================\n")


# =================================================================
# MAIN — orchestrates extract → analyze → save → print
# =================================================================

def main():
    args = get_args()

    # --- Get JD text ---
    if not args.jd:
        args.jd = input("Enter path to JD file: ").strip()
    jd_path = Path(args.jd)
    if not jd_path.exists():
        print(f"Error: File not found: {jd_path}")
        return
    jd_text = read_document(jd_path)

    # --- Get resume text ---
    if args.skills:
        resume_text = f"Skills: {args.skills}"
    elif args.resume:
        resume_path = Path(args.resume)
        if not resume_path.exists():
            print(f"Error: File not found: {resume_path}")
            return
        resume_text = read_document(resume_path)
    else:
        choice = input("Enter resume file path OR type your skills manually: ").strip()
        if Path(choice).exists():
            resume_text = read_document(Path(choice))
        else:
            resume_text = f"Skills: {choice}"

    # --- Extract ---
    candidate = parse_resume(resume_text)
    role = parse_job_description(jd_text)

    # --- Analyze ---
    report = compare(candidate, role, jd_text)

    # --- Save ---
    filename = f"{candidate.name or 'candidate'}_{role.role_name or 'role'}.json".replace(" ", "_")
    save_report(report, filename)

    # --- Print ---
    print_report(report)


# =================================================================
# ENTRY POINT
# =================================================================

if __name__ == "__main__":
    main()
