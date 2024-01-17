from textblob import TextBlob
from openai import OpenAI

client = OpenAI()
conversation_history = []  # Store conversation history

topic = input("Topic: ")

# Initial message from Sheela to start the conversation
initial_message = {"role": "system", "content": f"Hi there! My name is Sheela Kumari, and I'm conducting a survey about {topic}. Would you be willing to chat with me about your experiences?"}
conversation_history.append(initial_message)

while True:
    user_input = input("You: ")

    messages = conversation_history + [{"role": "user", "content": user_input}]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0.2,
        # prompt=... (Remove the prompt argument if it causes errors)
    )

    system_response = completion.choices[0].message.content
    print("Sheela:", system_response)

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "system", "content": system_response})

    if user_input.lower() == "quit":  # Termination condition
        break
