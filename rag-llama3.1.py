from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

reader = PdfReader("/Users/aliardafincan/Development/RAG-Implementation/T3AI_HACKATHON_ŞARTNAMESİ_IZQ61.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=100
)

doc_splits = text_splitter.split_text(text)

from langchain_community.vectorstores import SKLearnVectorStore
from langchain_openai import OpenAIEmbeddings

vectorstore = SKLearnVectorStore.from_texts(
    texts=doc_splits,
    embedding=OpenAIEmbeddings(openai_api_key="openai_api_key"),
)
retriever = vectorstore.as_retriever(k=4)

from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate(
    template="""Sen bir döküman uzmanı yapay zeka asistansın.
    Soruyu cevaplamak için aşağıdaki dökümanları kullan.
    Cevabı bilmiyorsan sadece bilmiyorum de.
    Question: {question}
    Documents: {documents}
    Answer:
    """,
    input_variables=["question", "documents"],
)


llm = ChatOllama(
    model="llama3.1",
    temperature=0.2,
)

rag_chain = prompt | llm | StrOutputParser()


class RAGApplication:
    def __init__(self, retriever, rag_chain):
        self.retriever = retriever
        self.rag_chain = rag_chain
    def run(self, question):
        documents = self.retriever.invoke(question)
        doc_texts = "\\n".join([doc.page_content for doc in documents])
        answer = self.rag_chain.invoke({"question": question, "documents": doc_texts})
        return answer
    

rag_application = RAGApplication(retriever, rag_chain)

question = input("Sorunuzu yazınız: ")
answer = rag_application.run(question)
print("Question:", question)
print("Answer:", answer)