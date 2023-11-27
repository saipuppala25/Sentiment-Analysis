# used https://realpython.com/python-gui-tkinter/, https://docs.python.org/3/library/tkinter.ttk.html

import tkinter as tk
from tkinter import ttk
from transformers import pipeline

sentiment_analysis_model = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_analysis_model)

website_class_model = "alimazhar-110/website_classification"
website_class_analyzer = pipeline("text-classification", model=website_class_model)

history = []

def submit_for_analysis():
    input_text = text_entry.get("1.0", tk.END).strip()
    
    # get teh results of the used models
    sentiment_result = sentiment_analyzer(input_text)
    website_result = website_class_analyzer(input_text)


    # Print the results of sentiment analysis
    sentiment_label = sentiment_result[0]["label"].capitalize()
    sentiment_score = round(sentiment_result[0]["score"], 2)
    
    sentiment_result_text.set(f"Result: {sentiment_label} statement\nSentiment intensity: {sentiment_score}")

    # Change background color to red if negative, green if positive
    if sentiment_label.lower() == "negative":
        sentiment_color = "#f75f52" # a light red
    elif sentiment_label.lower() == "positive":
        sentiment_color = "#4cf579" # a light green
    else:
        sentiment_color = "#dae86f" # a light yellow

    sentiment_result_label.config(background=sentiment_color)


    # Print results of website analysis
    website_type = website_result[0]["label"]
    website_confidence = round(website_result[0]["score"], 2)
    website_results_text.set(f"Best fit Website category: {website_type} \nConfidence: {website_confidence}")

    history.append((input_text, sentiment_label, sentiment_score))
    update_history_display()

def update_history_display():
    history_text.config(state=tk.NORMAL)  # Enable the widget before updating
    history_text.delete("1.0", tk.END)  # Clear the existing content
    for i, entry in enumerate(reversed(history)):
        input_text, sentiment_label, sentiment_score = entry
        history_text.insert(tk.END, f"{i+1}. \"{input_text}\" - Sentiment: {sentiment_label} ({sentiment_score})\n\n")
    history_text.config(state=tk.DISABLED)  # Disable the widget after updating

# Create the main window
window = tk.Tk()
window.geometry("700x800")
window.title("Sentiment Analyzer")

# setting the style
style = ttk.Style()
style.theme_use("clam")

# creates the frame for the header
header_frame = ttk.Frame(window, padding="10")
header_frame.pack(fill="x")

# header label
header_label = ttk.Label(header_frame, text="Sentiment Analyzer", font=("Helvetica", 16))
header_label.pack()

# frame for user input
text_frame = ttk.Frame(window, padding="10")
text_frame.pack(fill="x")

# user input text box
text_entry = tk.Text(text_frame, width=80, height=10)
text_entry.pack(padx=5, pady=5)

# buttons Frame
buttons_frame = ttk.Frame(window, padding="10")
buttons_frame.pack(fill="x")

# creates analyze button
analyze_button = ttk.Button(buttons_frame, text="Analyze", command=submit_for_analysis)
analyze_button.pack(side="left", padx=5)

# create exit button
exit_button = ttk.Button(buttons_frame, text="Exit", command=window.quit)
exit_button.pack(side="right", padx=5)

# frame for analysis results
result_frame = ttk.Frame(window, padding="10")
result_frame.pack(fill="both", expand=True)

# text output of sentiment analysis
sentiment_result_text = tk.StringVar()
sentiment_result_label = ttk.Label(result_frame, textvariable=sentiment_result_text, font=("Helvetica", 12), background="#DDDDDD", wraplength=500)
sentiment_result_label.pack(padx=5, pady=5, fill="both")

# text output of website classification
website_results_text = tk.StringVar()
website_results_label = ttk.Label(result_frame, textvariable=website_results_text, font=("Helvetica", 12), background="#DDDDDD", wraplength=500)
website_results_label.pack(padx=5, pady=5, fill="both")


# creates history frame
history_frame = ttk.Frame(window, padding="10")
history_frame.pack(fill="both", expand=True)

history_label = ttk.Label(history_frame, text="Analysis History", font=("Helvetica", 12))
history_label.pack()

scrollbar = ttk.Scrollbar(history_frame)
scrollbar.pack(side="right", fill="y")

history_text = tk.Text(history_frame, width=80, height=10, yscrollcommand=scrollbar.set)
history_text.pack(side="left", padx=5, pady=5, fill="both", expand=True)
scrollbar.config(command=history_text.yview)

window.mainloop()
