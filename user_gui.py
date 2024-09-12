import os
import asyncio
import tkinter as tk
from tkinter import scrolledtext
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Rag Implementation")

        # Create chat history frame
        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Create chat history area
        self.chat_history = tk.Text(self.chat_frame, wrap='none', height=20, width=50)
        self.chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and hide it
        self.chat_scrollbar = tk.Scrollbar(self.chat_frame)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_scrollbar.config(command=self.chat_history.yview)
        self.chat_history.config(yscrollcommand=self.chat_scrollbar.set)
        
        # Hide the scrollbar by setting its width to 0
        self.chat_scrollbar.pack_forget()  # Set width to 0 and background color to match your app background

        # Create user input area
        self.user_input = tk.Entry(root, width=48)
        self.user_input.pack(pady=10, padx=10, side='left', fill=tk.X, expand=True)

        # Create send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=10, padx=10, side='right')

        # Bind Enter key to send_message method
        self.user_input.bind('<Return>', self.send_message_event)

        # Bind focus in event to select the input area
        self.root.bind('<FocusIn>', self.focus_input)

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("\nYou: " + user_message)
            response = self.get_chatbot_response(user_message)
            self.display_message("Chatbot: " + response)
            self.user_input.delete(0, tk.END)

    def message_receiver(self):
        user_message = self.user_input.get()
        return user_message

    def send_message_event(self, event):
        self.send_message()
        return 'break'  # Prevent default behavior (newline in entry field)

    def display_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

    def focus_input(self, event):
        self.user_input.focus_set()  # Set focus to the user input field

    # LLM Part 

    def get_chatbot_response(self, user_message):
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
            embedding=OpenAIEmbeddings(openai_api_key="sk-proj-ozsRlQGengo3IrYKq1ppT3BlbkFJpftzn4iwQaWpOJPV5oSp"),
        )
        retriever = vectorstore.as_retriever(k=4)

        from langchain_ollama import ChatOllama
        from langchain.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        prompt = PromptTemplate(
            template="""Sen bir döküman uzmanı yapay zeka asistansın.
            Soruyu cevaplamak için aşağıdaki dökümanları kullan.
            Cevabı bilmiyorsan sadece 'Bu konuda bir bilgim yok' de.
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

        question =self.message_receiver()
        answer = rag_application.run(question)
        print("Question:", question)
        print("Answer:", answer)
        return answer

# Create the main window
root = tk.Tk()
app = ChatbotApp(root)

# Run the application
root.mainloop()


