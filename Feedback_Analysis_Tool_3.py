import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

DATABASE_PATH = 'survey_responses.db'

def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM responses", conn)
    conn.close()
    return df

def show_basic_info():
    df = load_data()
    total_responses = len(df)
    incomplete_responses = df[df[['gender', 'age', 'occupation', 'education']].isna().any(axis=1)].shape[0]
    info_text = f"Total Responses: {total_responses}\nIncomplete Surveys: {incomplete_responses}"
    text_basic_info.config(state='normal')
    text_basic_info.delete('1.0', tk.END)
    text_basic_info.insert(tk.END, info_text)
    text_basic_info.config(state='disabled')

def plot_personal_info():
    df = load_data()
    figure, axes = plt.subplots(2, 2, figsize=(10, 8))
    cols = ['gender', 'age', 'occupation', 'education']
    descriptions = []
    for i, col in enumerate(cols):
        ax = axes[i//2, i%2]
        counts = df[col].value_counts()
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title(col + ' Distribution')
        most_common = df[col].mode().iloc[0]
        descriptions.append(f"Most common in {col}: {most_common}")
    plt.tight_layout()
    
    clear_canvas()
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    description_text = "\n".join(descriptions)
    text_info.config(state='normal')
    text_info.delete('1.0', tk.END)
    text_info.insert(tk.END, description_text)
    text_info.config(state='disabled')

def show_correlation():
    df = load_data()
    questions = ['q1', 'q6', 'q7', 'q8', 'q9', 'q10']
    df = df[questions]
    correlation_matrix = df.corr()
    
    fig, ax = plt.subplots()
    cax = ax.matshow(correlation_matrix, cmap='coolwarm')
    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
    fig.colorbar(cax)
    
    clear_canvas()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    high_corr = correlation_matrix.abs() > 0.7
    high_corr_pairs = [(correlation_matrix.columns[i], correlation_matrix.columns[j]) 
                       for i in range(len(correlation_matrix.columns)) 
                       for j in range(i + 1, len(correlation_matrix.columns)) 
                       if high_corr.iloc[i, j]]
    description = "High correlation (>0.7) found between:\n" + "\n".join([f"{pair[0]} and {pair[1]}" for pair in high_corr_pairs])
    
    text_corr_info.config(state='normal')
    text_corr_info.delete('1.0', tk.END)
    text_corr_info.insert(tk.END, description)
    text_corr_info.config(state='disabled')

def clear_canvas():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()

root = tk.Tk()
root.title("Survey Data Analysis")

text_basic_info = tk.Text(root, width=40, height=4)
text_basic_info.pack(pady=(10, 0))
text_basic_info.config(state='disabled')

button_show_info = tk.Button(root, text="Show Personal Info Distribution", command=plot_personal_info)
button_show_info.pack(pady=10)

text_info = tk.Text(root, width=60, height=4)
text_info.pack()
text_info.config(state='disabled')

button_show_corr = ttk.Button(root, text="Show Correlation Analysis", command=show_correlation)
button_show_corr.pack(pady=10)

text_corr_info = tk.Text(root, height=4, width=60)
text_corr_info.pack(pady=(0, 10))
text_corr_info.config(state='disabled')

show_basic_info()

root.mainloop()

def clear_canvas(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()
            
def generate_word_cloud(root):
    df = load_data()
    text = ' '.join(df[['interest', 'value', 'improvement', 'next_theme', 'other_comments']].fillna('').astype(str).sum(axis=1))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    clear_canvas(root)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    plt.close(fig)

def analyze_sentiments(root, text_widget):
    df = load_data()
    sentiments = df[['interest', 'value', 'improvement', 'next_theme', 'other_comments']].fillna('').astype(str).apply(
        lambda x: TextBlob(' '.join(x)).sentiment.polarity, axis=1
    )
    avg_sentiment = sentiments.mean()
    sentiment_text = f"Average sentiment polarity: {avg_sentiment:.2f}"
    text_widget.config(state='normal')
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, sentiment_text)
    text_widget.config(state='disabled')

def setup_gui():
    root = tk.Tk()
    root.title("Survey Data Analysis")

    text_sentiment_analysis = tk.Text(root, height=2, width=40)
    text_sentiment_analysis.pack(pady=(5, 5))
    text_sentiment_analysis.config(state='disabled')

    button_generate_word_cloud = tk.Button(root, text="Generate Word Cloud", command=lambda: generate_word_cloud(root))
    button_generate_word_cloud.pack(pady=10)

    button_analyze_sentiments = tk.Button(root, text="Analyze Sentiments", command=lambda: analyze_sentiments(root, text_sentiment_analysis))
    button_analyze_sentiments.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()

#########################################################
def update_text_display(score):
    df = load_data()
    filtered_df = df[df['q1'] == score]
    
    text_display.config(state='normal')
    text_display.delete('1.0', tk.END)
    
    for index, row in filtered_df.iterrows():
        answers = f"User ID {index}:\n"
        answers += f"- Interesting Part: {row['interest']}\n"
        answers += f"- Valuable Content: {row['value']}\n"
        answers += f"- Improvement: {row['improvement']}\n"
        answers += f"- Next Theme: {row['next_theme']}\n"
        answers += f"- Other Comments: {row['other_comments']}\n\n"
        text_display.insert(tk.END, answers)
    
    text_display.config(state='disabled')

def update_text_display(score):
    global data_to_export  

    df = load_data()
    filtered_df = df[df['q1'] == score]
    data_to_export = filtered_df
    
    text_display.config(state='normal')
    text_display.delete('1.0', tk.END)
    
    for index, row in filtered_df.iterrows():
        answers = f"User ID {index}:\n"
        answers += f"- Interesting Part: {row['interest']}\n"
        answers += f"- Valuable Content: {row['value']}\n"
        answers += f"- Improvement: {row['improvement']}\n"
        answers += f"- Next Theme: {row['next_theme']}\n"
        answers += f"- Other Comments: {row['other_comments']}\n\n"
        text_display.insert(tk.END, answers)
    
    text_display.config(state='disabled')

def export_to_csv():
    if 'data_to_export' in globals():
        data_to_export.to_csv('exported_data.csv', index=False)
        print("Data exported successfully to 'exported_data.csv'")
    else:
        print("No data to export")

root = tk.Tk()
root.title("Survey Data Viewer")

score_label = ttk.Label(root, text="Select Score:")
score_label.pack(pady=(10, 0))
score_var = tk.IntVar()
score_dropdown = ttk.Combobox(root, textvariable=score_var, values=[1, 2, 3, 4, 5])
score_dropdown.pack()
score_dropdown.bind('<<ComboboxSelected>>', lambda event: update_text_display(score_var.get()))

text_display = tk.Text(root, width=80, height=20)
text_display.pack(pady=10)
text_display.config(state='disabled')

export_button = ttk.Button(root, text="Export to CSV", command=export_to_csv)
export_button.pack(pady=10)

root.mainloop()

score_label = ttk.Label(root, text="Select Score:")
score_label.pack(pady=(10, 0))
score_var = tk.IntVar()
score_dropdown = ttk.Combobox(root, textvariable=score_var, values=[1, 2, 3, 4, 5])
score_dropdown.pack()
score_dropdown.bind('<<ComboboxSelected>>', lambda event: update_text_display(score_var.get()))

text_display = tk.Text(root, width=80, height=20)
text_display.pack(pady=10)
text_display.config(state='disabled')

export_button = ttk.Button(root, text="Export to CSV", command=export_to_csv)
export_button.pack(pady=10)

root.mainloop()

