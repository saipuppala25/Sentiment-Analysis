import tkinter as tk
from tkinter import ttk, messagebox
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analysis_model = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_analysis_model)

# History list to store past results
history = []

def submit_for_analysis():
    input_text = text_entry.get("1.0", tk.END).strip()
    if input_text:
        try:
            res = sentiment_analyzer(input_text)
            label = res[0]['label'].capitalize()
            score = round(res[0]['score'], 3)
            result_text.set(f"Result: {label} statement\nStatement's score: {score}")
            color = "#FFCCCC" if label.lower() == "negative" else "#CCFFCC"
            result_label.config(background=color)
            
            # Update history by appending new entries
            history.append((input_text, label, score))
            
            # Update the history display
            update_history_display()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            result_text.set("")
    else:
        messagebox.showinfo("Info", "Please enter some text to analyze.")

def update_history_display():
    history_text.config(state=tk.NORMAL)  # Enable the widget before updating
    history_text.delete("1.0", tk.END)  # Clear the existing content
    for i, entry in enumerate(reversed(history)):
        input_text, label, score = entry
        history_text.insert(tk.END, f"{i+1}. \"{input_text}\" - {label} ({score})\n\n")
    history_text.config(state=tk.DISABLED)  # Disable the widget after updating

# Create the main window
window = tk.Tk()
window.geometry("700x900")  # Increased height to accommodate history area
window.title("Sentiment Analyzer")

# Styling
style = ttk.Style()
style.theme_use('clam')

# Header Frame
header_frame = ttk.Frame(window, padding="10")
header_frame.pack(fill='x')

header_label = ttk.Label(header_frame, text="Sentiment Analyzer", font=("Helvetica", 16))
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

result_text = tk.StringVar()
result_label = ttk.Label(result_frame, textvariable=result_text, font=("Helvetica", 12), background="#DDDDDD", wraplength=500)
result_label.pack(padx=5, pady=5, fill='both')

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