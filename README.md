# Customer Feedback Pipeline
The "Customer Feedback Pipeline" project develops four different graphical user interfaces (GUIs) to collect, store, analyze, and report feedback from participants. This system is designed to allow for efficient feedback management and analysis, helping organizers improve future events based on actionable insights.
<br>

## Objective
The main objectives of this project are to:
- Collect diverse types of feedback via an intuitive GUI.
- Store feedback data securely in a SQLite3 database.
- Display personal information and satisfaction levels, and analyze feedback using fake data as a reference via the second GUI.
- Perform sentiment analysis and generate word clouds via the third GUI.
- Provide visual reports and allow for easy data export for further analysis via the fourth GUI. <br>

## Database Schema
Feedback data is stored in a SQLite database with the following schema:

| Column Name    | Data Type |
|----------------|-----------|
| gender         | TEXT      |
| age            | TEXT      |
| occupation     | TEXT      |
| education      | TEXT      |
| q1 to q10      | INTEGER   |
| interest       | TEXT      |
| value          | TEXT      |
| improvement    | TEXT      |
| next_theme     | TEXT      |
| other_comments | TEXT      |
| submitted_at   | DATETIME  |

Note: `q1 to q10` represents ten separate integer fields for various survey questions.<br>

## Project Flowchart

<img src="https://github.com/user-attachments/assets/b77aa595-11f8-4671-8869-58e8d8e3225f" width="300">


## Project Components

### Step 1: Data Collection GUI
This component is the primary interface for user interaction, enabling participants to provide feedback through various input forms:
- **Personal Information**: Gathers demographic details such as gender, age, occupation, and education level.
- **Satisfaction Survey**: Evaluates participants' satisfaction with different aspects of the event on a scale from 1 (Strongly Disagree) to 5 (Strongly Agree).
- **Open-Ended Questions**: Offers a space for free text responses, allowing users to express their thoughts on what was interesting, suggest improvements, and make other comments.

### Step 2: Fake Data Insertion
A separate Python script is utilized to insert ten fabricated survey responses into the database. This facilitates system testing and demonstration by simulating realistic input data without the need for actual user responses.

### Step 3: Feedback Analysis Tools
This step involves several graphical user interfaces, each designed for a specific type of data analysis and reporting:

#### GUI 2: Personal Information and Satisfaction Analysis
- **Function**: Displays an analysis of the collected personal information and satisfaction levels to quickly assess and interpret participant feedback.

#### GUI 3: Sentiment Analysis and Word Cloud Generation
- **Function**: Performs sentiment analysis on responses to open-ended questions and generates word clouds to visually represent frequently mentioned terms.

#### GUI 4: Data Export Interface
- **Function**: Enables users to export selected data to a CSV file, facilitating external use or further detailed analysis outside the system.

<br>

## GUI Overview

### First GUI: Feedback Survey Screen
This interface is designed for users to input their feedback directly through a survey form.

<img src="https://github.com/user-attachments/assets/0cec76cf-17b2-44fa-855e-00d9b978e5fe" width="500"> <br>
<img src="https://github.com/user-attachments/assets/6a50ca7f-de99-4e4b-9d57-99ec201842b7" width="500">

### Second GUI: Survey Data Analysis
This screen displays an analysis of the collected personal information and satisfaction levels to quickly assess and interpret participant feedback.

<img src="https://github.com/user-attachments/assets/bc3729ec-5042-4b83-adde-d3a0d2abd395" width="400"><br>

<img src="https://github.com/user-attachments/assets/25a1a736-c870-404b-af90-8924107cca03" width="400">

### Third GUI: Sentiment Analysis and Word Cloud Generation
This interface performs sentiment analysis on open-ended survey responses and generates word clouds to visually represent key terms and sentiments.

<img src="https://github.com/user-attachments/assets/89568e95-b12a-4698-8974-3ca4d6303b53" width="300">

### Fourth GUI: Survey Data Viewer
This GUI allows users to view and export the survey data, facilitating further analysis or reporting outside the system.

<img src="https://github.com/user-attachments/assets/df189845-14ca-4afd-8899-32d49096e829" width="300">

