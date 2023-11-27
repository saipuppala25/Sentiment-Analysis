# Received a lot of assistance from: https://realpython.com/python-gui-tkinter/

import tkinter as tk
from transformers import pipeline

sentiment_analysis_model = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"

sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_analysis_model)

def submit_for_analysis():
    input = text_entry.get("1.0", tk.END)

    # Analyze input with emotional intent
    
    res = sentiment_analyzer(input)
    print(res)

    # if would be received negatively, suggest less controversial alternative

    # Use a website classification to tell the user where their post would likely fit the best
    print("User entered:", input)

# Create the window
window = tk.Tk()
window.geometry("600x600")
header = tk.Label(text="Sentiment Analyzer" )
header.pack()

# Creates text box for user to input their post they wish to analyze
text_entry = tk.Text(window, width="70", height="7")
text_entry.pack()

# Analyze button, calls the submit_for_analysis
analyze_button = tk.Button(window, text="Analyze", width="7", height="2", command=submit_for_analysis)
analyze_button.pack()

window.mainloop()