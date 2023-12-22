from django.db import models
from django.contrib.auth.models import User
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')

class FaissIndex:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    index_id = models.CharField(max_length=100, unique=True)
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
    )
    texts = [" "]
    index = FAISS.from_texts(texts,embeddings)
    
    def creates_index(text):
        global index
        # Initialize Faiss index and Hugging Face pipeline

            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=40,
            chunk_overlap=5,
            )
        documents = text_splitter.split_text(text)
        index.add_texts(documents)