import itertools
import os
from pathlib import Path

import numpy as np
from openai import OpenAI
from groq import Groq

import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

MODEL_ENGINE = "mixtral-8x7b-32768" # "gpt-3.5-turbo" 
load_dotenv()
# client = OpenAI(api_key=os.environ['OPEN_API_KEY'])
# Replacing OpenAI with Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
CSV_FILE_PATH = Path(__file__).parent.resolve() / "PRT-schemes.csv"


def read_pension_data_from_csv(filepath: str):
    pension_data = pd.read_csv(filepath).dropna()
    return pension_data

def get_embeddings_model():
    embeddings_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # multi-language model
    return embeddings_model


def build_embeddings_from_csv(pension_data):
    embeddings_model = get_embeddings_model()
    # limit the scope of the CSV to named fields if needed
    # descriptions = project_data[["Pension Scheme ID",  "Scheme Name", "Type", "Investment Strategy", "Management", "Employee Contributions",  "Employer Contributions", "Retirement Age"]]
    descriptions = pension_data
    embedding = embeddings_model.encode(descriptions["Descriptions"], convert_to_tensor=False)
    return embedding


def compare_requirements(requirements: str, description_embeddings, num_results: int, descriptions):
    embeddings_model = get_embeddings_model()
    encoded_sentence = embeddings_model.encode(requirements, convert_to_tensor=False)
    new_sentence_scores = util.cos_sim(description_embeddings, encoded_sentence)
    pairs = {}
    for i in range(descriptions.shape[0]):
        pairs[descriptions["Pension Scheme ID"][i]] = new_sentence_scores[i][0].item()

    ordered = dict(sorted(pairs.items(), key=lambda item: item[1], reverse = True))
    top = dict(itertools.islice(ordered.items(), num_results))

    return top


def ask_chatgpt(user_query, embedding, pension_data):

    top = compare_requirements(
        requirements = user_query,
        description_embeddings = embedding,
        num_results = 4,
        descriptions = pension_data
      )

    rag_context = ""
    for project_id in top.keys():
        mask = (pension_data["Pension Scheme ID"] == project_id)
        project = pension_data[mask].reset_index(drop=True)
        project_name = project["Scheme Name"][0]
        project_desc = project["Descriptions"][0]

        rag_context += project_name + '\n' + project_desc + '\n' + str(top[project_id]) + "\n\n"

    response = client.chat.completions.create(model=MODEL_ENGINE,
    n=1,
    messages=[
        {"role": "system", "content": f'''
                You are a chatbot responding to queries from employees interested in opting for various Pension schemes. You should offer advice on which Pension scheme to choose from based on the available pension schemes in the UK. You will be provided with information to inform your responses - please only use this information when formulating your response.

                  examples=[
                    input_text="""I am an employee receiving £75000 annually, I would like to opt for a pension scheme where the employer contribution is the highest""",
                    output_text="""Since you are interested in the pension scheme with the highest employer contribution, the alpha pension scheme would be the best fit. The employer contributions for the alpha pension scheme is 27.10% with the retirement age being the state retirement age or 65 years. To learn more about the pension scheme visit https://www.civilservicepensionscheme.org.uk/knowledge-centre/pension-schemes/alpha-scheme-guide/"""
                  ]

                  Here are the top related pension schemes:
                  {rag_context}


            '''},
        {"role": "user", "content": f'''
                
                Here is the user query:
                  {user_query}
            '''},
    ])

    message = response.choices[0].message
    return message.content



if __name__ == '__main__':

    pension_data = read_pension_data_from_csv(CSV_FILE_PATH)
    embedding = build_embeddings_from_csv(pension_data)
    question  = input("Enter the question: ")
    '''
     Sample Question: I am an employee of XYZ, recommend the pension schemes that have the highest employer contribution
     
     Sample Output (with Groq): 
        If you are an employee looking for a pension scheme with the highest employer contribution, the Alpha pension scheme would be the best fit. The employer contributions for the Alpha pension scheme is 27.10%, which is higher than the other pension schemes provided. The Alpha pension scheme is a Defined Benefit (DB) scheme with a diversified portfolio, active management, variable employee contributions based on salary, and a retirement age of the state pension age or 65.
        To learn more about the Alpha pension scheme, you can visit the following guide: <https://www.civilservicepensionscheme.org.uk/knowledge-centre/pension-schemes/alpha-scheme-guide/>

        Alternatively, the other pension schemes, such as the Premium, Classic, and Nuvos schemes, also have variable and generous employer contributions. However, the employer contribution rates for these schemes are not fixed, unlike the Alpha pension scheme, which has a fixed employer contribution rate of 27.10%.

        Overall, based on the information provided, the Alpha pension scheme offers the highest fixed employer contribution rate, making it the pension scheme with the highest employer contribution.
    '''
    try:
        print(ask_chatgpt(question, embedding, pension_data))
    except Exception as e:
        print("Encountered an exception", e)
