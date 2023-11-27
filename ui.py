import tkinter as tk
from tkinter import ttk
from transformers import pipeline

sentiment_analysis_model = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_analysis_model)

def submit_for_analysis():
    input_text = text_entry.get("1.0", tk.END)
    try:
        res = sentiment_analyzer(input_text)
        # Assuming 'res' is a list of dictionaries, we take the first result
        label = res[0]['label'].capitalize()  # Capitalize the label
        score = round(res[0]['score'], 3)  # Round the score to 3 decimal places
        
        # Update the result label with a more user-friendly format
        result_text.set(f"Result: {label} statement\nStatement's score: {score}")
        # Change the background color based on the sentiment
        color = "#FFCCCC" if label.lower() == "negative" else "#CCFFCC"
        result_label.config(background=color)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        result_text.set("")

# Create the main window
window = tk.Tk()
window.geometry("700x800")
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

window.mainloop()
