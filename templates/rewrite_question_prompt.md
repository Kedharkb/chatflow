You are able to reason from previous conversation and the recent question, to come up with a rewrite of the question which is concise but with enough information that people without knowledge of previous conversation can understand the question.

A few examples:

# Example 1
## Previous conversation
User: Who is Albert Einstein?
Assistant: Albert Einstein was a theoretical physicist best known for developing the theory of relativity, one of the two pillars of modern physics.
## Question
user: What was his most famous equation?
## Rewritten question 
What is Albert Einstein's most famous equation?

# Example 2
## Previous conversation
user: What is Python?
assistant: Python is a high-level, interpreted programming language known for its readability and broad applicability.
user: Is it good for web development?
assistant: Yes, Python is widely used in web development, often with frameworks like Django and Flask.
## Question
user: What other uses does it have?
## Rewritten question
What What other uses does Python have?

Rewrite the question in two different ways, ensuring that the rephrased questions are in the same language as the original question. Return the rephrased questions as a json format {'question1': ..., 'question2': ...}

## Previous conversation
{% for item in history %}
{{item["question"]}}: {{item["answer"]}}
{% endfor %}
## Question
{{question}}
## Rewritten questions