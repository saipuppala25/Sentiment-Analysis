import tkinter as tk
from tkinter import ttk, messagebox
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analysis_model = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_analysis_model)

website_class_model = "alimazhar-110/website_classification"
website_class_analyzer = pipeline("text-classification", model=website_class_model)

# History list to store past results
history = []

def submit_for_analysis():
    input_text = text_entry.get("1.0", tk.END).strip()
    if input_text:
        try:
            sentiment_result = sentiment_analyzer(input_text)
            website_result = website_class_analyzer(input_text)

            # Sentiment analysis results
            sentiment_label = sentiment_result[0]["label"].capitalize()
            sentiment_score = round(sentiment_result[0]["score"], 3)
            sentiment_color = "#FFCCCC" if sentiment_label.lower() == "negative" else "#CCFFCC"
            sentiment_result_text.set(f"Sentiment: {sentiment_label} statement\nScore: {sentiment_score}")
            sentiment_result_label.config(background=sentiment_color)

            # Website classification results
            website_type = website_result[0]["label"]
            website_confidence = round(website_result[0]["score"], 3)
            website_results_text.set(f"Website Category: {website_type}\nConfidence: {website_confidence}")

            # Update history
            history.append((input_text, sentiment_label, sentiment_score, website_type, website_confidence))
            update_history_display()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            sentiment_result_text.set("")
            website_results_text.set("")
    else:
        messagebox.showinfo("Info", "Please enter some text to analyze.")

def update_history_display():
    history_text.config(state=tk.NORMAL)  # Enable the widget before updating
    history_text.delete("1.0", tk.END)  # Clear the existing content
    for i, entry in enumerate(reversed(history)):
        input_text, sentiment_label, sentiment_score, website_type, website_confidence = entry
        history_text.insert(tk.END, f"{i+1}. \"{input_text}\" - Sentiment: {sentiment_label} ({sentiment_score}), Website Category: {website_type} (Confidence: {website_confidence})\n\n")
    history_text.config(state=tk.DISABLED)  # Disable the widget after updating

# Create the main window
window = tk.Tk()
window.geometry("700x1000")  # Adjusted height to accommodate additional features
window.title("Sentiment and Website Category Analyzer")

# Styling
style = ttk.Style()
style.theme_use('clam')

# Header Frame
header_frame = ttk.Frame(window, padding="10")
header_frame.pack(fill='x')
header_label = ttk.Label(header_frame, text="Sentiment and Website Category Analyzer", font=("Helvetica", 16))
header_label.pack()

# Text Entry Frame
text_frame = ttk.Frame(window, padding="10")
text_frame.pack(fill='x')
text_entry = tk.Text(text_frame, width=80, height=10)
text_entry.pack(padx=5, pady=5)

# Buttons Frame
buttons_frame = ttk.Frame(window, padding="10")
buttons_frame.pack(fill='x')
analyze_button = ttk.Button(buttons_frame, text="Analyze", command=submit_for_analysis)
analyze_button.pack(side='left', padx=5)
exit_button = ttk.Button(buttons_frame, text="Exit", command=window.quit)
exit_button.pack(side='right', padx=5)

# Result Frame
result_frame = ttk.Frame(window, padding="10")
result_frame.pack(fill='both', expand=True)

sentiment_result_text = tk.StringVar()
sentiment_result_label = ttk.Label(result_frame, textvariable=sentiment_result_text, font=("Helvetica", 12), background="#DDDDDD", wraplength=500)
sentiment_result_label.pack(padx=5, pady=5, fill='both')

website_results_text = tk.StringVar()
website_results_label = ttk.Label(result_frame, textvariable=website_results_text, font=("Helvetica", 12), background="#DDDDDD", wraplength=500)
website_results_label.pack(padx=5, pady=5, fill='both')

# History Frame
history_frame = ttk.Frame(window, padding="10")
history_frame.pack(fill='both', expand=True)

history_label = ttk.Label(history_frame, text="Analysis History", font=("Helvetica", 12))
history_label.pack()

scrollbar = ttk.Scrollbar(history_frame)
scrollbar.pack(side='right', fill='y')

history_text = tk.Text(history_frame, width=80, height=10, yscrollcommand=scrollbar.set)
history_text.pack(side='left', padx=5, pady=5, fill='both', expand=True)
scrollbar.config(command=history_text.yview)

window.mainloop()
