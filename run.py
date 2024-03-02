import chat
import yaml
import argparse


def chat_with_pdf():
    """Generate response based on user query using llm."""
    with open('config.yaml', 'r') as file:
        keys = yaml.safe_load(file)

    parser = argparse.ArgumentParser()
    parser.add_argument('-model', required=True,
                        help='Specify the model to use (e.g., ollama)')
    args = parser.parse_args()
    model_name = args.model

    chat_obj = chat.Chat(keys, model_name)
    chat_obj.main()
chat_with_pdf()
