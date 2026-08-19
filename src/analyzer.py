# =================================================================
# IMPORTS
# =================================================================

from extractor import CandidateProfile, RoleRequirements
from pydantic import BaseModel


# =================================================================
# PYDANTIC MODELS
# =================================================================

class SkillGap(BaseModel):
    skill_name: str
    priority: str       # "Critical" | "Important" | "Nice-to-have"
    reason: str         # why this priority was assigned


class GapReport(BaseModel):
    candidate_name: str | None
    target_role: str | None
    matched_skills: list[str]
    gaps: list[SkillGap]
    experience_gap: str | None
    verdict: str


# =================================================================
# PRIORITY RANKING — deterministic Python logic, no LLM
# =================================================================

def assign_priority(skill: str, required_skills: list[str], preferred_skills: list[str], jd_text: str) -> str:
    skill_lower = skill.lower()
    jd_lower = jd_text.lower()

    frequency = jd_lower.count(skill_lower)
    is_required = skill_lower in [s.lower() for s in required_skills]
    is_preferred = skill_lower in [s.lower() for s in preferred_skills]

    if is_required and frequency >= 2:
        return "Critical"
    elif is_required and frequency < 2:
        return "Important"
    elif is_preferred and frequency >= 2:
        return "Important"
    else:
        return "Nice-to-have"


# =================================================================
# EXPERIENCE GAP CHECK
# =================================================================

def check_experience_gap(candidate: CandidateProfile, role: RoleRequirements) -> str | None:
    if candidate.experience_years is None or role.min_experience is None:
        return None

    gap = role.min_experience - candidate.experience_years

    if gap <= 0:
        return "Meets requirement"
    else:
        return f"You have {candidate.experience_years} yr(s). Role needs {role.min_experience} yr(s). Gap: {gap} yr(s)."


# =================================================================
# VERDICT GENERATION
# =================================================================

def generate_verdict(matched_skills: list[str], gaps: list[SkillGap]) -> str:
    if len(gaps) == 0:
        return "Strong fit — no skill gaps found."

    critical_count = sum(1 for g in gaps if g.priority == "Critical")

    if critical_count == 0:
        return "Good fit — only minor gaps."
    else:
        return f"Partial fit — missing {critical_count} critical skill(s)."


# =================================================================
# MAIN COMPARISON — ties everything together
# =================================================================

def compare(candidate: CandidateProfile, role: RoleRequirements, jd_text: str) -> GapReport:

    # Step 1 — normalize candidate skills
    candidate_skills_lower = [s.lower() for s in candidate.skills]

    # Step 2 — all role skills combined
    all_role_skills = role.required_skills + role.preferred_skills

    # Step 3 — matched skills (candidate HAS them)
    matched_skills = [
        s for s in candidate.skills
        if s.lower() in [r.lower() for r in all_role_skills]
    ]

    # Step 4 — missing skills (role needs them, candidate DOESN'T have them)
    missing_skills = [
        s for s in all_role_skills
        if s.lower() not in candidate_skills_lower
    ]

    # Step 5 — build SkillGap list
    gaps = []
    for skill in missing_skills:
        priority = assign_priority(skill, role.required_skills, role.preferred_skills, jd_text)
        skill_lower = skill.lower()
        frequency = jd_text.lower().count(skill_lower)
        if skill_lower in [s.lower() for s in role.required_skills]:
            classification = "Required skill"
        else:
            classification = "Preferred skill"
        reason = f"{classification}, mentioned {frequency}x in JD."
        gaps.append(SkillGap(skill_name=skill, priority=priority, reason=reason))

    # Step 6 — experience + verdict
    experience_gap = check_experience_gap(candidate, role)
    verdict = generate_verdict(matched_skills, gaps)

    # Step 7 — return final report
    return GapReport(
        candidate_name=candidate.name,
        target_role=role.role_name,
        matched_skills=matched_skills,
        gaps=gaps,
        experience_gap=experience_gap,
        verdict=verdict
    )
