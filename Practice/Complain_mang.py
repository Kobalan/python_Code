import datetime

class ComplaintManagementSystem:
    def __init__(self):
        self.complaints = {}

    def submit_complaint(self, user_name, complaint_text):
        complaint_id = len(self.complaints) + 1
        timestamp = datetime.datetime.now()
        status = "Pending"
        self.complaints[complaint_id] = {
            "user_name": user_name,
            "complaint_text": complaint_text,
            "timestamp": timestamp,
            "status": status,
        }
        print(f"Complaint submitted successfully. Complaint ID: {complaint_id}")

    def view_complaints(self):
        if not self.complaints:
            print("No complaints to display.")
            return

        print("Complaints:")
        for complaint_id, complaint in self.complaints.items():
            print(
                f"ID: {complaint_id}, User: {complaint['user_name']}, Status: {complaint['status']}, Timestamp: {complaint['timestamp']}"
            )
            print(f"  {complaint['complaint_text']}")
            print()

    def update_complaint_status(self, complaint_id, new_status):
        if complaint_id in self.complaints:
            self.complaints[complaint_id]["status"] = new_status
            print(f"Complaint {complaint_id} status updated to {new_status}")
        else:
            print(f"Complaint {complaint_id} not found.")

# Example Usage
cms = ComplaintManagementSystem()

while True:
    print("\nComplaint Management System Menu:")
    print("1. Submit a Complaint")
    print("2. View Complaints")
    print("3. Update Complaint Status")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        user_name = input("Enter your name: ")
        complaint_text = input("Enter your complaint: ")
        cms.submit_complaint(user_name, complaint_text)

    elif choice == "2":
        cms.view_complaints()

    elif choice == "3":
        complaint_id = int(input("Enter the complaint ID: "))
        new_status = input("Enter the new status: ")
        cms.update_complaint_status(complaint_id, new_status)

    elif choice == "4":
        print("Exiting the Complaint Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
