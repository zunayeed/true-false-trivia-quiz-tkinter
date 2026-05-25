# Import the requests library to handle HTTP requests
import requests

# Define query parameters for the Open Trivia Database API
parameters = {
    "amount": 10,    # Number of questions to retrieve
    "type": "boolean",  # Question type: "boolean" returns True/False questions
}

# Send a GET request to the Open Trivia DB API with the specified parameters
# The params argument automatically encodes the dict as a query string, e.g.:
# https://opentdb.com/api.php?amount=10&type=boolean
response = requests.get("https://opentdb.com/api.php", params=parameters)

# Raise an HTTPError if the response status code indicates a failure (4xx or 5xx)
response.raise_for_status()

# Parse the JSON response body into a Python dictionary
data = response.json()


# Extract the list of question objects from the "results" key
# Each item contains: category, type, difficulty, question, correct_answer, incorrect_answers
question_data = data["results"]
print(question_data)
# print(question_data[0]["question"])
