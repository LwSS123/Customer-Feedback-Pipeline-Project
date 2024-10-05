import sqlite3
import random
from faker import Faker

conn = sqlite3.connect('survey_responses.db')
c = conn.cursor()

# Clear existing data from the 'responses' table
# c.execute('DELETE FROM responses')
# conn.commit()
# print("Existing data removed from the table.")

# Create a Faker instance
fake = Faker()

def random_score():
    return random.randint(1, 5)

# Open-ended responses lists
interest_responses = [
    "The interactive workshop where we could apply the principles we learned in real-time. It made the learning experience very tangible and memorable.",
    "The keynote speech by Dr. Smith, whose insights into industry trends were enlightening and provoking.",
    "The panel discussion on the future of technology in healthcare, as it included diverse perspectives from leading experts in the field.",
    "The live demonstration of the new software, showcasing its capabilities and potential applications in our work.",
    "The networking session at the end of the event, which provided a great opportunity to connect with peers and industry leaders.",
    "The breakout sessions that allowed for deeper discussion on specific topics with smaller groups.",
    "The Q&A sessions that followed each presentation, providing clarity and further insights into complex topics.",
    "The hands-on activities that encouraged active participation and learning by doing, rather than just listening.",
    "The virtual reality setup that was used to demonstrate new architectural visualization tools.",
    "The award ceremony celebrating innovative projects in the community, which was both inspiring and motivating."
]

value_responses = [
    "The comprehensive overview of recent advancements in renewable energy technologies presented during the first session.",
    "The detailed case studies shared by industry veterans, which highlighted practical challenges and solutions.",
    "The resource materials and references provided, which will be useful for ongoing learning and application.",
    "The expert tips on project management in high-pressure environments, which are immediately applicable to my job.",
    "The insights into regulatory changes and how they will affect our industry, helping us to prepare ahead.",
    "The data analysis techniques demonstrated, which I can now integrate into my work to enhance our project outcomes.",
    "The leadership strategies for remote teams, which are particularly relevant in the current work-from-home culture.",
    "The marketing session that discussed innovative approaches to customer engagement in the digital age.",
    "The discussions on sustainability practices, offering practical steps our company can take to improve our environmental footprint.",
    "The personal development workshop that focused on building resilience and adaptability in a fast-changing industry."
]

improvement_responses = [
    "More hands-on workshops to apply learned concepts in real-world scenarios, enhancing the practical value of the event.",
    "Additional networking opportunities structured around specific interest areas to facilitate more targeted connections.",
    "A follow-up webinar series to continue discussions on key topics and track implementation progress of learned strategies.",
    "Interactive polls and live feedback during sessions to gauge audience understanding and adjust the pace of presentations.",
    "Translation services or subtitles for presentations, making them accessible to a non-English speaking audience.",
    "A mobile app for the event that includes schedules, speaker bios, session materials, and interactive features.",
    "Longer breaks between sessions to allow for more informal interactions and discussions among attendees.",
    "Childcare facilities for attendees bringing families, encouraging wider participation.",
    "Sessions that focus more on case studies and less on theoretical concepts, to bridge the gap between theory and practice.",
    "Better food options catering to a wider range of dietary preferences and restrictions."
]

next_theme_responses = [
    "Innovations in Sustainable Technology: Navigating the Future of Green Solutions.",
    "Global Health Challenges and Technological Advances in Medicine.",
    "The Impact of Artificial Intelligence on Society: Opportunities and Ethical Considerations.",
    "The Future of Remote Work: Strategies for Effective Management and Employee Engagement.",
    "Emerging Trends in Cybersecurity: Protecting Digital Assets in an Interconnected World.",
    "Revolutionizing Education Through Technology: From K-12 to Higher Education.",
    "Building Inclusive Workplaces: Strategies for Diversity, Equity, and Inclusion.",
    "The Next Frontier in Space Exploration: Opportunities for Research and Innovation.",
    "Financial Technology Innovations: Streamlining Banking and Finance for the Next Decade.",
    "Creative Industries and the Digital Economy: New Paths for Artistic and Economic Growth."
]

other_comments_responses = [
    "Overall, a well-organized event, but could benefit from more detailed session descriptions in the program.",
    "Appreciated the expertise of the speakers but would love to see more young innovators and startups featured next time.",
    "Consider reducing the use of disposable plastics at the event to align with sustainability themes.",
    "The venue was excellent, though some of the rooms were a bit too small for popular sessions.",
    "Please consider starting the day later; the early start was challenging for those commuting from afar.",
    "The technical difficulties during some sessions disrupted the flow; having a tech rehearsal might prevent this in the future.",
    "The inclusion of more practical takeaways and toolkits would make the implementation of ideas smoother.",
    "Would appreciate more interactive and dynamic presentation styles to keep the audience engaged throughout long sessions.",
    "The registration process was smooth, but on-site sign-ins were congested. Maybe open more registration desks next time.",
    "The event app was helpful but had some bugs that need fixing. Also, push notifications for session changes would be useful."
]

# Function to generate a single response
def generate_response(i):
    return (
        random.choice(["Male", "Female"]),
        random.choice(["13-19", "20-29", "30-39", "40-49", "50-59", "60+"]),
        random.choice(["Student", "Government/Military/Public Service", "Service Industry", "Business/Industrial", "Self-Employed", "Homemaker", "Retired", "Other"]),
        random.choice(["Elementary School", "Junior High School", "High School/Diploma", "College/University", "Master's Degree"]),
        *[random_score() for _ in range(10)],
        interest_responses[i],
        value_responses[i],
        improvement_responses[i],
        next_theme_responses[i],
        other_comments_responses[i]
    )

# Create database connection and cursor
conn = sqlite3.connect('survey_responses.db')
c = conn.cursor()

# Generate and insert 10 responses
for i in range(10):
    response = generate_response(i)
    c.execute('''
    INSERT INTO responses (
        gender, age, occupation, education, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
        interest, value, improvement, next_theme, other_comments
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', response)

conn.commit()
print("10 responses have been generated and inserted into the database.")

conn.close()
