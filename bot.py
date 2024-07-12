import os
from urllib.parse import quote
from PyPDF2 import PdfReader
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.llms.ollama_functions import OllamaFunctions

# Pydantic Schema for structured response
class Answer(BaseModel):
    """Schema for the structured response."""
    answer: str = Field(description="The detailed answer to the query", required=True)

def extract_relevant_text(text, query_terms):
    """Extracts relevant text snippets containing the query terms.
    
    Args:
        text (str): The text to search through.
        query_terms (list): The terms to search for.

    Returns:
        str: The relevant text snippets.
    """
    relevant_snippets = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if any(term.lower() in line.lower() for term in query_terms):
            # Extract a snippet around the query term
            start_index = max(0, i - 2)
            end_index = min(len(lines), i + 3)
            snippet = "\n".join(lines[start_index:end_index])
            relevant_snippets.append(snippet)
    return "\n\n".join(relevant_snippets)

def extract_text_from_pdf(pdf_path, query_terms):
    """Extracts text from a PDF and finds relevant snippets.
    
    Args:
        pdf_path (str): The path to the PDF file.
        query_terms (list): The terms to search for.

    Returns:
        list: A list of tuples with page number and relevant text snippets.
    """
    snippets = []
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                relevant_text = extract_relevant_text(page_text, query_terms)
                if relevant_text:
                    snippets.append((page_num + 1, relevant_text))
    return snippets

def extract_data_from_pdfs(pdf_dir, query_terms):
    """Extracts data from all PDFs in a directory.
    
    Args:
        pdf_dir (str): The directory containing PDF files.
        query_terms (list): The terms to search for.

    Returns:
        pd.DataFrame: A DataFrame with the extracted data.
    """
    data = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            snippets = extract_text_from_pdf(pdf_path, query_terms)
            for page_num, text in snippets:
                data.append({'filename': filename, 'page': page_num, 'text': text})
    return pd.DataFrame(data)

def rank_results(data, query_terms):
    """Ranks the results based on the presence of query terms.
    
    Args:
        data (pd.DataFrame): The DataFrame with extracted data.
        query_terms (list): The terms to rank by.

    Returns:
        pd.DataFrame: The ranked DataFrame.
    """
    data['score'] = data['text'].apply(lambda x: sum(1 for term in query_terms if term.lower() in x.lower()))
    return data.sort_values(by='score', ascending=False)

# Initialize OllamaFunctions
llm = OllamaFunctions(model="llama3", 
                      format="json", 
                      temperature=0)

structured_llm = llm.with_structured_output(Answer)

prompt = PromptTemplate.from_template(
    """system
    You are a smart assistant. Take the following context and question below and return your answer in JSON.
    user
QUESTION: {question} \n
CONTEXT: {context} \n
JSON:

assistant
 """
)

def generate_answer_with_llama3(query, snippets):
    """Generates an answer using the Llama3 model.
    
    Args:
        query (str): The user's query.
        snippets (list): The context snippets.

    Returns:
        dict: The response from the model.
    """
    context = "\n\n".join(snippets)
    chain = prompt | structured_llm
    response = chain.invoke({
        "question": query,
        "context": context
    })
    return response

def answer_query(data, query, top_n=5):
    """Answers a query based on the extracted data.
    
    Args:
        data (pd.DataFrame): The DataFrame with extracted data.
        query (str): The user's query.
        top_n (int): The number of top results to return.

    Returns:
        tuple: The top results and the generated answer.
    """
    query_terms = query.split()
    ranked_data = rank_results(data, query_terms)
    top_results = ranked_data.head(top_n)
    
    snippets = [row['text'] for index, row in top_results.iterrows()]
    answer = generate_answer_with_llama3(query, snippets)
    return top_results, answer

if __name__ == "__main__":
    pdf_dir = "C:/Users/Srinjoy Ghosh/Desktop/Folders/Study/APDS/slides"
    
    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            break

        query_terms = query.split()
        # Extract data from PDFs
        data = extract_data_from_pdfs(pdf_dir, query_terms)
        
        # Answer query
        top_results, answer = answer_query(data, query)
        
        if not top_results.empty:
            print(f"\nTop {len(top_results)} results matching the query '{query}':")
            for index, row in top_results.iterrows():
                pdf_path = os.path.join(pdf_dir, row['filename'])
                pdf_link = f'file:///{quote(pdf_path)}#page={row["page"]}'
                print(f"Filename: {row['filename']}, Page: {row['page']}")
                print(f"Link: {pdf_link}")
                print(f"Text snippet:\n{row['text']}\n")
            print("Answer from LLM:")
            print(answer)
        else:
            print(f"No results found for the query '{query}'.")
