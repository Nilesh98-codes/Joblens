import os
import json
from datetime import datetime
from pypdf import PdfReader
from matplotlib import pyplot as plt
from resume_matcher import resume_matcher
from ui import (
    console, prompt, wait_for_enter,
    print_success, print_error, print_warning, print_info,
    print_welcome, print_main_menu, print_exit,
    print_app_table, print_app_detail,
    print_section_header, print_status_select,
    print_search_menu, print_statistics_menu,
    print_statistics_dashboard,
    STATUS_STYLE,
)


STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview",
    "Offer",
    "Rejected"
]

# for a bit of personality, it looks too bland with just text
STATUS_ICONS = {
    "Applied": "\U0001f4dd",
    "Online Assessment": "\U0001f4bb",
    "Interview": "\U0001f4bc",
    "Offer": "\U0001f389",
    "Rejected": "\u274c"
}

class JobApplication:
    def __init__(self, id, company, role, location, date_applied, status , job_link, notes):
        self.id = id
        if not company or not role or not location:
            raise ValueError("Company, role, and location cannot be empty.") 
        self.company = company
        self.role = role
        self.location = location

        try:
            datetime.strptime(date_applied, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        self.date_applied = date_applied

        if status not in STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {STATUSES}")
        self.status = status
        self.job_link = job_link
        self.notes = notes

        
    def __str__(self):
        icon = STATUS_ICONS.get(self.status, "")
        return (
    # the comment with = below is to make it easier to see the table, below one is better for modification
    # f"\n========================================\n"
    f"{'-' * 18}\n"
    f"\U0001f4c4 Application #{self.id}\n"
    f"Company      : {self.company}\n"
    f"Role         : {self.role}\n"
    f"Location     : {self.location}\n"
    f"\nDate Applied : {self.date_applied}\n"
    f"Status       : {icon} {self.status}\n"

    f"\nJob Link     : {self.job_link}\n"

    f"\nNotes: \n{self.notes}\n"
    f"{'-' * 18}\n"
    # f"\n========================================\n"
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "location": self.location,
            "date_applied": self.date_applied,
            "status": self.status,
            "job_link": self.job_link,
            "notes": self.notes,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            company=data["company"],
            role=data["role"],
            location=data["location"],
            date_applied=data["date_applied"],
            status=data["status"],
            job_link=data["job_link"],
            notes=data["notes"]
        )


def main():

    while True:
        print_welcome()
        print_main_menu()

        option = prompt("Enter your choice (1-8)")


        # new application
        if option == "1":
            add_application()
            
        elif option == "2":
            view_application()

        elif option == "3":
            update_status()

        elif option == "4":
            delete_application()
           
        elif option == "5":
            search_application()
            
        elif option == "6":
            show_statistics()

        elif option == "7":
            resume_matcher()

        elif option == "8" or option == "q" or option == "Q":
            # just break out of the loop
            print_exit()
            break


def save_json_file(filename, data):
    with open(filename, "w") as file:
        obj = [item.to_dict() for item in data]
        json.dump(obj, file, indent=4)


def load_json_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [JobApplication.from_dict(item) for item in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print_error(f"Failed to decode JSON from {filename}.")
        return []


def add_application():
    applications = load_json_file("applications.json")
    if applications:
        next_id = max(app.id for app in applications) + 1
    else:
        next_id = 1
        
    print_section_header("Add Application")

    company = prompt("Enter company name").title().strip()
    role = prompt("Enter role").title().strip()
    location = prompt("Enter location").title().strip()
    date_applied = prompt("Enter date applied (YYYY-MM-DD)")
    status = prompt("Enter status (Applied, Online Assessment, Interview, Offer, Rejected)").strip().title()
    job_link = prompt("Enter job link")
    notes = prompt("Enter notes").strip()

    try: 
        application = JobApplication(
            id=next_id,
            company=company,
            role=role,
            location=location,
            date_applied=date_applied,
            status=status,
            job_link=job_link,
            notes=notes
        )
        applications.append(application)
        save_json_file("applications.json", applications)
        print_success("Application added successfully!")

    except ValueError as e:
        print_error(str(e))
    
    wait_for_enter()


def view_application():
    applications = load_json_file("applications.json")
    if not applications:
        print_warning("No applications found")
        return
    
    # the short list of jobs will show here
    print_section_header("View Applications")
    print_app_table(applications)

    # Prompt user for detailed view
    try:
        choose = int(prompt("Enter application ID to view details"))
    except ValueError:
        print_error("Invalid input. Please enter a valid numerical ID.")
    else:
        console.print()
        # this will show a detailed window of the application
        matched_app = next((app for app in applications if app.id == choose), None)
        
        if matched_app:
            print_app_detail(matched_app)
        else:
            print_warning("Application not found")

    # Go back to menu
    wait_for_enter()


def update_status():
    applications = load_json_file("applications.json")
    if not applications:
            print_warning("No applications found")
            return
        
    # the short view of job applications
    print_section_header("Update Status")
    print_app_table(applications)

    update = int(prompt("Enter application ID to update"))
    found = False

    for app in applications:
        icon = STATUS_ICONS.get(app.status)
        if update == app.id:
            found = True
            style = STATUS_STYLE.get(app.status, "white")
            print_info(f"Current Status: [{style}]{icon} {app.status}[/]")

            print_status_select(STATUSES)

            try:
                choice = int(prompt("Choice"))

                # Validate the user's input
                if 1 <= choice <= len(STATUSES):
                    selected_status = STATUSES[choice - 1]
                    app.status = selected_status
                    print_success(f"Successfully updated status to: {selected_status}")
                    save_json_file("applications.json", applications)
                    return 
                else:
                    print_error("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print_error("Invalid input. Please enter a valid number.")
            wait_for_enter()
            
    if not found:
        print_warning("Application not found")
        wait_for_enter()
        return

def delete_application():
    applications = load_json_file("applications.json")
    if not applications:
            print_warning("No applications found")
            return
        
    # the short view of job applications
    print_section_header("Delete Application")
    print_app_table(applications)

    try:
        delete = int(prompt("Enter application ID to delete"))
        for app in applications:
            if delete == app.id:
                applications.remove(app)
                save_json_file("applications.json", applications)
                print_success("Application successfully deleted")
                return 
        print_warning("Application does not exist")

    except ValueError:
            print_error("Invalid input. Please enter a valid number.")

    
def search_application():
    applications = load_json_file("applications.json")
    while True:

        print_section_header("Search Applications")
        print_search_menu()

        choice = prompt("Enter choice")
        if choice == "1":
            print_section_header("Search By Company")

            search_company = prompt("Enter Company").lower()
            match = False
            for app in applications:
                if app.company.lower().startswith(search_company):
                    match = True
                    print_app_detail(app)
            if not match:
                print_warning("Company not found")

        if choice == "2":
            print_section_header("Search by Role")

            search_role = prompt("Enter Role").lower()
            match = False
            for app in applications:
                if app.role.lower().startswith(search_role):
                    match = True
                    print_app_detail(app)
            if not match:
                print_warning("Role not found")
            
        if choice == "3":
            print_section_header("Search by Location")
            
            search_location = prompt("Enter Location").lower()
            match = False
            for app in applications:
                if app.location.lower().startswith(search_location):
                    match = True
                    print_app_detail(app)
            if not match:
                print_warning("Applications in given location not found")

        if choice == "4":
            print_section_header("Search by Status")
            
            search_status = prompt("Enter Status").lower()
            match = False
            for app in applications:
                if app.status.lower().startswith(search_status):
                    match = True
                    print_app_detail(app)
            if not match:
                print_warning("Status not found")
        if choice == "5":
            break
                

def show_statistics():
    applications = load_json_file("applications.json")

    print_section_header("Statistics")
    print_statistics_menu()
    
    try:
        choice = int(prompt("Enter your choice"))
    except ValueError:
        print_error("Invalid input. Please enter a valid number.")
        return

    # build tracking dictionary dynamically
    track = {status: 0 for status in STATUSES}

    # count each status
    for app in applications:
        if app.status in track:
            track[app.status] += 1

    # FOR THE TERMINAL STATS
    if 1 <= choice <= 3 and choice == 1:
        total = len(applications)
        print_statistics_dashboard(track, total)
        wait_for_enter()
    

    # FOR THE VISUAL CHART
    elif 1 <= choice <= 3 and choice == 2:

        # remove statuses with 0 applications
        filtered = {}
        for status, count in track.items():
            if count > 0:
                filtered[status] = count

        statuses = list(filtered.keys())
        counts = list(filtered.values())

        # consistent colors for each status
        status_colors = {
            "Applied": "#42A5F5",             
            "Online Assessment": "#FFCA28",   
            "Interview": "#AB47BC",           
            "Offer": "#66BB6A",               
            "Rejected": "#EF5350"             
        }

        # store the colors of each status so that each status bar has its appropiate color
        colors = []
        for status in statuses:
            colors.append(status_colors[status])

        plt.figure(figsize=(7, 5))

        bars = plt.bar(
            statuses,
            counts,
            width=0.25,
            color=colors,
            edgecolor="black",
            linewidth=1
        )

        plt.title("JobLens - Application Statistics", fontsize=18)
        plt.xlabel("Application Status", fontsize=12)
        plt.ylabel("Applications", fontsize=12)

        # light grid
        plt.grid(axis="y", linestyle="--", alpha=0.25)

        # add some headroom
        plt.ylim(0, max(counts) + 0.7)

        # display values above bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.05,
                str(int(height)),
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold"
            )

        # a bit of slight rotation looks cleaner, neat right?
        plt.xticks(rotation=10)

        plt.tight_layout()

        os.makedirs("charts", exist_ok=True)
        plt.savefig("charts/job_statistics.png", dpi=300)
        plt.show()
        print_info("Chart saved as charts/job_statistics.png")

        

if __name__ == "__main__":
    main()