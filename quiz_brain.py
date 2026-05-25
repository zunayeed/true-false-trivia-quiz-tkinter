import html  # Used to decode HTML entities in question text (e.g., &quot; → ", &#039; → ')


class QuizBrain:
    """
    Manages the quiz logic: tracking progress, serving questions,
    and checking answers.
    """

    def __init__(self, q_list):
        """
        Initialize the QuizBrain with a list of question objects.

        Args:
            q_list (list): A list of Question objects, each having .text and .answer attributes.
        """
        self.question_number = 0        # Tracks the index of the current question (starts at 0)
        self.score = 0                  # Counts the number of correct answers
        self.question_list = q_list     # Stores the full list of Question objects
        self.current_question = None    # Holds the Question object currently being asked

    def still_has_questions(self):
        """
        Check whether there are more questions left in the quiz.

        Returns:
            bool: True if there are unanswered questions remaining, False otherwise.
        """
        return self.question_number < len(self.question_list)

    def next_question(self):
        # Fetch question at current index, then increment counter for the next call
        # use current value first (as index), then advance — so Q.1 displays as question_number=1 after increment
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1

        # html.unescape() converts HTML entities → readable characters
        # e.g. &quot; → ", &amp; → &, &#039; → '
        # necessary because Open Trivia DB returns HTML-encoded strings
        # inlined directly into f-string — no need for a separate q_text variable
        return f"Q.{self.question_number}: {html.unescape(self.current_question.text)}"




    def check_answer(self, user_answer):
        # .lower() on both sides makes comparison case-insensitive
        # e.g. "True", "TRUE", "true" all match "true" from the data
        is_right = user_answer.lower() == self.current_question.answer.lower()

        # Only increment score if answer is correct — bool acts as 0/1 in arithmetic
        # self.score += True → adds 1, self.score += False → adds 0
        self.score += is_right

        # Return the bool directly — no need for an if/else just to return True or False
        return is_right