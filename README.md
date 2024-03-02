# Chat-with-your-pdf
An open-source project leveraging the capabilities of LLM (Large Language Models) and RAG (Retrieval Augmented Generation) to process queries based on PDF data at hand.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
What things you need to install the software and how to install them:
+ Python 3x
+ For running using open-source models, Ollama has to be installed and ruuning in your machine. For more details visit :[Ollama](https://ollama.com/)
+ For running using openai, your open_ai_key has to be configured in the config.json

### Installation
1. Clone the repository:
```git clone https://github.com/ragesh2000/Chat-with-your-pdf.git```

2. Navigate into the project directory:
```cd Chat-with-your-pdf```

3. Install the required dependencies:
```pip install -r requirements.txt```

4. Run the ```run.py``` file:
```python run.py -model openai/ollama```
#### Arguments
```model : Which model you need to use. (currently supports openai and ollama)```


