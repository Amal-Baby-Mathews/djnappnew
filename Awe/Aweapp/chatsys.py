from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests
import google.generativeai as genai
import json
import base64
from PIL import Image
import requests
import io
import os
import time
import requests

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": ""}
qAPI_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
qheaders = {"Authorization": ""}
genai.configure(api_key="")
def image_query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
def query_genai(user_input):
    model = 'gemini-1.0-pro' # @param {isTemplate: true}
    contents_b64 = 'W3sicm9sZSI6InVzZXIiLCJwYXJ0cyI6ImhlbGxvIn0seyJyb2xlIjoibW9kZWwiLCJwYXJ0cyI6IkhlbGxvIHRoZXJlISBIb3cgY2FuIEkgaGVscCB5b3UgdG9kYXk/In1d' # @param {isTemplate: true}
    generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MC45LCJ0b3BfcCI6MSwidG9wX2siOjEsIm1heF9vdXRwdXRfdG9rZW5zIjoyMDQ4LCJzdG9wX3NlcXVlbmNlcyI6W119' # @param {isTemplate: true}
    safety_settings_b64 = 'W3siY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX0hBUkFTU01FTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfSEFURV9TUEVFQ0giLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfU0VYVUFMTFlfRVhQTElDSVQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfREFOR0VST1VTX0NPTlRFTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn1d' # @param {isTemplate: true}

    contents = json.loads(base64.b64decode(contents_b64))
    generation_config = json.loads(base64.b64decode(generation_config_b64))
    safety_settings = json.loads(base64.b64decode(safety_settings_b64))
    stream = False
    gemini = genai.GenerativeModel(model_name=model)

    chat = gemini.start_chat(history=contents)

    response = chat.send_message(
        user_input,
        stream=stream)
    return response.text
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
image_texts = ["image", "create image", "painting", "Make", "draw", "paint", "image generator", "generate"]
image_db=FAISS.from_texts(image_texts,embeddings)
#End embeddings
def save_image(relevance_score, image_bytes, filename="generated_image"):
    """
    Saves the image from `image_bytes` to the local directory, handling errors and potential format issues.

    Args:
        relevance_score: Relevance score for image generation.
        image_bytes: Bytes representing the image data.
        filename: Optional filename for the saved image. Defaults to "generated_image.jpg".

    Returns:
        None
    """
    # Remove all spaces from filename
    filename = filename.replace(" ", "")
    if relevance_score > 0.1:
        print("Relevance for image generation detected:", relevance_score)

        try:
            # Check if response contains valid image data
            if image_bytes:
                # Create local directory if it doesn't exist
                os.makedirs("Aweapp\static\images", exist_ok=True)  # Replace with your desired directory

                # Try to open the image in PIL to determine format (if unknown)
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    # Extract format from image object if available
                    format = image.format if image.format else "JPEG"
                except OSError:
                    # If PIL cannot open, assume raw bytes and use JPEG
                    format = "JPEG"

                # Construct save path
                save_path = os.path.join("Aweapp\static\images", f"{filename}.{format}")

                # Write image data to file
                with open(save_path, "wb") as f:
                    f.write(image_bytes)

                print(f"Image saved successfully to: {save_path}")
            else:
                print("Error: Empty image data received from API.")
        except Exception as e:
            print(f"Error saving image: {e}")
    return save_path
def get_response(input, ind):
    # try:
        global image_db
        db=ind.return_index()
        user_input = input
        PROMPT=user_input
        relevance= image_db.similarity_search_with_relevance_scores(PROMPT)
        for document, relevance_score in relevance:
            if relevance_score > 0.1:
                print("Relevance for image generation detected: ",relevance_score)
                image_bytes = image_query({
                    "inputs": PROMPT,
                })
                # if int(image_bytes)  < 100:
                #     print(image)
                image=save_image(relevance_score, image_bytes)  
                #image=r'Awe\Aweapp\static\images\generated_image.JPEG'
                return image
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
                return output['answer'] 
            except Exception as e:
                    print(f"Error: {e}")
                    print(f"Retrying in 20 seconds...")
                    time.sleep(20)
               
        else:
            print("Normal answer",type(user_input)) 
            output = query_genai(PROMPT)

            print(output)    
            #out=output['generated_text']
            return output
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
      

