from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.docstore.document import Document
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()
vectorstore = Chroma("Prof_vector_store",embedding_function = embeddings)

st.title("Connect2PHD")
interests = st.text_input("Enter your research interests")

# def embed_document(prof_text_info):
#     doc = Document(page_content=prof_text_info[1], metadata={"name": prof_text_info[0]})
#     vectorstore.insert(doc)

extracted_texts = []

for file_name in os.listdir("./Prof_info_docs"):
    print(file_name)
    extracted_text = ""
    with open("./Prof_info_docs/"+file_name, 'r', encoding='iso-8859-1') as file:
        prof_name = file_name[:-4]
        extracted_text = file.read()
    extracted_texts.append(prof_name + "\n" + extracted_text)

print(extracted_texts)
vectorstore.add_texts(extracted_texts)

if interests:
    results = vectorstore.similarity_search(query=interests, k=3)
    for i,res in enumerate(results):
        st.write(f"# Professor {i+1}")
        st.write(res.page_content)