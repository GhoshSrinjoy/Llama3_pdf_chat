# PDF Query Assistant

This project implements a smart assistant to query PDF documents and provide detailed answers using the Llama3 model from the LangChain experimental library. The assistant extracts relevant text snippets from the PDFs and generates structured responses based on the user's query.

## Features

- Extract relevant text snippets from PDF documents.
- Rank the results based on the presence of query terms.
- Generate detailed answers using the Llama3 model.
- Provide structured responses in JSON format.

## Installation

### Prerequisites

- Python 3.7+
- Pip package manager

### Dependencies

Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Running the Script

Save the script as `bot.py` and run it from the command line:

```sh
python bot.py
```

### Interacting with the Assistant

- The assistant will prompt you to enter your query.
- You can enter your query interactively, and the assistant will process the PDFs and display the top results with structured answers.
- Type 'exit' to quit the script.

### Example Queries

- `Enter your query (or type 'exit' to quit): How to dynamically add, change, and/or remove properties (keys) from dictionary objects?`

## Code Documentation

### Extract Relevant Text

Extracts relevant text snippets containing the query terms.

```python
def extract_relevant_text(text, query_terms):
    """
    Args:
        text (str): The text to search through.
        query_terms (list): The terms to search for.

    Returns:
        str: The relevant text snippets.
    """
```

### Extract Text from PDF

Extracts text from a PDF and finds relevant snippets.

```python
def extract_text_from_pdf(pdf_path, query_terms):
    """
    Args:
        pdf_path (str): The path to the PDF file.
        query_terms (list): The terms to search for.

    Returns:
        list: A list of tuples with page number and relevant text snippets.
    """
```

### Extract Data from PDFs

Extracts data from all PDFs in a directory.

```python
def extract_data_from_pdfs(pdf_dir, query_terms):
    """
    Args:
        pdf_dir (str): The directory containing PDF files.
        query_terms (list): The terms to search for.

    Returns:
        pd.DataFrame: A DataFrame with the extracted data.
    """
```

### Rank Results

Ranks the results based on the presence of query terms.

```python
def rank_results(data, query_terms):
    """
    Args:
        data (pd.DataFrame): The DataFrame with extracted data.
        query_terms (list): The terms to rank by.

    Returns:
        pd.DataFrame: The ranked DataFrame.
    """
```

### Generate Answer with Llama3

Generates an answer using the Llama3 model.

```python
def generate_answer_with_llama3(query, snippets):
    """
    Args:
        query (str): The user's query.
        snippets (list): The context snippets.

    Returns:
        dict: The response from the model.
    """
```

### Answer Query

Answers a query based on the extracted data.

```python
def answer_query(data, query, top_n=5):
    """
    Args:
        data (pd.DataFrame): The DataFrame with extracted data.
        query (str): The user's query.
        top_n (int): The number of top results to return.

    Returns:
        tuple: The top results and the generated answer.
    """
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
```

This `README.md` file provides an overview of the project, installation instructions, usage examples, and detailed documentation of the code. It should help users understand how to set up and use your PDF Query Assistant.
