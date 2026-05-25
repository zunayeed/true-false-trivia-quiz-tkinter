from tkinter import *
from quiz_brain import QuizBrain

# Background color used throughout the UI (dark teal/blue)
THEME_COLOR = "#375362"


class QuizInterface:
    """
    Builds and manages the Tkinter GUI for the Quizzler app.
    Displays questions on a canvas and handles True/False button interactions.
    """

    def __init__(self, quiz_brain: QuizBrain):
        """
        Initialize the quiz UI window with all widgets and start the main loop.

        Args:
            quiz_brain (QuizBrain): The logic controller that manages questions and scoring.
        """
        # Store the QuizBrain instance to access questions and score
        self.quiz = quiz_brain

        # ─── Window Setup ──────────────────────────────────────────────────────
        self.window = Tk()
        self.window.title("Quizzler")
        # Add padding around all widgets and set background to theme color
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # ─── Score Label ───────────────────────────────────────────────────────
        # Displayed in the top-right corner (row=0, column=1)
        self.score_label = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        # ─── Question Canvas ───────────────────────────────────────────────────
        # White canvas that displays the question text in the center
        self.canvas = Canvas(width=300, height=250, bg="white")

        # Create a text item centered on the canvas at (150, 125)
        # width=280 allows text to wrap before reaching the canvas edge
        self.question_text = self.canvas.create_text(
            150,          # x position (horizontal center)
            125,          # y position (vertical center)
            width=280,    # max width before text wraps to next line
            text="Some Question Text",
            fill=THEME_COLOR,
            font=("Arial", 20, "italic")
        )
        # Place canvas spanning both columns with vertical padding
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)



        # ─── True Button ───────────────────────────────────────────────────────
        # Load the checkmark image for the True button
        # Note: must store as instance variable to prevent garbage collection
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(
            image=true_image,
            activebackground=THEME_COLOR,#remove quick flash of white color that appears when the button is clicked
            highlightthickness=0,        # Remove the default button border highlight
            bd=0,
            command=lambda: self.answer_pressed("True")   # Call answer_pressed() when clicked
        )
        self.true_button.grid(row=2, column=0)




        # ─── False Button ──────────────────────────────────────────────────────
        # Load the cross image for the False button
        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(
            image=false_image,
            activebackground=THEME_COLOR,
            highlightthickness=0,         # Remove the default button border highlight
            bd=0,
            command=lambda: self.answer_pressed("False")    # Call answer_pressed() when clicked
            #Because command= expects a function reference, not a function call. so
            # lambda lets you pass an argument without calling it immediately:
        )
        self.false_button.grid(row=2, column=1)

        # ─── Start Quiz ────────────────────────────────────────────────────────
        # Load and display the first question before entering the main loop
        self.get_next_question()

        # Start the Tkinter event loop — keeps the window open and responsive
        self.window.mainloop()

    # def get_next_question(self):
    #     """
    #     Advance to the next question and update the UI.
    #
    #     - Resets the canvas background to white
    #     - Updates the score label
    #     - Displays the next question text, or an end message if quiz is complete
    #     - Disables both buttons when there are no more questions
    #     """
    #     # Reset canvas background to white (clears red/green feedback color)
    #     self.canvas.config(bg="white")
    #
    #     if self.quiz.still_has_questions():
    #         # Update score label to reflect current score
    #         self.score_label.config(text=f"Score: {self.quiz.score}")
    #
    #         # Get the next question as a formatted string from QuizBrain
    #         q_text = self.quiz.next_question()
    #
    #         # Update the canvas text item with the new question
    #         self.canvas.itemconfig(self.question_text, text=q_text)
    #     else:
    #         # No more questions — show completion message
    #         self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
    #
    #         # Disable both buttons to prevent further interaction
    #         self.true_button.config(state="disabled")
    #         self.false_button.config(state="disabled")

    def get_next_question(self):
        # Reset canvas to white — clears the green/red feedback flash from give_feedback()
        self.canvas.config(bg="white")

        if self.quiz.still_has_questions():
            # Sync score label with QuizBrain's current score after each answer
            self.score_label.config(text=f"Score: {self.quiz.score}")

            # next_question() advances the index and returns formatted string e.g. "Q.3: Is the Earth round?"
            # inlined directly into itemconfig — no need for a separate q_text variable
            self.canvas.itemconfig(self.question_text, text=self.quiz.next_question())
        else:
            # Quiz complete — replace question text with end message
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")

            # Disable both buttons so user can't submit answers after quiz ends
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")


    def answer_pressed(self, user_answer):
        # Check user's answer against correct answer, then show feedback
        is_right = self.quiz.check_answer(user_answer)
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        # is_right (bool) comes from check_answer() in QuizBrain
        # ternary resolves to "green" if correct, "red" if wrong — avoids repeating canvas.config()
        self.canvas.config(bg="green" if is_right else "red")

        # window.after(delay_ms, callback) schedules get_next_question after 1 second
        # non-blocking — unlike time.sleep(), it doesn't freeze the Tkinter UI while waiting
        self.window.after(1000, self.get_next_question)