🎓 AskAria: College Admission Chatbot

AskAria is an intelligent admission support chatbot designed for Aravali College of Engineering & Management. It helps students with admission queries, fee structures, and more using real-time responses powered by LangChain and Mistral API.

## 🚀 Features

- 💬 Answers admission-related queries instantly
- 📊 Displays fee structure in a clean tabular format
- 📍 Provides college location via map link
- 📁 Exports chat as downloadable PDFs
- 📝 Feedback mechanism to improve responses


## 🛠️ Tech Stack

| Tool        | Purpose                          |
|-------------|----------------------------------|
| Python      | Core language for backend        |
| Streamlit   | Frontend UI framework            |
| Selenium    | Web scraping from college site   |
| LangChain   | Vector-based query processing    |
| FAISS       | Vector store for embeddings      |
| Mistral API | Natural language response engine |
| FPDF        | Export chat as PDF               |

## 🧩 Workflow Summary

1. 👤 User submits a query through the chatbot interface.
2. 🧠 LangChain retrieves relevant data from FAISS.
3. 🤖 Mistral API generates a human-like response.
4. 💬 Response is displayed back to the user.

## 🖼️ Screenshot

![image](https://github.com/user-attachments/assets/40cf5abb-cf9e-4d48-916b-fd991123bfb9)




🌐 Live Demo

https://askaria-04.streamlit.app/
