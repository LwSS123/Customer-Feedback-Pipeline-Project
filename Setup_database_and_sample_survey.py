import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os


# # Check if the database file exists
# if os.path.exists('survey_responses.db'):
#      # Remove the existing database file
#     os.remove('survey_responses.db')
#     print("Existing database removed.")

# Create database connection
conn = sqlite3.connect('survey_responses.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS responses (
    gender TEXT,
    age TEXT,
    occupation TEXT,
    education TEXT,
    q1 INTEGER,
    q2 INTEGER,
    q3 INTEGER,
    q4 INTEGER,
    q5 INTEGER,
    q6 INTEGER,
    q7 INTEGER,
    q8 INTEGER,
    q9 INTEGER,
    q10 INTEGER,
    interest TEXT,
    value TEXT,
    improvement TEXT,
    next_theme TEXT,
    other_comments TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Create main window
root = tk.Tk()
root.title("Event Feedback Survey")
root.geometry("600x800")

# Scrollable Frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Variables
gender = tk.StringVar()
age = tk.StringVar()
occupation = tk.StringVar()
education = tk.StringVar()
satisfaction_scores = {f"q{i}": tk.IntVar(value=1) for i in range(1, 11)}
interest = tk.StringVar()
value = tk.StringVar()
improvement = tk.StringVar()
next_theme = tk.StringVar()
other_comments = tk.StringVar()

# Personal Information
ttk.Label(frame, text="Personal Information", font=('Helvetica', 16)).pack(fill=tk.X, pady=10)
ttk.Label(frame, text="1. Your gender:").pack(anchor=tk.W)
genders = [("Male", "Male"), ("Female", "Female")]
for text, mode in genders:
    ttk.Radiobutton(frame, text=text, variable=gender, value=mode).pack(anchor=tk.W)
ttk.Label(frame, text="2. Your age:").pack(anchor=tk.W)
ages = ["13-19", "20-29", "30-39", "40-49", "50-59", "60+"]
age_combo = ttk.Combobox(frame, textvariable=age, values=ages, state='readonly')
age_combo.pack(fill=tk.X, expand=True, padx=10)
ttk.Label(frame, text="3. Your occupation:").pack(anchor=tk.W)
occupations = ["Student", "Government/Military/Public Service", "Service Industry", "Business/Industrial", "Self-Employed", "Homemaker", "Retired", "Other"]
occupation_combo = ttk.Combobox(frame, textvariable=occupation, values=occupations, state='readonly')
occupation_combo.pack(fill=tk.X, expand=True, padx=10)
ttk.Label(frame, text="4. Your education level:").pack(anchor=tk.W)
educations = ["Elementary School", "Junior High School", "High School/Diploma", "College/University", "Master's Degree"]
education_combo = ttk.Combobox(frame, textvariable=education, values=educations, state='readonly')
education_combo.pack(fill=tk.X, expand=True, padx=10)

# Satisfaction Survey
ttk.Label(frame, text="Satisfaction Survey", font=('Helvetica', 16)).pack(fill=tk.X, pady=20)
questions = [
    "Overall, I am very satisfied with this event.",
    "The content of this event was helpful to me.",
    "This event was very rewarding.",
    "I look forward to participating in similar events in the future.",
    "I would recommend this event to peers or friends.",
    "The event's theme and content were consistent.",
    "The presenter's overall performance was good.",
    "The event was well-organized.",
    "The timing of the event was appropriate.",
    "The location of the event was convenient."
]

for idx, question in enumerate(questions, 1):
    question_frame = ttk.Frame(frame)
    question_frame.pack(fill=tk.X, padx=10, pady=10)  
    ttk.Label(question_frame, text=f"{idx}. {question}").pack(fill=tk.X)
    scale_frame = ttk.Frame(question_frame)
    scale_frame.pack(fill=tk.X, padx=10)
    ttk.Label(scale_frame, text="1 Strongly Disagree").pack(side=tk.LEFT)
    ttk.Scale(scale_frame, from_=1, to=5, variable=satisfaction_scores[f"q{idx}"], orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)
    ttk.Label(scale_frame, text="5 Strongly Agree").pack(side=tk.RIGHT)
def labeled_input(parent, label_text, widget_factory, **kwargs):
    """
    Creates a labeled input field using the specified widget factory.

    :param parent: The parent widget.
    :param label_text: The text for the label.
    :param widget_factory: The factory function for creating the input widget.
    :param kwargs: Additional arguments for the widget factory.
    :return: The created input widget.
    """
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, padx=10, pady=5)
    
    label = ttk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    
    input_widget = widget_factory(frame, **kwargs)
    input_widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    return input_widget

# Open-Ended Questions
ttk.Label(frame, text="Open-Ended Questions", font=('Helvetica', 16)).pack(fill=tk.X, pady=10)
interest_entry = labeled_input(frame, "The most interesting part of the event was:", ttk.Entry, textvariable=interest)
value_entry = labeled_input(frame, "The most valuable content of the event was:", ttk.Entry, textvariable=value)
improvement_entry = labeled_input(frame, "I think the event could be improved by adding:", ttk.Entry, textvariable=improvement)
next_theme_entry = labeled_input(frame, "I would like the theme of the next event to be:", ttk.Entry, textvariable=next_theme)
other_comments_entry = labeled_input(frame, "Other comments and suggestions:", ttk.Entry, textvariable=other_comments)

# Submit Button
# Submit Button Functionality
def submit():
    # Check if personal information is not filled
    if not (gender.get() and age.get() and occupation.get() and education.get()):
        for key in satisfaction_scores:
            satisfaction_scores[key].set(0)  # Set all satisfaction scores to 0
    
    try:
        data = (
            gender.get(), age.get(), occupation.get(), education.get(),
            *[satisfaction_scores[f"q{i}"].get() for i in range(1, 11)],
            interest.get(), value.get(), improvement.get(), next_theme.get(), other_comments.get()
        )
        c.execute('''
        INSERT INTO responses (
            gender, age, occupation, education, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
            interest, value, improvement, next_theme, other_comments, submitted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', data)
        conn.commit()
        messagebox.showinfo("Success", "Thank you for your feedback!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        conn.rollback()

submit_button = ttk.Button(frame, text="Submit", command=submit)
submit_button.pack(pady=20)

# Run the application
root.mainloop()

# Close the database connection
conn.close()