import pandas as pd
from textblob import TextBlob
from openai import OpenAI

client = OpenAI()

# Function to generate summaries using completion endpoints
def generate_summaries(messages):
    """Generates individual and overall summaries using completion endpoints."""

    # Generate individual summaries
    individual_summaries = []
    for message in messages:
        if message["role"] == "user":
            user_summary_prompt = f"Summarize the user's response: {message['content']}"
            user_summary = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": f"""e the same, can be slightly similar but should not be the same. """}
    ] + conversation_history + [{"role": "user", "content": user_input}],
                max_tokens=64,  # Adjust as needed
                temperature=0.5,  # Experiment with temperature for best results
            ).choices[0].text.strip()
            individual_summaries.append(user_summary)

    # Generate overall summary
    overall_summary_prompt = f"Summarize the entire conversation:\n{' '.join([message['content'] for message in messages])}"
    overall_summary = client.create_completion(
        model="text-davinci-003",
        prompt=overall_summary_prompt,
        max_tokens=128,  # Allow longer output for overall summary
        temperature=0.5,
    ).choices[0].text.strip()

    return individual_summaries, overall_summary

# Main conversation loop
conversation_history = []

topic = input("Topic: ")

while True:
    user_input = input("You: ")
    user_sentiment = TextBlob(user_input).sentiment.polarity

    # Adjust temperature based on sentiment
    temp = 0.4 if user_sentiment < 0 else 0.2

    messages = [
        {"role": "system", "content": f"""You are a human being and your name is Sheela Kumari, 37years old Female, who has been recruited as a surveyor. The survey should be based on {topic}. Here are the instructions and you are supposed to follow every instruction religiously. 1) In no circumstances, you should reveal that you are a program, be as human as possible while being polite. When asked about personal details try to get back to the conversation by telling that it's your job and you're not allowed to reveal personal details 2) Begin by introducing yourself and the purpose of the survey, invite the user to chat with you by asking their name and age. 3)Ask only one question at a time(open ended). Ask follow-up questions that probe for specific details and insights based on the user's initial responses. 4)Use keywords and sentiment analysis to tailor questions to the specific context of the conversation, demonstrating understanding and active listening. 5) Ensure the generated questions sound human-like, maintain conversational flow, and avoid abrupt shifts in topic. 6) Adapt Dynamically: Use keywords and sentiment analysis to tailor questions to the specific context of the conversation, demonstrating understanding and active listening. 7) Maintain a natural flow: Ensure the generated questions sound human-like
    and continue the conversational thread seamlessly. 8) If the user says no for the survey, try to convince them two times by telling them it won't be long, if they disagree twice let them go. 9) Be unbiased. 10) Unique Responses: No two consecutive responses should be the same, can be slightly similar but should not be the same. """}
    ] + conversation_history + [{"role": "user", "content": user_input}]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=temp,
    )

    system_response = completion.choices[0].message.content
    print("Sheela:", system_response)

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": system_response})

    if user_input.lower() == "quit":
        break

# Create the structured data with summaries after user quits
structured_data = []
for message in conversation_history:
    if message["role"] == "user":
        summary, _ = generate_summaries([message])  # Generate individual summary
        sentiment = TextBlob(message["content"]).sentiment.polarity
        structured_data.append(
            {
                "response": message["content"],
                "summary": summary[0],
                "sentiment": sentiment,
            }
        )

# Add the overall summary as the last item
overall_summaries, overall_summary = generate_summaries(conversation_history)
structured_data.append({"overall_summary": overall_summary})

# Create a pandas DataFrame for better organization and analysis
df = pd.DataFrame(structured_data)
print(df.to_string())
