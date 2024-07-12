# PDF Query Assistant

This project implements a smart assistant to query PDF documents and provide detailed answers using the Llama3 model from the LangChain experimental library. The assistant extracts relevant text snippets from the PDFs and generates structured responses based on the user's query.

## Prerequisites

- Python 3.10+
- Pip package manager
- [Ollama](https://ollama.com) installed on your system
- Llama3 model, which can be downloaded by running `ollama run llama3` after installing Ollama

## Installation

### 1. Install Dependencies

First, ensure you have the required Python dependencies. You can install them using the provided `requirements.txt` file.

```sh
pip install -r requirements.txt
```

### 2. Install Ollama and Llama3

Make sure Ollama is installed on your system. Follow the installation instructions on the [Ollama website](https://ollama.com).

After installing Ollama, download the Llama3 model by running:

```sh
ollama run llama3
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

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
