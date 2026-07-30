from pypdf import PdfReader
import json 

DISPLAY_NAMES = {
    "sql": "SQL",
    "aws": "AWS",
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "github": "GitHub",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "postgresql": "PostgreSQL",
}


def resume_matcher():

    resume_text = extract_resume_skills()
    skills = load_skills()
    job_desc = get_job_desc()

    resume_skills = extract_skills(resume_text.lower(), skills)
    jd_skills = extract_skills(job_desc.lower(), skills)


    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    score = calculate_match_score(matched, jd_skills)

    display_report(score, matched, missing, jd_skills)


# to show skills properly, eg AWS might show as Aws, so this will help with that
def format_skill(skill):
    return DISPLAY_NAMES.get(skill, skill.title())


def display_report(score, matched, missing, jd_skills):

    print("\n" + "=" * 55)
    print("RESUME MATCH REPORT".center(55))
    print("=" * 55)

    # emojis give a nice touch tbh
    print(f"\n📊 Match Score : {score:.1f}% ({len(matched)}/{len(jd_skills)} skills matched)\n")
    if 85 <= score <= 100:
        print("🟢 Excellent Match")
    elif 70 <= score <= 84:
        print("🟡 Good Match  ")
    elif 50 <= score <= 69:
        print("🟠 Moderate Match ")
    elif score < 50:
        print("🔴 Low Match  ")


    print(f"✅ Matched Skills ({len(matched)})")
    print("-" * 55)

    if matched:
        for skill in sorted(matched):
            print(f"✓ {format_skill(skill)}")
    else:
        print("No matching skills found.")

    print()

    print(f"❌ Missing Skills ({len(missing)})")
    print("-" * 55)

    if missing:
        for skill in sorted(missing):
            print(f"✗ {format_skill(skill)}")
    else:
        print("None! Your resume covers every detected skill.")

    print("\n" + "=" * 55)

    input("Press Enter to return to menu...")


# having a fixed resume path is good   
def extract_resume_skills():
    reader = PdfReader("resume/NILESH_CHIDAMBARAM_Resume.pdf")

    # Loop through each page and print its content
    for index, page in enumerate(reader.pages):
        resume_text = page.extract_text()
    return resume_text


def get_job_desc():
    job_desc = input("Paste Job Description: \n")
    return job_desc


def load_skills():
    with open("skills.json", "r", encoding="utf-8") as file:
        skills = json.load(file)

    stored_skills = set(skills)
    return stored_skills


def extract_skills(text, stored_skills):
    extracted_skills = set()
    for skill in stored_skills:
        if skill in text:
            extracted_skills.add(skill)
    
    return extracted_skills

def calculate_match_score(matched, jd_skills):
    if not jd_skills:
        return 0

    return (len(matched) / len(jd_skills)) * 100

if __name__ == "__main__":
    resume_matcher()