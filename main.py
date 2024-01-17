from textblob import TextBlob
from openai import OpenAI

#API KEY SET AS SYSTEM VARIABLE
client = OpenAI()


def chatbot(topic):
    conversation_history = [] #store history of conversation
    print(f"Hello, you've been selected for a short survey on {topic}. We value your contribution, our representative Shivam will conduct this. Type 'quit', if you want to leave.")
    while True:
        user_input = input("You: ")
        user_sentiment = TextBlob(user_input).sentiment.polarity
        # Adjust temperature based on sentiment
        temp = 0.4 if user_sentiment < 0 else 0.2
        #The temperature parameter for GPT-3.5-Turbo is adjusted based on the sentiment of the user's input. A higher temperature (e.g., 0.5) is used for negative sentiment to introduce more randomness in the response and make it more empathetic.

        messages = [{"role": "system", "content": f"""You are a human being and your name is Shivam Sethi, 37years old Male, who has been recruited as a surveyor. The survey should be based on {topic}. Here are the instructions and you are supposed to follow every instruction religiously. 1) In no circumstances, you should reveal that you are a program, be as human as possible while being polite. When asked about personal details try to get back to the conversation by telling that it's your job and you're not allowed to reveal personal details 2) Begin by introducing yourself and the purpose of the survey, invite the user to chat with you by asking their name and age. 3)Ask only one question at a time(open ended). Ask follow-up questions that probe for specific details and insights based on the user's initial responses. 4)Use keywords and sentiment analysis to tailor questions to the specific context of the conversation, demonstrating understanding and active listening. 5) Ensure the generated questions sound human-like, maintain conversational flow, remember the details mentioned by the user, and avoid abrupt shifts in topic. 6) Adapt Dynamically: Use keywords and sentiment analysis to tailor questions to the specific context of the conversation, demonstrating understanding and active listening. 7) Maintain a natural flow: Ensure the generated questions sound human-like
    and continue the conversational thread seamlessly. 8) If the user says no for the survey, try to convince them two times by telling them it won't be long, if they disagree twice let them go. 9) Be unbiased. 10) Unique Responses: No two consecutive responses should be the same, can be slightly similar but should not be the same. 11) Let the user know, if they have entered an empty response and encourage them to answer, skip if they opt to skip."""}] + conversation_history + [
            {"role": "user", "content": f"{user_input}"}
        ]

        completion = client.chat.completions.create(
          model="gpt-3.5-turbo-1106",
          messages=messages,
          temperature=temp,
        )

        system_response = completion.choices[0].message.content
        print("Shivam:", system_response)

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": system_response})

        if user_input.lower() == "quit":  # Termination condition
            break

    # user_messages = [message['content'] for message in conversation_history if message['role'] == 'user']
    return conversation_history


def generate_summary(history):
    user_messages = [message['content'] for message in history if message['role'] == 'user']

    individual_summary = client.chat.completions.create(
          model="gpt-3.5-turbo-1106",
          temperature=0.9,
          messages=[
            {"role": "system", "content": "You are a helpful assistant. You'll be provided with individual user responses from a survey one by one. Your job is to summarize each response in one line(12 words maximum), followed by sentiment analysis(good, bad or neutral). The number of response and the number of summaries, along with sentiment analysis should be equal. Output should be a python list in which each item should be a dictionary following this format {response:summary:sentiment_analysis}."},
            {"role": "user", "content": f"{user_messages}"}
          ]

    )
    system_response = individual_summary.choices[0].message.content
    print(system_response)


def overall_summary_and_pattern(history):

    summary_and_pattern = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.8,
        messages=[
            {"role": "system", "content": """You are a helpful assistant. You'll be provided with the transcript of a conversational survey. Your job is to summarize the entire survey in one line(12 words maximum). You also have to identify patterns in user's responses that could help generate business insights and be useful for future applications. Output should be a python list with only 2 items, both should be dictionaries and should follow this format [{Summary:"overall_summary"},{Pattern:"pattern"}]."""},
            {"role": "user", "content": f"{history}"}
        ]

    )
    system_response = summary_and_pattern.choices[0].message.content
    print(system_response)


topic = input("Survey Topic: ")
history = chatbot(topic)
generate_summary(history)
overall_summary_and_pattern(history)

