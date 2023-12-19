from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import requests
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": "Bearer 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"}
qAPI_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
qheaders = {"Authorization": "Bearer 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"}
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
def get_response(input):
    # try:
        global db
        user_input = input
        PROMPT=user_input
        relevant_documents = db.similarity_search_with_relevance_scores(PROMPT)
        answer = []
        text_splitter = RecursiveCharacterTextSplitter(
               chunk_size=100,
               chunk_overlap=50,
               )
        documents = text_splitter.split_text(PROMPT)
        db.add_texts(documents)
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