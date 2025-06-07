# import openai as ai
# ai.api_key="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"

# def chat(prompt):
#     response=ai.ChatCompletion.create(
#         engine_required="gpt-3.5-turbo",
#         messages=[{"role":"user","content":prompt}]
#     )

#     return response.choices[0].message.content.strip()

# if __name__ == "__main__":
#     while True:
#         user_input=input("You:")
#         if user_input.lower() in ["leave", "resign", "depart","withdraw", "retire", "vacate","goodbye", "farewell", "adios", "cheerio", "see you later"]:
#             break
#         response=chat(user_input)
#         print("bot:",response)
import openai

# Set your OpenAI API key
api_key = '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'
openai.api_key = api_key


def chat(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()


def main():
    print("Welcome to the ChatBot!")
    print("You can start chatting. Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("ChatBot: Goodbye!")
            break

        response = chat(user_input)
        print("ChatBot:", response)


if __name__ == "__main__":
    main()
