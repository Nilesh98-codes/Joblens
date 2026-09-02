import pytest
from project import JobApplication, load_json_file, save_json_file
import json



def test_job_application_valid():
    app = JobApplication(
        id= 1,
        company = "Google", 
        role = "SWE",
        location = "Mumbai", 
        date_applied= "2026-06-07",
        status= "Applied",
        job_link= "careers.google.com",
        notes= "Testing"
    )

    assert app.company == "Google"
    assert app.role == "SWE"
    assert app.location == "Mumbai"
    assert app.date_applied == "2026-06-07"
    assert app.status == "Applied"
    assert app.job_link == "careers.google.com"
    assert app.notes == "Testing"



def test_invalid_date():
        with pytest.raises(ValueError):
            JobApplication(
            id=1,
            company = "Google", 
            role = "SWE",
            location = "Mumbai", 
            date_applied= "2026-99-99",
            status= "Applied",
            job_link= "careers.google.com",
            notes= "Testing"
        )



        with pytest.raises(ValueError):
            JobApplication(
            id= 1,
            company = "Google", 
            role = "SWE",
            location = "Mumbai", 
            date_applied= "2026-99-99",
            status= "Hired",
            job_link= "careers.google.com",
            notes= "Testing"
        )



def test_from_dict():
    data = {
            "id": 1,
            "company": "Google",
            "role": "SWE",
            "location": "Mumbai",
            "date_applied": "2026-06-07",
            "status": "Applied",
            "job_link": "careers.google.com",
            "notes": "Testing"
    }

    app = JobApplication.from_dict(data)

    assert data["id"] == app.id
    assert data["company"] == app.company
    assert data["role"] == app.role
    assert data["location"] == app.location
    assert data["date_applied"] == app.date_applied
    assert data["status"] == app.status
    assert data["job_link"] == app.job_link
    assert data["notes"] == app.notes
    


def test_to_dict():
        app = JobApplication(
            id = 1,
            company = "Google", 
            role = "SWE",
            location = "Mumbai", 
            date_applied= "2026-06-07",
            status= "Applied",
            job_link= "careers.google.com",
            notes= "Testing"
    )

        expected_dict = {
            "id": 1,
            "company": "Google",
            "role": "SWE",
            "location": "Mumbai",
            "date_applied": "2026-06-07",
            "status": "Applied",
            "job_link": "careers.google.com",
            "notes": "Testing"
    }

        assert app.to_dict() == expected_dict

        
     
def test_load_json_missing_file(tmp_path):
      file = tmp_path / "missing.json"

      result = load_json_file(file)
      assert result == []
      


def test_save_json_file(tmp_path):
    file = tmp_path / "applications.json"

    app = JobApplication(
        id = 1,
        company = "Google", 
        role = "SWE",
        location = "Mumbai", 
        date_applied= "2026-06-07",
        status= "Applied",
        job_link= "careers.google.com",
        notes= "Testing"
    )

    expected = [app.to_dict()]
    applications = [app]
    
    save_json_file(file, applications)

    with open(file, "r") as f1:
          file1 = json.load(f1)

    assert file1 == expected

#new tests below

# ─── New tests: JobApplication validation & behavior ───────────────────
def test_invalid_status():
    """Constructor rejects a status not in STATUSES (the status-validation branch)."""
    with pytest.raises(ValueError, match="Invalid status"):
        JobApplication(
            id=1,
            company="Google",
            role="SWE",
            location="Mumbai",
            date_applied="2026-06-07",
            status="Hired",           # Hired is not in STATUSES
            job_link="careers.google.com",
            notes="Testing",
        )


def test_empty_required_fields_raise():
    """Constructor rejects empty company, role, or location."""
    base = dict(
        id=1,
        date_applied="2026-06-07",
        status="Applied",
        job_link="",
        notes="",
    )
    # empty company
    with pytest.raises(ValueError, match="cannot be empty"):
        JobApplication(company="", role="SWE", location="Mumbai", **base)

    # empty role
    with pytest.raises(ValueError, match="cannot be empty"):
        JobApplication(company="Google", role="", location="Mumbai", **base)

    # empty location
    with pytest.raises(ValueError, match="cannot be empty"):
        JobApplication(company="Google", role="SWE", location="", **base)


def test_wrong_date_format():
    """Constructor rejects a real date written in the wrong format (DD-MM-YYYY)."""
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        JobApplication(
            id=1,
            company="Google",
            role="SWE",
            location="Mumbai",
            date_applied="07-06-2026",   # DD-MM-YYYY instead of YYYY-MM-DD
            status="Applied",
            job_link="",
            notes="",
        )


def test_str_contains_key_fields():
    """__str__ includes company, role, location, and the appropriate status icon."""
    app = JobApplication(
        id=1,
        company="Google",
        role="SWE",
        location="Mumbai",
        date_applied="2026-06-07",
        status="Offer",
        job_link="careers.google.com",
        notes="Great opportunity",
    )
    text = str(app)
    assert "Google" in text
    assert "SWE" in text
    assert "Mumbai" in text
    assert "Offer" in text
    # Offer icon is 🎉 (\U0001f389)
    assert "\U0001f389" in text


def test_from_dict_to_dict_roundtrip():
    """from_dict(app.to_dict()) produces an object whose to_dict() matches the original."""
    app = JobApplication(
        id=42,
        company="Meta",
        role="ML Engineer",
        location="London",
        date_applied="2026-01-15",
        status="Interview",
        job_link="https://meta.com/careers",
        notes="Round 2 scheduled",
    )
    roundtripped = JobApplication.from_dict(app.to_dict())
    assert roundtripped.to_dict() == app.to_dict()


# ─── New tests: JSON persistence ────────────────────────────────────
def test_load_json_corrupt_file(tmp_path):
    """load_json_file returns [] when the file contains invalid JSON."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json!!", encoding="utf-8")

    result = load_json_file(bad_file)
    assert result == []


def test_save_load_roundtrip(tmp_path):
    """save_json_file then load_json_file on the same path produces equivalent objects."""
    filepath = tmp_path / "apps.json"
    app = JobApplication(
        id=1,
        company="Amazon",
        role="SDE",
        location="Seattle",
        date_applied="2026-03-20",
        status="Applied",
        job_link="https://amazon.jobs",
        notes="Referral",
    )
    save_json_file(filepath, [app])
    loaded = load_json_file(filepath)

    assert len(loaded) == 1
    assert loaded[0].to_dict() == app.to_dict()


def test_save_load_multiple_applications(tmp_path):
    """Round-trip with 3 applications preserves count, order, and all field values."""
    filepath = tmp_path / "multi.json"
    apps = [
        JobApplication(id=1, company="Google", role="SWE", location="NYC",
                       date_applied="2026-01-01", status="Applied",
                       job_link="", notes=""),
        JobApplication(id=2, company="Meta", role="PM", location="London",
                       date_applied="2026-02-15", status="Interview",
                       job_link="", notes="Phone screen"),
        JobApplication(id=3, company="Apple", role="Designer", location="Cupertino",
                       date_applied="2026-03-10", status="Rejected",
                       job_link="", notes=""),
    ]
    save_json_file(filepath, apps)
    loaded = load_json_file(filepath)

    assert len(loaded) == 3
    for original, reloaded in zip(apps, loaded):
        assert reloaded.to_dict() == original.to_dict()


def test_save_overwrites_existing_file(tmp_path):
    """Saving a new list fully replaces old file content (no append)."""
    filepath = tmp_path / "overwrite.json"

    first = [JobApplication(id=1, company="OldCo", role="Old", location="Old",
                            date_applied="2026-01-01", status="Applied",
                            job_link="", notes="")]
    save_json_file(filepath, first)

    second = [JobApplication(id=99, company="NewCo", role="New", location="New",
                             date_applied="2026-06-01", status="Offer",
                             job_link="", notes="")]
    save_json_file(filepath, second)

    loaded = load_json_file(filepath)
    assert len(loaded) == 1
    assert loaded[0].company == "NewCo"
    assert loaded[0].id == 99


# ─── New tests: resume_matcher pure-logic functions ───────────────────
from resume_matcher import extract_skills, calculate_match_score, format_skill



def test_extract_skills():
    """extract_skills finds matching skills in text and returns empty set for no matches."""
    skills_db = {"python", "docker", "react", "sql"}

    # positive case: text contains some skills
    text = "experienced with python and docker, familiar with linux"
    found = extract_skills(text, skills_db)
    assert found == {"python", "docker"}

    # negative case: text has no overlap with skill set
    text_none = "project management and leadership"
    found_none = extract_skills(text_none, skills_db)
    assert found_none == set()


def test_calculate_match_score():
    """Score is (matched/jd_skills)*100; returns 0 when jd_skills is empty."""
    # normal case
    matched = {"python", "sql"}
    jd_skills = {"python", "sql", "react", "docker"}
    assert calculate_match_score(matched, jd_skills) == 50.0

    # perfect match
    assert calculate_match_score(jd_skills, jd_skills) == 100.0

    # empty JD (division-by-zero guard)
    assert calculate_match_score(set(), set()) == 0


def test_format_skill():
    """format_skill returns DISPLAY_NAMES entry for abbreviations, .title() for others."""
    # known abbreviations
    assert format_skill("sql") == "SQL"
    assert format_skill("aws") == "AWS"
    assert format_skill("html") == "HTML"
    assert format_skill("javascript") == "JavaScript"

    # unknown skill falls back to .title()
    assert format_skill("flask") == "Flask"
    assert format_skill("docker") == "Docker"
