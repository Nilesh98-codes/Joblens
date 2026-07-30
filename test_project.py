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

           