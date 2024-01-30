from django.db import models
from django.contrib.auth.models import User
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')

class FaissIndex(models.Model):
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
    text=[" "]
    db= FAISS.from_texts(text,embeddings)
    index=db
    def return_index(self):

        return self.index
    def add_to_index(self,text=""):
        text_splitter = RecursiveCharacterTextSplitter(
               chunk_size=100,
               chunk_overlap=50,
               )
        print("Prompt Inserted:", text)
        documents = text_splitter.split_text(text)
        self.index.add_texts(documents)