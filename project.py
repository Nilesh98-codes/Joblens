import os
import json
from datetime import datetime
from pypdf import PdfReader
from matplotlib import pyplot as plt
from resume_matcher import resume_matcher


STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview",
    "Offer",
    "Rejected"
]

# for a bit of personality, it looks too bland with just text
STATUS_ICONS = {
    "Applied": "📝",
    "Online Assessment": "💻",
    "Interview": "💼",
    "Offer": "🎉",
    "Rejected": "❌"
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
    f"📄 Application #{self.id}\n"
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
        print()
        print("=" * 60)
        print("JobLens".center(60))
        print("Job Application Tracker".center(60))
        print("=" * 60)

        print("\nChoose an option:\n")

        print("1. Add Application")
        print("2. View Applications")
        print("3. Update Status")
        print("4. Delete Application")
        print("5. Search Applications")
        print("6. Statistics")
        print("7. Resume Matcher")
        print("8. Exit (Press Q or 8)")

        print("\n" + "=" * 60)

        option = input("Enter your choice (1-8): ")


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
        print(f"Error: Failed to decode JSON from {filename}.")
        return []


def add_application():
    applications = load_json_file("applications.json")
    if applications:
        next_id = max(app.id for app in applications) + 1
    else:
        next_id = 1
        
    
    company = input("Enter company name: ").title().strip()
    role = input("Enter role: ").title().strip()
    location = input("Enter location: ").title().strip()
    date_applied = input("Enter date applied (YYYY-MM-DD): ")
    status = input("Enter status (Applied, Online Assessment, Interview, Offer, Rejected): ").strip().title()
    job_link = input("Enter job link: ")
    notes = input("Enter notes: ").strip()

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
        print(f" ✓ Application added successfully!")

    except ValueError as e:
        print(f"Error: {e}") 
    
    input("\nPress Enter to return to the main menu...")


def view_application():
    applications = load_json_file("applications.json")
    if not applications:
        print("No applications found")
        return
    
    # the short list of jobs will show here
    print("=" * 70)
    print(f"{'ID':<5}{'Company':<20}{'Role':<20}{'Status':<15}")
    print("-" * 70)

    for app in applications:
        icon = STATUS_ICONS.get(app.status)
        print(f"{app.id:<5}{app.company:<20}{app.role:<20}{icon} {app.status}")

    print("=" * 70)
    # Prompt user for detailed view
    try:
        choose = int(input("Enter application ID to view details: "))
    except ValueError:
        print("\nInvalid input. Please enter a valid numerical ID.")
    else:
        print()
        # this will show a detailed window of the application
        matched_app = next((app for app in applications if app.id == choose), None)
        
        if matched_app:
            print(matched_app)
        else:
            print("Application not found")

    # Go back to menu
    input("Press Enter to return to the main menu...")


def update_status():
    applications = load_json_file("applications.json")
    if not applications:
            print("No applications found")
            return
        
    # the short view of job applications
    print("=" * 70)
    print(f"{'ID':<5}{'Company':<20}{'Role':<20}{'Status':<15}")
    print("-" * 70)
    for app in applications:
            icon = STATUS_ICONS.get(app.status)
            print(f"{app.id:<5}{app.company:<20}{app.role:<20}{icon} {app.status}")
    
    print("=" * 70)

    update = int(input("Enter application ID to update: \n"))

    for app in applications:
        icon = STATUS_ICONS.get(app.status)
        if update == app.id:
            print(f"Current Status: {icon} {app.status}")

            print("Select new Status: ")

            # Loop through the list to print them dynamically (1-indexed)
            for index, status in enumerate(STATUSES, start=1):
                print(f"{index}. {status}")

            try:
                choice = int(input("Choice: "))

                # Validate the user's input
                if 1 <= choice <= len(STATUSES):
                    selected_status = STATUSES[choice - 1]
                    app.status = selected_status
                    print(f"Successfully updated status to: {selected_status}")
                    save_json_file("applications.json", applications)
                    return 
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            print("Press Enter to return to main menu")
            input("\nPress Enter to return to the main menu...")
   

def delete_application():
    applications = load_json_file("applications.json")
    if not applications:
            print("No applications found")
            return
        
    # the short view of job applications
    print("=" * 70)
    print(f"{'ID':<5}{'Company':<20}{'Role':<20}{'Status':<15}")
    print("-" * 70)
    for app in applications:
            icon = STATUS_ICONS.get(app.status)
            print(f"{app.id:<5}{app.company:<20}{app.role:<20}{icon} {app.status}")
    
    print("=" * 70)
    try:
        delete = int(input("Enter application ID to delete: "))
        for app in applications:
            if delete == app.id:
                applications.remove(app)
                save_json_file("applications.json", applications)
                print("✓ Application successfully deleted")
                return 
        print("Application does not exit")       

    except ValueError:
            print("Invalid input. Please enter a valid number.")

    
def search_application():
    applications = load_json_file("applications.json")
    while True:

        # TODO for the future: make this look better
        menu = """Search By:
        1. By Company
        2. By Role
        3. By Location
        4. By Status
        5. Back"""

        print(menu)
        choice = input("Enter choice: ")
        if choice == "1":
            print("Search By Company")

            search_company = input("Enter Company: ").lower()
            match = False
            for app in applications:
                if app.company.lower().startswith(search_company):
                    match = True
                    print(app)
            if not match:
                print("Company not found")

        if choice == "2":
            print("Search by role")

            search_role = input("Enter Role: ").lower()
            match = False
            for app in applications:
                if app.role.lower().startswith(search_role):
                    match = True
                    print(app)
            if not match:
                print("Role not found")
            
        if choice == "3":
            print("Search by location")
            
            search_location = input("Enter Role: ").lower()
            match = False
            for app in applications:
                if app.role.lower().startswith(search_location):
                    match = True
                    print(app)
            if not match:
                print("Applications in given location not found")

        if choice == "3":
            print("Search by Status")
            
            search_status = input("Enter Role: ").lower()
            match = False
            for app in applications:
                if app.role.lower().startswith(search_status):
                    match = True
                    print(app)
            if not match:
                print("Status not found")
        if choice == "5":
            break
                

def show_statistics():
    applications = load_json_file("applications.json")

    print()
    print("""-----Statistics-----

1. View Terminal Statistics

2. Generate Applications by Status Chart

3. Back""")
    
    print()
    choice = int(input("Enter your choice: "))

    # build tracking dictionary dynamically
    track = {status: 0 for status in STATUSES}

    # count each status
    for app in applications:
        if app.status in track:
            track[app.status] += 1

    # FOR THE TERMINAL STATS
    if 1 <= choice <= 3 and choice == 1:
        print("\n" + "=" * 50)
        print("📊 JOB STATISTICS".center(50))
        print("=" * 50)

        total = len(applications)
        print(f"\n📄 Total Applications : {total}\n")


        print("Application Status")
        print("-" * 50)

        # prevent division by zero
        max_count = max(track.values()) if total else 1

        for status, count in track.items():
            # scale bars to a maximum width of 20
            bar_length = int((count / max_count) * 20) if count else 0
            bar = "■" * bar_length

            percentage = (count / total * 100) if total else 0

            print(
                f"{status:<20} "
                f"{bar:<20} "
                f"{count:>2} ({percentage:>5.1f}%)"
            )

        print("=" * 50)
        input("\nPress Enter to return to the menu...")
    

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
        print("\nChart saved as charts/job_statistics.png")

        

if __name__ == "__main__":
    main()