#SOURCE CODE – PYTHON- JOB_LINKER
import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import messagebox, simpledialog
from reportlab.pdfgen import canvas
import os
from reportlab.lib import colors #type:ignore
from reportlab.lib.pagesizes import letter #type:ignore
from reportlab.pdfgen import canvas
from fpdf import FPDF
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph #type: ignore
from reportlab.lib.styles import getSampleStyleSheet #type: ignore
style = getSampleStyleSheet()
 
 
try:
    # Connect to the MySQL database
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="job_linker"
    )
 
    print('Test connection Successful')
                
    cursor = db.cursor()
    db.commit()
 
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error: {err}")
        
finally:
    if db.is_connected():
        cursor.close()
        db.close()
 
# Connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
          password="123456789",
        database="JOB_LINKER"
    )
 
def create_account_window():
    # Create a new window for account creation
    account_window = tk.Toplevel(root)
    account_window.title("Create Account")
 
    # Label for user type selection
    tk.Label(account_window, text="Select Account Type:").pack()
 
    # Button for employer account creation
    employer_button = tk.Button(account_window, text="Employer", command=lambda: create_account("emp"))
    employer_button.pack(pady=5)
 
    # Button for job seeker account creation
    job_seeker_button = tk.Button(account_window, text="Job Seeker", command=lambda: create_account("jsk"))
    job_seeker_button.pack(pady=5)
 
    # Run the account creation window
    account_window.mainloop()
 
def create_account(user_type):
    # Create a new window for account creation
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")
 
    # Label and entry for username
    tk.Label(create_account_window, text="Username:").pack()
    username_entry = tk.Entry(create_account_window)
    username_entry.pack()
 
    # Label and entry for password
    tk.Label(create_account_window, text="Password:").pack()
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.pack()
 
    # Label and entry for email
    tk.Label(create_account_window, text="Email:").pack()
    email_entry = tk.Entry(create_account_window)
    email_entry.pack()
 
    # Label and entry for phone number
    tk.Label(create_account_window, text="Phone Number:").pack()
    phone_entry = tk.Entry(create_account_window)
    phone_entry.pack()
 
    # Function to handle account creation submission
    def submit_account():
        # Get the values from the entry fields
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        phone_number = phone_entry.get()
 
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Insert new account into the appropriate table
        if user_type == "emp":
            query = "INSERT INTO login_credentials (user_id, user_type,email, password) VALUES (%s, %s, %s,%s)"
            cursor.execute(query, (username, user_type,email, password))
 
            query = "INSERT INTO employers (employer_id, name, email, phone_no,password) VALUES (%s, %s, %s, %s,%s)"
            cursor.execute(query, (username, username, email, phone_number,password))
        else:
            query = "INSERT INTO login_credentials (user_id, user_type,email, password) VALUES (%s, %s, %s,%s)"
            cursor.execute(query, (username, user_type,email, password))
 
            query = "INSERT INTO job_seekers (job_seeker_id, name, email, phone_no,password) VALUES (%s, %s, %s, %s,%s)"
            cursor.execute(query, (username, username, email, phone_number,password))
 
        # Commit changes and close the database connection
        db_connection.commit()
        cursor.close()
        db_connection.close()
 
        # Close the account creation window
        create_account_window.destroy()
 
        # Inform the user that the account has been created
        messagebox.showinfo("Account Created", "Account created successfully. Please login.")
 
    # Button to submit the account creation
    submit_button = tk.Button(create_account_window, text="Create Account", command=submit_account)
    submit_button.pack(pady=10)
 
    # Run the account creation window
    create_account_window.mainloop()
 
 
 
# Function to open employer dashboard window
def create_employer_dashboard(username):
    def open_employer_dashboard():
        dashboard_window = tk.Toplevel(root)
        dashboard_window.title("Employer Dashboard")
 
        # Add button to view profile
        view_profile_button = tk.Button(dashboard_window, text="View Profile", command=lambda: view_profile_emp(username))
        view_profile_button.pack(pady=10)
     
        # Add button to search jobs
        update_jobs_button = tk.Button(dashboard_window, text="Update Application Deadline", command=lambda: update_application_deadline(username))
        update_jobs_button.pack(pady=10)
    
        # Add button to apply for jobs
        add_jobs_button = tk.Button(dashboard_window, text="Add Job Vacancy", command=lambda: add_job_vacancy(username))
        add_jobs_button.pack(pady=10)
 
        # Add button to apply for jobs
        delete_jobs_button = tk.Button(dashboard_window, text="Delete Job Vacancy", command=lambda: delete_job_vacancy(username))
        delete_jobs_button.pack(pady=10)
 
        # Add button to apply for jobs
        app_jobs_button = tk.Button(dashboard_window, text="View Job Vacancy", command=lambda: view_job_vacancies(username))
        app_jobs_button.pack(pady=10)
 
        apply_jobs_button = tk.Button(dashboard_window, text="View and Update Application Request", command=lambda: view_and_update_applications(username))
        apply_jobs_button.pack(pady=10)
 
    open_employer_dashboard()
 
def view_profile_emp(username):
    # Connect to the database
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
 
    # Retrieve employer's profile information
    query = "SELECT * FROM employers WHERE employer_id = %s"
    cursor.execute(query, (username,))
    employer_profile = cursor.fetchone()
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
    # Function to open employer profile window
    def open_profile_window_emp():
        # Display profile information in a new window
        profile_window = tk.Toplevel()
        profile_window.title("Employer Profile")
        # Display profile information in labels
        tk.Label(profile_window, text="Employer ID:").pack()
        tk.Label(profile_window, text=employer_profile[0]).pack()  # Assuming employer_id is the first column
        tk.Label(profile_window, text="Name:").pack()
        tk.Label(profile_window, text=employer_profile[1]).pack()  # Assuming name is the second column
        tk.Label(profile_window, text="Email:").pack()
        tk.Label(profile_window, text=employer_profile[2]).pack()  # Assuming email is the third column
        tk.Label(profile_window, text="Phone No:").pack()
        tk.Label(profile_window, text=employer_profile[3]).pack()  # Assuming phone_no is the fourth column
 
    open_profile_window_emp()
 
def add_job_vacancy(username):
    # Create add job vacancy window
    add_job_window = tk.Toplevel()
    add_job_window.title("Add Job Vacancy")
 
    # Display the username and listing ID
    tk.Label(add_job_window, text=f"Employer ID: {username}").pack()
 
    # Create a StringVar to hold the listing ID
    listing_id_var = tk.StringVar()
 
    # Display the listing ID
    listing_id_label = tk.Label(add_job_window, textvariable=listing_id_var)
    listing_id_label.pack()
 
    # Entry fields for job vacancy details
    tk.Label(add_job_window, text="Position:").pack()
    position_entry = tk.Entry(add_job_window)
    position_entry.pack()
 
    tk.Label(add_job_window, text="Description:").pack()
    description_entry = tk.Text(add_job_window, height=5, width=50)
    description_entry.pack()
 
    tk.Label(add_job_window, text="Requirements:").pack()
    requirements_entry = tk.Text(add_job_window, height=5, width=50)
    requirements_entry.pack()
 
    tk.Label(add_job_window, text="Deadline (YYYY-MM-DD):").pack()
    application_deadline_entry = tk.Entry(add_job_window)
    application_deadline_entry.pack()
 
    # Function to handle submitting the job vacancy
    def submit_job_vacancy():
        nonlocal listing_id_var
 
        # Get job vacancy details from entry fields
        employer_id = username
        position = position_entry.get()
        description = description_entry.get("1.0", tk.END)
        requirements = requirements_entry.get("1.0", tk.END)
        application_deadline = application_deadline_entry.get()
 
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Get the number of existing job listings for the employer
        query = "SELECT COUNT(*) FROM job_listings WHERE employer_id = %s"
        cursor.execute(query, (employer_id,))
        count = cursor.fetchone()[0]
 
        # Generate the listing_id
        listing_id = f"{employer_id}{count + 1:03}"
 
        # Insert job vacancy details into the database
        query = "INSERT INTO job_listings (listing_id, employer_id, position, description, requirements, application_deadline) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (listing_id, employer_id, position, description, requirements, application_deadline))
        db_connection.commit()
 
        # Close database connection
        cursor.close()
        db_connection.close()
 
        # Display the generated listing ID
        listing_id_var.set(f"Listing ID: {listing_id}")
 
        messagebox.showinfo("Job Vacancy Added", "Job vacancy added successfully.")
        add_job_window.destroy()
 
    # Submit button
    submit_button = tk.Button(add_job_window, text="Submit", command=submit_job_vacancy)
    submit_button.pack()
 
    # Run the add job vacancy window
    add_job_window.mainloop()
 
def view_job_vacancies(username):
    try:
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
        # Extract employer_id from username (first five characters)
        employer_id = username[:5]
 
        # Query to fetch job listings for the employer
        query = "SELECT listing_id, position, application_deadline FROM job_listings WHERE employer_id = %s"
        cursor.execute(query, (username,))
        jobs = cursor.fetchall()
 
        # Create a new window to display job vacancies
        vacancies_window = tk.Toplevel()
        vacancies_window.title("Job Vacancies")
 
        # Create a treeview to display job vacancies
        tree = ttk.Treeview(vacancies_window, columns=("Position", "Deadline"))
        tree.heading("#0", text="ID")
        tree.heading("Position", text="Position")
        tree.heading("Deadline", text="Deadline")
        tree.column("#0", width=50)
        tree.column("Position", width=200)
        tree.column("Deadline", width=150)
        tree.pack(expand=True, fill='both')
 
        # Populate the treeview with job listings
        for job in jobs:
            tree.insert("", "end", text=job[0], values=(job[1], job[2]))
 
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(vacancies_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
 
        # Function to generate and print PDF
        def generate_pdf(jobs):
            print("generating pdf")
            # Create a PDF file
            c = canvas.Canvas("C:\\Users\\91799\\OneDrive\\Desktop\\job_search_results.pdf")
            c.setFont("Helvetica", 12)
            y_position = 750  # Initial y position
            for job in jobs:
                # Write job details to the PDF
                c.drawString(100, y_position, f"ID: {job[0]}, Position: {job[1]}, Deadline: {job[2]}")
                y_position -= 20  # Move to the next line
            c.save()
            os.startfile("C:\\Users\\91799\\OneDrive\\Desktop\\job_search_results.pdf")
 
        # Print button to generate and print PDF
        print_button = tk.Button(vacancies_window, text="Print Results", command=lambda: generate_pdf(jobs))
        print_button.pack()
 
        # Start the Tkinter main loop
        vacancies_window.mainloop()
 
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching job vacancies: {e}")
   
def view_and_update_applications(username):
    def display_applications():
        try:
            # Connect to the MySQL database
            db_connection = connect_to_db()
            cursor = db_connection.cursor()
 
            # Extract employer_id from username (first five characters)
            employer_id = username[:5]
    
            # Query to fetch job applications for the employer
            query = "SELECT * FROM applications WHERE listing_id LIKE %s"
            cursor.execute(query, (f"{employer_id}%",))
            applications = cursor.fetchall()
 
            # Create a new window to display job applications
            applications_window = tk.Toplevel()
            applications_window.title("Job Applications")
 
            # Create a treeview to display job applications
            tree = ttk.Treeview(applications_window, columns=("Job Seeker ID", "Status", "Application Date"))
            tree.heading("#0", text="Application ID")
            tree.heading("Job Seeker ID", text="Job Seeker ID")
            tree.heading("Status", text="Status")
            tree.heading("Application Date", text="Application Date")
            tree.column("#0", width=100)
            tree.column("Job Seeker ID", width=150)
            tree.column("Status", width=100)
            tree.column("Application Date", width=150)
            tree.pack(expand=True, fill='both')
 
            # Populate the treeview with job applications
            for application in applications:
                application_id, job_seeker_id, listing_id, status, application_date = application
                tree.insert("", "end", text=application_id, values=(job_seeker_id, status, application_date))
 
                # Update status buttons
                application_frame = tk.Frame(applications_window)
                application_frame.pack(pady=5)
 
                tk.Label(application_frame, text=f"Application ID: {application_id}").pack()
                tk.Label(application_frame, text=f"Job Applicant ID: {job_seeker_id}").pack()
                tk.Label(application_frame, text=f"Job Listing ID: {listing_id}").pack()
                tk.Label(application_frame, text=f"Status: {status}").pack()
 
                status_frame = tk.Frame(application_frame)
                status_frame.pack(pady=5)
 
                accept_button = tk.Button(status_frame, text="Accept", command=lambda id=application_id: update_application_status(id, "ACCEPTED"))
                accept_button.pack(side=tk.LEFT, padx=5)
 
                decline_button = tk.Button(status_frame, text="Decline", command=lambda id=application_id: update_application_status(id, "DECLINED"))
                decline_button.pack(side=tk.LEFT, padx=5)
 
                in_process_button = tk.Button(status_frame, text="In Process", command=lambda id=application_id: update_application_status(id, "IN-PROCESS"))
                in_process_button.pack(side=tk.LEFT, padx=5)
 
                pending_button = tk.Button(status_frame, text="Pending", command=lambda id=application_id: update_application_status(id, "PENDING"))
                pending_button.pack(side=tk.LEFT, padx=5)
 
            # Add a scrollbar
            scrollbar = ttk.Scrollbar(applications_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)
 
            applications_window.mainloop()
 
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching job applications: {e}")
 
    def update_application_status(application_id, new_status):
        try:
            # Connect to the MySQL database
            db_connection = connect_to_db()
            cursor = db_connection.cursor()
 
            # Update the status of the application
            query = "UPDATE applications SET status = %s WHERE application_id = %s"
            cursor.execute(query, (new_status, application_id))
            db_connection.commit()
 
            # Close database connection
            cursor.close()
            db_connection.close()
 
            # Show a success message
            messagebox.showinfo("Status Updated", f"Application {application_id} status updated to {new_status}.")
 
            # Refresh the application list
            display_applications()
 
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error updating application status: {e}")
 
    display_applications()
 
def update_application_deadline(username):
    # Function to handle updating the application deadline
    def update_deadline():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a job vacancy to update the deadline.")
            return
 
        job_id = tree.item(selected_item, 'text')
        new_deadline = new_deadline_entry.get()
 
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Update the application deadline for the selected job vacancy
        query = "UPDATE job_listings SET application_deadline = %s WHERE listing_id = %s AND employer_id = %s"
        cursor.execute(query, (new_deadline, job_id, username))
        db_connection.commit()
 
        # Close database connection
        cursor.close()
        db_connection.close()
 
        messagebox.showinfo("Deadline Updated", "Application deadline updated successfully.")
        update_deadline_window.destroy()
    
 
    # Create update deadline window
    update_deadline_window = tk.Toplevel()
    update_deadline_window.title("Update Application Deadline")
 
    # Display a list of job vacancies for the employer to select from
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    query = "SELECT listing_id, position, application_deadline FROM job_listings WHERE employer_id = %s"
    cursor.execute(query, (username,))
    jobs = cursor.fetchall()
 
    tree = ttk.Treeview(update_deadline_window, columns=("Position", "Deadline"))
    tree.heading("#0", text="ID")
    tree.heading("Position", text="Position")
    tree.heading("Deadline", text="Deadline")
    tree.column("#0", width=50)
    tree.column("Position", width=200)
    tree.column("Deadline", width=150)
    tree.pack(expand=True, fill='both')
 
    for job in jobs:
        tree.insert("", "end", text=job[0], values=(job[1], job[2]))
 
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(update_deadline_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
 
    # Entry field for new deadline
    tk.Label(update_deadline_window, text="New Deadline (YYYY-MM-DD):").pack()
    new_deadline_entry = tk.Entry(update_deadline_window)
    new_deadline_entry.pack()
 
    # Update button
    update_button = tk.Button(update_deadline_window, text="Update Deadline", command=update_deadline)
    update_button.pack()
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
    # Run the update deadline window
    update_deadline_window.mainloop()
 
def delete_job_vacancy(username):
    # Function to handle deleting a job vacancy
    def delete_selected_job():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a job vacancy to delete.")
            return
 
        job_id = tree.item(selected_item, 'text')
 
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Delete the selected job vacancy
        query = "DELETE FROM job_listings WHERE listing_id = %s AND employer_id = %s"
        cursor.execute(query, (job_id, username))
        db_connection.commit()
 
        # Close database connection
        cursor.close()
        db_connection.close()
 
        messagebox.showinfo("Job Vacancy Deleted", "Job vacancy deleted successfully.")
        delete_job_window.destroy()
 
    # Create delete job vacancy window
    delete_job_window = tk.Toplevel()
    delete_job_window.title("Delete Job Vacancy")
 
    # Display a list of job vacancies for the employer to select from
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    query = "SELECT listing_id, position FROM job_listings WHERE employer_id = %s"
    cursor.execute(query, (username,))
    jobs = cursor.fetchall()
 
    tree = ttk.Treeview(delete_job_window, columns=("Position",))
    tree.heading("#0", text="ID")
    tree.heading("Position", text="Position")
    tree.column("#0", width=50)
    tree.column("Position", width=200)
    tree.pack(expand=True, fill='both')
 
    for job in jobs:
        tree.insert("", "end", text=job[0], values=(job[1],))
 
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(delete_job_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
 
    # Delete button
    delete_button = tk.Button(delete_job_window, text="Delete", command=delete_selected_job)
    delete_button.pack()
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
    # Run the delete job vacancy window
    delete_job_window.mainloop()
 
 
# Function to open jsk dashboard window
def create_jsk_dashboard(username):
    # Function to open jsk dashboard window
    def open_jsk_dashboard():
        dashboard_window = tk.Toplevel(root)
        dashboard_window.title("Applicant Dashboard")
 
        # Add button to view profile
        view_profile_button = tk.Button(dashboard_window, text="View Profile", command=lambda: view_profile_jsk(username))
        view_profile_button.pack(pady=10)
 
        # Add button to search jobs
        search_jobs_button = tk.Button(dashboard_window, text="Search and Apply for Jobs", command=lambda: search_jobs(username))
        search_jobs_button.pack(pady=10)
 
        # Add button to search jobs
        applied_jobs_button = tk.Button(dashboard_window, text="View my Job Application", command=lambda: view_applied_jobs(username))
        applied_jobs_button.pack(pady=10)
 
        # Add button to search jobs
        delete_jobs_button = tk.Button(dashboard_window, text="Withdraw Job Application", command=lambda: delete_job_application(username))
        delete_jobs_button.pack(pady=10)
      
 
       
    open_jsk_dashboard()
 
def view_profile_jsk(username):
    # Connect to the database
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
 
    # Retrieve employer's profile information
    query = "SELECT * FROM job_seekers WHERE job_seeker_id = %s"
    cursor.execute(query, (username,))
    jsk_profile = cursor.fetchone()
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
    # Function to open jsk profile window
    def open_profile_window_jsk():
        # Display profile information in a new window
        profile_window = tk.Toplevel()
        profile_window.title("Job Applicant Profile")
        # Display profile information in labels
        tk.Label(profile_window, text="Applicant ID:").pack()
        tk.Label(profile_window, text=jsk_profile[0]).pack()  # Assuming employer_id is the first column
        tk.Label(profile_window, text="Name:").pack()
        tk.Label(profile_window, text=jsk_profile[1]).pack()  # Assuming name is the second column
        tk.Label(profile_window, text="Email:").pack()
        tk.Label(profile_window, text=jsk_profile[2]).pack()  # Assuming email is the third column
        tk.Label(profile_window, text="Phone No:").pack()
        tk.Label(profile_window, text=jsk_profile[3]).pack()  # Assuming phone_no is the fourth column
 
    open_profile_window_jsk()
 
 
def search_jobs(username):
    # Function to handle job search
    def search():
        # Get search criteria from entry field
        search_keyword = search_entry.get()
 
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Search for job listings based on the search keyword
        query = "SELECT * FROM job_listings WHERE position LIKE %s OR description LIKE %s OR requirements LIKE %s"
        cursor.execute(query, (f"%{search_keyword}%", f"%{search_keyword}%", f"%{search_keyword}%"))
        jobs = cursor.fetchall()
 
        # Close database connection
        cursor.close()
        db_connection.close()
 
        # Display search results in a new window
        search_results_window = tk.Toplevel()
        search_results_window.title("Job Search Results")
 
        # Create a treeview to display job listings
        tree = ttk.Treeview(search_results_window, columns=("Employer ID","Position", "Description", "Requirements", "Deadline"))
        tree.heading("#0", text="ID")
        tree.column("#0", width=50)
        tree.heading("Employer ID", text="Employer ID")
        tree.heading("Position", text="Position")
        tree.heading("Description", text="Description")
        tree.heading("Requirements", text="Requirements")
        tree.heading("Deadline", text="Deadline")
        tree.column("Employer ID", width=100)
        tree.column("Position", width=200)
        tree.column("Description", width=400)
        tree.column("Requirements", width=200)
        tree.column("Deadline", width=150)
        tree.pack(expand=True, fill='both')
 
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(search_results_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
 
        for job in jobs:
            apply_button = tk.Button(search_results_window, text="Apply", command=lambda job_id=job[0]: apply_for_job_window(username, job_id))
            tree.insert("", "end", text=job[0], values=(job[1], job[2], job[3], job[4], job[5]), tags=("button",))
            tree.tag_bind("button", "<Button-1>", lambda event, job_id=job[0]: apply_for_job_window(username, job_id))
 
    # Create search window
    search_window = tk.Toplevel()
    search_window.title("Job Search")
 
    # Entry field for search keyword
    tk.Label(search_window, text="Enter keyword to search jobs:").pack()
    search_entry = tk.Entry(search_window)
    search_entry.pack()
 
    # Search button
    search_button = tk.Button(search_window, text="Search", command=search)
    search_button.pack()
 
    # Run the application
    search_window.mainloop()
 
def apply_for_job_window(username, job_id):
    def apply():
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Get the number of existing applications for the job seeker
        query = "SELECT COUNT(*) FROM applications WHERE job_seeker_id = %s"
        cursor.execute(query, (username,))
        count = cursor.fetchone()[0]
 
        # Generate the application_id
        application_id = f"{username}{count + 1:03}"
 
        # Check if the job applicant has already applied for this job
        query = "SELECT * FROM applications WHERE job_seeker_id = %s AND listing_id = %s"
        cursor.execute(query, (username, job_id))
        existing_application = cursor.fetchone()
 
        if existing_application:
            messagebox.showinfo("Application Status", "You have already applied for this job.")
        else:
            # Apply for the job
            query = "INSERT INTO applications (application_id, job_seeker_id, listing_id, status, application_date) VALUES (%s, %s, %s, %s, NOW())"
            cursor.execute(query, (application_id, username, job_id, "Pending"))
            db_connection.commit()
            messagebox.showinfo("Application Status", "Application submitted successfully.")
 
        # Close database connection
        cursor.close()
        db_connection.close()
 
    # Create a new window for job details and apply button
    apply_window = tk.Toplevel()
    apply_window.title("Apply for Job")
 
    # Retrieve job details from the database
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    query = "SELECT * FROM job_listings WHERE listing_id = %s"
    cursor.execute(query, (job_id,))
    job_details = cursor.fetchone()
    cursor.close()
    db_connection.close()
 
    # Display job details
    tk.Label(apply_window, text=f"Position: {job_details[2]}").pack()
    tk.Label(apply_window, text=f"Description: {job_details[3]}").pack()
    tk.Label(apply_window, text=f"Requirements: {job_details[4]}").pack()
    tk.Label(apply_window, text=f"Application Deadline: {job_details[5]}").pack()
    tk.Label(apply_window, text=f"Employer ID: {job_details[1]}").pack()
 
    # Apply button
    apply_button = tk.Button(apply_window, text="Apply", command=apply)
    apply_button.pack(pady=10)
def delete_job_application(username):
    # Function to handle deleting a job vacancy
    def delete_select_job():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a job application to delete.")
            return
 
        job_id = tree.item(selected_item, 'text')
 
        # Connect to the database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Delete the selected job vacancy
        query = "DELETE FROM applications WHERE application_id = %s AND job_seeker_id = %s"
        cursor.execute(query, (job_id, username))
        db_connection.commit()
 
        # Close database connection
        cursor.close()
        db_connection.close()
 
        messagebox.showinfo("Job Application Deleted", "Job Application deleted successfully.")
        delete_job_window.destroy()
 
    # Create delete job vacancy window
    delete_job_window = tk.Toplevel()
    delete_job_window.title("Withdraw Job Application")
 
    # Display a list of job vacancies for the employer to select from
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    query = "SELECT application_id, job_seeker_id, listing_id, status, application_date FROM applications WHERE job_seeker_id = %s"
    cursor.execute(query, (username,))
    jobs = cursor.fetchall()
 
    tree = ttk.Treeview(delete_job_window, columns=("Job Seeker ID", "Listing ID", "Status", "Application Date"))
    tree.heading("#0", text="Application ID")
    tree.heading("Job Seeker ID", text="Job Seeker ID")
    tree.heading("Listing ID", text="Listing ID")
    tree.heading("Status", text="Status")
    tree.heading("Application Date", text="Application Date")
    tree.column("#0", width=100)
    tree.column("Job Seeker ID", width=150)
    tree.column("Listing ID", width=150)
    tree.column("Status", width=100)
    tree.column("Application Date", width=150)
    tree.pack(expand=True, fill='both')
 
    for job in jobs:
        tree.insert("", "end", text=job[0], values=(job[1], job[2], job[3], job[4]))
 
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(delete_job_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
 
    # Delete button
    delete_button = tk.Button(delete_job_window, text="Delete", command=delete_select_job)
    delete_button.pack()
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
    # Run the delete job vacancy window
    delete_job_window.mainloop()
 
def view_applied_jobs(username):
    def on_select(event):
        selected_item = tree.selection()
        if not selected_item:
            return
        item = tree.item(selected_item)
        application_id = item['text']
        status = item['values'][1]
        if status == 'ACCEPTED':
            messagebox.showinfo("Invitation for Interview", "You are invited for the interview.")
        elif status == 'DECLINED':
            messagebox.showinfo("Job Application Declined", "Sorry, Your Job application has been declined.")
        elif status == 'IN-PROCESS':
            # Extracting listing_id from the database
            query = "SELECT listing_id FROM applications WHERE application_id = %s"
            cursor.execute(query, (application_id,))
            listing_id = cursor.fetchone()[0]
            employer_id = listing_id[:5]  # Assuming the first 5 characters of listing_id is employer_id
            # Query to fetch employer email
            query = "SELECT email FROM employers WHERE employer_id = %s"
            cursor.execute(query, (employer_id,))
            employer_email = cursor.fetchone()[0]
            messagebox.showinfo("Send Documents", f"Please send your resume and other documents to {employer_email}.")
        elif status == 'PENDING':
            messagebox.showinfo("Document Verification", "Your documents are in verification.")
 
 
    try:
        # Connect to the MySQL database
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
 
        # Query to fetch job applications for the job seeker
        query = "SELECT * FROM applications WHERE job_seeker_id = %s"
        cursor.execute(query, (username,))
        applications = cursor.fetchall()
 
        # Create a new window to display job applications
        applications_window = tk.Toplevel()
        applications_window.title("My Job Applications")
 
        # Create a treeview to display job applications
        tree = ttk.Treeview(applications_window, columns=("Listing ID", "Status", "Application Date"))
        tree.heading("#0", text="Application ID")
        tree.heading("Listing ID", text="Listing ID")
        tree.heading("Status", text="Status")
        tree.heading("Application Date", text="Application Date")
        tree.column("#0", width=100)
        tree.column("Listing ID", width=150)
        tree.column("Status", width=100)
        tree.column("Application Date", width=150)
        tree.pack(expand=True, fill='both')
 
        # Populate the treeview with job applications
        for application in applications:
            application_id, job_seeker_id, listing_id, status, application_date = application
            tree.insert("", "end", text=application_id, values=(listing_id, status, application_date))
 
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(applications_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        tree.bind("<<TreeviewSelect>>", on_select)
 
        applications_window.mainloop()
 
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching job applications: {e}")
    
def view_all_job_adm(username):
    # Connect to the database
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    query = "SELECT * FROM job_listings"
    cursor.execute(query)
    adm_jobs = cursor.fetchall()
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
    # Function to open adm profile window
    def open_jobs_adm():
        profile_window = tk.Toplevel()
        profile_window.title("ALL JOB VACANCY")
 
        # Create a treeview widget
        tree = ttk.Treeview(profile_window, columns=("Position", "Description", "Requirements", "Deadline", "Employer ID"))
        tree.heading("#0", text="ID")
        tree.heading("Position", text="Position")
        tree.heading("Description", text="Description")
        tree.heading("Requirements", text="Requirements")
        tree.heading("Deadline", text="Deadline")
        tree.heading("Employer ID", text="Employer ID")
 
        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(profile_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
 
        # Insert data into the treeview
        for job in adm_jobs:
            tree.insert("", "end", text=job[0], values=(job[2], job[3], job[4], job[5], job[1]))
 
        # Pack the treeview widget
        tree.pack(expand=True, fill="both")
 
    open_jobs_adm()
 
# Modify the login function to call create_employer_dashboard
def login(user_type):
    username = username_entry.get()
    password = password_entry.get()
 
    # Connect to the database
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
 
    # Check user credentials
    query = "SELECT * FROM login_credentials WHERE user_id = %s AND user_type = %s AND password = %s"
    cursor.execute(query, (username, user_type, password))
    result = cursor.fetchone()
 
    if result:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        # Handle different user types here (employer, job applicant, admin)
        # Redirect to appropriate interface
        if user_type == "emp":
            create_employer_dashboard(username)
        elif user_type == "jsk":
            create_jsk_dashboard(username)
        '''
        elif user_type == "adm":
            create_adm_dashboard(username)
        '''
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
 
    # Close database connection
    cursor.close()
    db_connection.close()
 
# Create main window
root = tk.Tk()
root.title("JOB - LINKER")
 
# Create login frame
login_frame = tk.Frame(root)
login_frame.pack(padx=20, pady=20)
 
# Username label and entry
username_label = tk.Label(login_frame, text="User ID:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)
 
# Password label and entry
password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)
 
# Login buttons
employer_button = tk.Button(login_frame, text="Login as Employer", command=lambda: login("emp"))
employer_button.grid(row=2, column=0, columnspan=2, pady=5)
job_applicant_button = tk.Button(login_frame, text="Login as Job Applicant", command=lambda: login("jsk"))
job_applicant_button.grid(row=3, column=0, columnspan=2, pady=5)
create_button = tk.Button(login_frame, text="Create Account", command=lambda: create_account_window())
create_button.grid(row=4, column=0, columnspan=2, pady=5)
 
# Run the application
root.mainloop()

