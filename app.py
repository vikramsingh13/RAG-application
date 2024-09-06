import os
from openai import OpenAI
from dotenv import load_dotenv
import pymupdf
import json



# Load the enviroment variables from .env
load_dotenv()

# Create a new OpenAI client with the API key
client = OpenAI(
    # Set the API key from the enviroment variable
    api_key=os.getenv("OPENAI_API_KEY"),
)

def pdf_to_text(pdf_path: str):
    try:
        # Limit the pages for now to avoid going over the GPT token limit
        max_pages = 25
        # Open the pdf file for processing
        pdf = pymupdf.open(pdf_path)
        # Initialize the variable text that will store the text from the pdf
        text = ""
        # Loop through each page in the pdf and extract the text
        for page in pdf:
            # Add the text from the page to the text variable
            text += page.get_text()
            # Decrement the max_pages by 1 after processing a page
            max_pages -= 1
            # Break the loop if the max_pages is less than or equal to 0
            if max_pages <= 0:
                break

        # Close the pdf file after processing
        pdf.close()
        # Finally, return the text extracted from the pdf
        return text
    except:
        print("app.py::pdf_to_text: Error reading the pdf file.\n")
        return None

def get_chat_response(prompt: str, model: str = "gpt-3.5-turbo"):
    # Create a openai chat completion with the prompt and model
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )

    # Return the message content from the first choice of the chat completion
    return chat_completion.choices[0].message.content

def get_prompt_template(template_name: str = 'text_qa_template'):
    try:
        # Read JSON data to get the prompt template
        with open("prompts/zero_shot_templates.json", 'r') as file:
            # Load the JSON template file into a dictionary
            data = json.load(file)
            # Get the template from the dictionary with the template name
            prompt_template = data[template_name]
            return prompt_template
    except:
        print("app.py::get_prompt_template: Error reading the prompt template json file.\n")
        return None
    
def replace_template_placeholders(template: str, placeholders: dict):
    # Placeholders is a dictionary with the placeholder name as the key and the value to replace as the value
    for placeholder, value in placeholders.items():
        # Add {} around the placeholder to match the template format
        placeholder = "{" + placeholder + "}"
        # Replace the template placeholder with the value
        template = template.replace(placeholder, value)
    return template
        

def create_prompt_from_template_user_input_context(user_input: str, context_file_path: str):
    # Get the prompt template from the JSON file
    # Using the text_qa_template as the default template
    prompt_template = get_prompt_template()
    # Get the context text from the pdf file
    context_text = pdf_to_text(context_file_path)
    # Create the placeholders dictionary needed to call replace_template_placeholders
    placeholders = {
        "context_str": context_text,
        "query_str": user_input
    }
    # Replace the placeholders in the template with the user input and context text
    prompt = replace_template_placeholders(prompt_template, placeholders)
    # Finally, return the modified prompt
    return prompt

# Main function
def main():
    # Define the path to the pdf or context file
    context_file_path = "data/recipe_book_LR.pdf"
    # Get the user query from the user
    user_input = input("Enter your recipe request: ")
    # Create the prompt from the template and user input
    prompt = create_prompt_from_template_user_input_context(user_input, context_file_path)
    # Get the chat response from the prompt
    # Using the gpt-3.5-turbo model as the default model
    response = get_chat_response(prompt)
    # Print the response from the chat
    print(response)

# Run the main function if the script is run directly
if __name__ == "__main__":
    main()



