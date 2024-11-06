import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import webbrowser

class SimpleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zoom Meeting Information")
        self.geometry("500x500")
        self.config(bg="#f7f7f7")
        
        # Set the theme to 'clam' to make sure ttk styles are properly applied
        ttk.Style().theme_use('clam')

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create the pages
        self.page_one = PageOne(self.notebook)
        self.page_two = ZoomMeetingPage(self.notebook, self.page_one)  # Pass PageOne to update after submitting
        
        # Add pages to the Notebook with tab titles
        self.notebook.add(self.page_one, text="Schedule")
        self.notebook.add(self.page_two, text="Zoom Meeting Info")

class PageOne(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title_label = ttk.Label(self, text="Today's Zoom Meetings", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=15)
        
        # Create style for buttons
        self.style = ttk.Style(self)
        self.style.configure("MeetingButton.TButton",
                             font=("Arial", 14),
                             padding=10,
                             background="#4CAF50",  # Button background color
                             foreground="white")  # Text color
        self.style.map("MeetingButton.TButton",
                       background=[('active', '#45a049')])  # Change button color when hovered
        
        # Placeholder for buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Display today's meetings
        self.display_schedule()

    def display_schedule(self):
        # Get the current day of the week (e.g., "Monday")
        current_day = datetime.now().strftime("%A")

        # Initialize the schedule data
        schedule_data = self.read_schedule()

        # Clear any existing buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Get the index for the current day
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_index = days_of_week.index(current_day)

        # Iterate through the schedule data to display meetings for the current day
        meetings_for_today = [entry for entry in schedule_data if entry[0] == current_day]  # Filter entries by current day
        
        if meetings_for_today:
            # Sort the meetings by time (column 2)
            meetings_for_today.sort(key=lambda x: x[2])  # Sort by the 'Time' field (which is in 24-hour format)
            
            # Display each meeting's button
            for meeting in meetings_for_today:
                self.create_meeting_button(meeting)  # Pass each entry as a list to create the button
        else:
            # Display message if no meetings for today
            no_meetings_label = ttk.Label(self.buttons_frame, text="No meetings scheduled for today.", font=("Arial", 14, "italic"), foreground="gray")
            no_meetings_label.pack(pady=10)

    def read_schedule(self):
        # Read existing schedule from the CSV file
        data = []
        try:
            with open("schedule.csv", "r") as file:
                reader = csv.reader(file)
                data = list(reader)
                
                # Ensure the first row is the header
                if data[0] != ["Weekday", "Name", "Time", "Link", "Additional Info"]:
                    raise ValueError("CSV format is incorrect, missing header.")
        except FileNotFoundError:
            # Initialize with an empty list if file doesn't exist
            data = [["Weekday", "Name", "Time", "Link", "Additional Info"]]
        except ValueError as e:
            # Handle invalid CSV format
            messagebox.showerror("Error", str(e))
            return []

        return data[1:]  # Skip the header row and return the rest of the data

    def create_meeting_button(self, schedule_entry):
        # Extract data from the schedule entry
        course_name = schedule_entry[1]  # Name (column 2 in CSV)
        time = schedule_entry[2]         # Time (column 3 in CSV)
        additional_info = schedule_entry[4] if schedule_entry[4] != "N/A" else ""  # Additional Info (column 5 in CSV)

        # Create the button text with course name, time, and additional info
        button_text = f"{course_name}\n{time}\n{additional_info}"

        # Create the button with some padding and style
        meeting_button = ttk.Button(self.buttons_frame, text=button_text, command=lambda: self.open_link(schedule_entry[3]), style="MeetingButton.TButton")
        meeting_button.pack(pady=10, fill="x")

    def open_link(self, link):
        # Open the link in a web browser
        if link:
            webbrowser.open(link)
        else:
            messagebox.showerror("Invalid Link", "No valid link found for this meeting.")

class ZoomMeetingPage(tk.Frame):
    def __init__(self, parent, schedule_page):
        super().__init__(parent)
        self.schedule_page = schedule_page  # Reference to PageOne for refresh
        
        # Title
        title_label = ttk.Label(self, text="Enter Zoom Meeting Information", font=("Arial", 18, "bold"))
        title_label.pack(pady=15)

        # Course Name
        course_name_label = ttk.Label(self, text="Course Name:")
        course_name_label.pack(anchor="w", padx=15)
        self.course_name_entry = ttk.Entry(self, font=("Arial", 16))  # Set font size here
        self.course_name_entry.pack(fill="x", padx=15, pady=8)

        # Day of the Week
        day_label = ttk.Label(self, text="Day of the Week:")
        day_label.pack(anchor="w", padx=15)
        self.day_combobox = ttk.Combobox(self, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], font=("Arial", 16))  # Set font size here
        self.day_combobox.pack(fill="x", padx=15, pady=8)

        # Time Selection with Dropdowns for Hour, Minute, and AM/PM
        time_label = ttk.Label(self, text="Time:")
        time_label.pack(anchor="w", padx=15)

        # Hour Dropdown
        self.hour_combobox = ttk.Combobox(self, values=[f"{i:02d}" for i in range(1, 13)], width=5, font=("Arial", 16))  # Set font size here
        self.hour_combobox.set("08")  # Default value
        self.hour_combobox.pack(side="left", padx=(15, 5))

        # Minute Dropdown with 10-minute intervals
        self.minute_combobox = ttk.Combobox(self, values=["00", "10", "20", "30", "40", "50"], width=5, font=("Arial", 16))  # Set font size here
        self.minute_combobox.set("00")  # Default value
        self.minute_combobox.pack(side="left", padx=(0, 5))

        # AM/PM Dropdown
        self.ampm_combobox = ttk.Combobox(self, values=["AM", "PM"], width=5, font=("Arial", 16))  # Set font size here
        self.ampm_combobox.set("AM")  # Default value
        self.ampm_combobox.pack(side="left", padx=(0, 15))

        # Meeting Link
        link_label = ttk.Label(self, text="Link to the Class:")
        link_label.pack(anchor="w", padx=15)
        self.link_entry = ttk.Entry(self, font=("Arial", 16))  # Set font size here
        self.link_entry.pack(fill="x", padx=15, pady=8)

        # Additional Info
        additional_info_label = ttk.Label(self, text="Additional Info (Optional):")
        additional_info_label.pack(anchor="w", padx=15)
        self.additional_info_entry = ttk.Entry(self, font=("Arial", 16))  # Set font size here
        self.additional_info_entry.pack(fill="x", padx=15, pady=8)

        # Submit Button
        submit_button = ttk.Button(self, text="Submit", command=self.submit_info, style="SubmitButton.TButton")
        submit_button.pack(pady=15)

    def submit_info(self):
        # Collect the entered data
        course_name = self.course_name_entry.get()
        day = self.day_combobox.get()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        ampm = self.ampm_combobox.get()
        time_str = f"{hour}:{minute} {ampm}"
        link = self.link_entry.get()
        additional_info = self.additional_info_entry.get() or "N/A"

        # Validate inputs
        if not course_name or not day or not time_str or not link:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Convert 12-hour time to 24-hour time
        try:
            time_obj = datetime.strptime(time_str, "%I:%M %p")  # Convert to 24-hour format
            time_24hr = time_obj.strftime("%H:%M")  # Format as HH:MM (24-hour format)
        except ValueError:
            messagebox.showerror("Error", "Invalid time format.")
            return

        # Check if the time already exists for the given day
        schedule_data = self.schedule_page.read_schedule()
        existing_times = [entry[2] for entry in schedule_data if entry[0] == day]
        if time_24hr in existing_times:
            messagebox.showerror("Error", "A meeting is already scheduled at this time.")
            return

        # Append the new meeting info to the CSV
        self.append_schedule(course_name, day, time_24hr, link, additional_info)

        # Update PageOne after adding the new meeting
        self.schedule_page.display_schedule()  # Refresh the schedule display
        messagebox.showinfo("Success", "Zoom meeting info has been added.")

        # Clear the entry fields
        self.course_name_entry.delete(0, tk.END)
        self.day_combobox.set("")
        self.hour_combobox.set("08")
        self.minute_combobox.set("00")
        self.ampm_combobox.set("AM")
        self.link_entry.delete(0, tk.END)
        self.additional_info_entry.delete(0, tk.END)

    def append_schedule(self, course_name, day, time_str, link, additional_info):
        # Append the new meeting to the CSV
        with open("schedule.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([day, course_name, time_str, link, additional_info])

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()
