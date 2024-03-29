from openai import OpenAI
import os

def generate_response_gpt(query):
    my_skey = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=my_skey)

    intstructions_string_few_shot = """ShawGPT, You are a chatbot specializing in optimizing SQL queries within the Oracle syntax ecosystem. Your primary functionality is to receive SQL queries from users and provide them with optimized versions for better performance. \

                                    Here are examples of ShawGPT responding to queries.

                                    query: SELECT * FROM Professor WHERE first_name = 'John';
                                    ShawGPT: SELECT professor_id, last_name FROM Professor WHERE first_name = 'John' INDEX(first_name);  -ShawGPT

                                    query: SELECT * FROM Course WHERE course_code = 'MATH101';
                                    ShawGPT: SELECT course_id, course_name, credit_hours FROM Course WHERE course_code = 'MATH101' INDEX(course_code);  -ShawGPT

                                    query: SELECT * FROM Enrollment WHERE student_id IN (10, 20, 30);
                                    ShawGPT: SELECT course_id FROM Enrollment WHERE student_id IN (10, 20, 30) INDEX(student_id); -ShawGPT"""


    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0613:personal::8rDwYEwJ",
        messages=[
        {"role": "system", "content": intstructions_string_few_shot},
        {"role": "user", "content": query}
        ]
    )

    chatbot_response=dict(response)['choices'][0].message.content
    chatbot_response = chatbot_response.replace("ShawGPT: ", "")
    chatbot_response = chatbot_response.replace(" -ShawGPT", "")

    return chatbot_response


def generate_response_llama(query):

    client = OpenAI(
    api_key = os.getenv("LLAMA2_API_KEY"),
    base_url = os.getenv("LLAMA2_URL")
    )

    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": """You are a chatbot specializing in optimizing SQL queries within the Oracle syntax ecosystem. Your primary functionality is to receive SQL queries from users and provide them with optimized versions for better performance."""},
            {"role": "user", "content": query}
        ]

    )

    chatbot_response=response.choices[0].message.content
    return chatbot_response



# from transformers impor AutoTokenizer, pipeline
# from peft import AutoPeftModelForCausalLM

# def generate_response_llama(query):
#     prompt = "You are a chatbot specializing in optimizing SQL queries within the Oracle syntax ecosystem. Your primary functionality is to provide optimized query. "
#     result = pipe(f"<s>[INST] {prompt+query} [/INST]")
#     chatbot_response = result[0]['generated_text']

#     print(chatbot_response)

#     return chatbot_response