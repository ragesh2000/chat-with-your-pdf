from langchain.llms import Ollama, OpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings, OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
import os


class Chat():
    """Chat with pdf."""

    def __init__(self, keys, modelname):
        """Init variables."""
        self.keys = keys
        self.model_name = modelname

    def create_db(self, pdf_file):
        """Create vector db."""
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                  chunk_overlap=50)
        texts = splitter.split_documents(documents)

        # create the vector store database
        db = FAISS.from_documents(texts, self.embedding)
        return db

    def create_prompt_template(self):
        """Create langchain prompt template."""
        template = PromptTemplate(
            input_variables=['input', 'context'],
            template="""You are an AI assistant. Use the context below to generate response to queries

            Contexts:
            {context}

            Query: {input}

            """)
        return template

    def load_ollama(self):
        """Load ollama model and embedding."""
        model = self.keys.get('ollama_model')
        self.llm = Ollama(model=model)
        self.embedding = OllamaEmbeddings()

    def load_openai(self):
        """Load gpt model and embedding."""
        apikey = self.keys.get('openai_api_key')
        self.llm = OpenAI(openai_api_key=apikey)
        self.embedding = OpenAIEmbeddings(openai_api_key=apikey)

    def create_chain(self):
        """Create conversation chain."""
        prompt = self.create_prompt_template()

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=False)

        return chain

    def retrieve_context(self, query, db):
        """Retrieve context."""
        retriever = db.as_retriever(search_kwargs={'k': 2})
        documents = retriever.get_relevant_documents(query)
        context = "\n".join([x.page_content for x in documents])
        return context

    def main(self):
        """Process chain with user query."""
        if self.model_name == 'ollama':
            self.load_ollama()
        elif self.model_name == 'openai':
            self.load_openai()
        else:
            print("please provide one among (ollama/ openai) as model")
            return

        pdf_file = input("provide path to pdf file: ")

        if os.path.exists(pdf_file) and pdf_file.lower().endswith('.pdf'):
            pass
        else:
            print('Please provide a valid pdf file ')
            return
        try:
            db = self.create_db(pdf_file)
        except:
            print("Exception in processing pdf file ")
            return
        while True:
            user_query = input("Enter your query: ")
            context = self.retrieve_context(user_query, db)
            chain = self.create_chain()
            res = chain.predict(input=user_query, context=context)
            print("> ", res)
