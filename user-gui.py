import tkinter as tk
from tkinter import scrolledtext

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Rag Implement")

        # Create chat history area
        self.chat_history = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
        self.chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_history.config(yscrollcommand=lambda *args: None)

        # Create user input area
        self.user_input = tk.Entry(root)
        self.user_input.pack(pady=10, padx=10, side='left', fill=tk.BOTH, expand=True)

        # Bind Enter key to send_message method
        self.user_input.bind('<Return>', self.send_message_event)

        # Create send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=10, padx=10, side='right')

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("You: " + user_message)
            response = self.get_chatbot_response(user_message)
            self.display_message("Chatbot: " + response)
            self.user_input.delete(0, tk.END)

    def send_message_event(self, event):
        self.send_message()
        return 'break'  # Prevent default behavior (newline in entry field)

    def display_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

    def get_chatbot_response(self, user_message):
        # Basic response logic for demonstration
        # Replace this with actual chatbot logic or API call
        return "I'm not sure how to respond to that."

# Create the main window
root = tk.Tk()
app = ChatbotApp(root)

# Run the application
root.mainloop()
