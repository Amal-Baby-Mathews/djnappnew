from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": "Bearer "}
qAPI_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
qheaders = {"Authorization": "Bearer "}
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
def queryQ(payload):
	response = requests.post(qAPI_URL, headers=qheaders, json=payload)
	return response.json()
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


texts = ["FAISS is an important library", "LangChain supports FAISS", "My passion is to swim"]
db = FAISS.from_texts(texts,embeddings)
#End embeddings
def get_response(input, ind):
    # try:
        db=ind.return_index()
        user_input = input
        PROMPT=user_input
        relevant_documents = db.similarity_search_with_relevance_scores(PROMPT)
        answer = []
        ind.add_to_index(PROMPT)
        for document, relevance_score in relevant_documents:
            if relevance_score > 0.4:
                print(relevance_score,document.page_content)
                answer.append(document.page_content)
        if answer !=[]:
        #!!!!!!!CHANGE MADE HERE TO TEST ^^^^   
            answer = ' '.join(answer)
         
            
            print("Doc answer",type(answer), answer)
            try:
                output = queryQ({
        "inputs": {
            "question": PROMPT,
            "context": answer
        },
    })
                print(output)
                return output['answer'] 
            except Exception as e:
                    print(f"Error: {e}")
                    print(f"Retrying in 20 seconds...")
                    time.sleep(20)
               
        else:
            print("Normal answer",type(user_input)) 
            output = query({
            "inputs": {"past_user_inputs": [""],
            "generated_responses": [""],
            "text": PROMPT

            },
            })

            print(output['generated_text'])    
            out=output['generated_text']
            return out
    # except KeyError:
        # print("KeyError: 'user_input' not found in form data")
        # return "Error: 'user_input' not found in form data", 400
import PyPDF2
import csv

def extract_text_from_file(file_path):
    """
    Extracts text data from a file if it is a PDF, CSV, or .txt file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: Extracted text data from the file or an empty string if extraction is not possible.
    """

    # Check the file extension and process accordingly
    if file_path.endswith('.pdf'):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ''

    elif file_path.endswith('.csv'):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                text = ''
                reader = csv.reader(csvfile)
                for row in reader:
                    text += ' '.join(row) + '\n'
                return text
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return ''

    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ''

    else:
        print("Unsupported file format. Please upload a file of type: PDF, CSV, or .txt")
        return ''
      

