# ============================================================
# main.py — Entry point of the Quiz Application
# Responsibilities:
#   1. Build the question bank from raw data
#   2. Initialize the quiz logic (QuizBrain)
#   3. Launch the GUI (QuizInterface)
# ============================================================

# --- Imports ---
from question_model import Question      # Question class: holds text + correct answer
from data import question_data           # Raw list of question dicts fetched from Open Trivia DB
from quiz_brain import QuizBrain         # Handles quiz logic: scoring, progression, answer checking
from ui import QuizInterface             # Tkinter GUI: displays questions and handles user interaction

# ============================================================
# STEP 1: Build the Question Bank
# ============================================================
# question_bank will hold a list of Question objects (not raw dicts)
# We convert raw dict data → structured Question objects for cleaner access
question_bank = []

for question in question_data:
    # Each 'question' here is a dict from data.py, e.g.:
    # {
    #   "question": "What is 2+2?",
    #   "correct_answer": "True",
    #   ...other fields we don't need...
    # }

    # Extract just the fields we care about
    question_text = question["question"]        # The actual question string
    question_answer = question["correct_answer"]  # "True" or "False"

    # Create a Question object using the model class
    # This wraps the text + answer into a clean reusable object
    new_question = Question(question_text, question_answer)

    # Add the Question object to our bank list
    question_bank.append(new_question)

# At this point, question_bank = [Question(...), Question(...), ...]
# Ready to be passed into QuizBrain

# ============================================================
# STEP 2: Initialize Quiz Logic
# ============================================================
# QuizBrain receives the full question bank and manages:
#   - Which question we're on (question_number)
#   - The user's current score
#   - Whether there are more questions left (still_has_questions())
#   - Answer validation (check_answer())
quiz = QuizBrain(question_bank)

# ============================================================
# STEP 3: Launch the GUI
# ============================================================
# QuizInterface takes the quiz brain as input so it can:
#   - Pull the next question to display
#   - Pass user's True/False button clicks to QuizBrain for checking
#   - Show score feedback and end screen when quiz is complete
# NOTE: This line starts the Tkinter mainloop — the app runs from here
quiz_ui = QuizInterface(quiz)