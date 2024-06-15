import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random

# Function to read the CSV file and create a dictionary
def read_csv(file_path):
    word_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames  # Get the column names from the header row

        for row in reader:
            expression = row[fieldnames[0]]  # Assuming the first column is the expression
            word_dict[expression] = {
                'kana': row[fieldnames[1]],  # Assuming the second column is the kana
                'type': row[fieldnames[2]],  # Assuming the third column is the type
                'accent': row[fieldnames[3]],  # Assuming the fourth column is the accent
                'chinese_meaning': row[fieldnames[4]],  # Assuming the fifth column is the Chinese meaning
                'verb_type': row[fieldnames[5]]  # Assuming the sixth column is the verb type
            }
    return word_dict

# Function to run the quiz
def run_quiz():
    global current_word, filtered_words, score, total_questions
    if not filtered_words:
        return

    expression, word_info = current_word
    kana = word_info['kana']
    user_input = entry.get().strip()
    if user_input == kana:
        result_label.config(text=f"Correct! The Hiragana for {expression} is '{kana}'.")
        score += 1
    else:
        result_label.config(text=f"Incorrect. The Hiragana for {expression} is '{kana}', NOT '{user_input}'.")

    filtered_words.pop(expression)
    total_questions -= 1
    if not filtered_words:
        messagebox.showinfo("Quiz Completed", f"Your score: {score}/{total_questions + score}")
        reset_quiz()
    else:
        next_word()

# Function to display the next word
def next_word():
    global current_word
    current_word = random.choice(list(filtered_words.items()))
    expression, word_info = current_word
    kana = word_info['kana']
    question_label.config(text=f"Enter the Hiragana for '{expression}':")
    entry.delete(0, tk.END)

# Function to reset the quiz
def reset_quiz():
    global filtered_words, score, total_questions
    filtered_words = {}
    score = 0
    total_questions = 0
    question_label.config(text="")
    entry.delete(0, tk.END)
    result_label.config(text="")

# Function to open the CSV file and select word type
def open_file():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        global word_dict, filtered_words, total_questions
        word_dict = read_csv(file_path)
        word_types = sorted(set(info['type'] for info in word_dict.values()))
        word_type = select_word_type(word_types)
        if word_type:
            if word_type == 'All':
                filtered_words = word_dict
            else:
                filtered_words = {expression: info for expression, info in word_dict.items() if info['type'] == word_type}
            total_questions = len(filtered_words)
            next_word()

# Function to select word type from a dropdown menu
def select_word_type(word_types):
    root = tk.Toplevel(main_window)
    root.title("Select Word Type")

    selected_type = tk.StringVar()
    selected_type.set('All')

    type_dropdown = ttk.Combobox(root, textvariable=selected_type, values=['All'] + list(word_types), state='readonly')
    type_dropdown.pack(pady=10)

    confirm_button = tk.Button(root, text="Confirm", command=lambda: root.destroy())
    confirm_button.pack(pady=10)

    root.grab_set()
    root.wait_window()

    return selected_type.get()

# Create the main window
main_window = tk.Tk()
main_window.title("Hiragana Quiz")

# Create the file open button
open_button = tk.Button(main_window, text="Open CSV File", command=open_file)
open_button.pack(pady=10)

# Create the question label
question_label = tk.Label(main_window, text="", font=("Arial", 16))
question_label.pack(pady=10)

# Create the entry field
entry = tk.Entry(main_window, font=("Arial", 16))
entry.pack(pady=10)
entry.bind("<Return>", lambda event: run_quiz())

# Create the result label
result_label = tk.Label(main_window, text="", font=("Arial", 14))
result_label.pack(pady=10)

# Initialize variables
word_dict = {}
filtered_words = {}
current_word = None
score = 0
total_questions = 0

# Run the main loop
main_window.mainloop()