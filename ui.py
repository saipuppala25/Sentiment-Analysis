import tkinter as tk

def on_submit():
    user_input = text_box.get("1.0", "end-1c")
    print("User entered:", user_input)

# Create the main window
root = tk.Tk()
root.title("Text Box Input")

# Create a Text widget
text_box = tk.Text(root, height=5, width=40)
text_box.pack()

# Create a Button to submit text
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

# Run the application
root.mainloop()