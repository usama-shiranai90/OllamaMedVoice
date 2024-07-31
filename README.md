# OllamaMedVoice

## Overview

**OllamaMedVoice** is a project that integrates the Ollama-based models and ChatGPT with audio recognition technology to
provide accurate and efficient medical question answering.
This project aims to enhance the accessibility and responsiveness of medical information through voice interactions.

## Features

- **Audio Recognition**: Converts spoken medical questions into text.
- **Medical Question Answering**: Uses advanced AI models to provide accurate answers to medical queries.
- **Integration with ChatGPT**: Leverages the power of ChatGPT for natural language understanding and generation.
- **Ollama-based Model**: Incorporates Ollama's specialized model for improved medical context comprehension.

[//]: # (- **User-Friendly Interface**: Simple and intuitive interface for seamless user experience.)

## Getting Started

### Prerequisites

- Python 3.10+
- Pip (Python package installer)
- Docker

### Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/usama-shiranai-090/OllamaMedVoice.git
    cd OllamaMedVoice
    ```

2. **Run docker file**

    ```sh
    docker compose --profile ollamaMedVoice up
    ```

3. **Use Python interactive mode**
    ```sh
    docker exec --workdir /src -it project-runner /bin/bash
    docker exec --workdir /src -it python-demo python3 main.py
    ```

### Running the Application

1. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the necessary environment variables:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    OLAMA_MODEL_PATH=path_to_ollama_model
    ```

2. **Start the Application**

    ```sh
    python file.py
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [OpenAI](https://www.openai.com/) for ChatGPT
- [Ollama](https://ollama.com/) for the specialized medical model
- The open-source community for various tools and libraries

---

*This project is for educational and informational purposes only. It is not intended as a substitute for professional
medical advice, diagnosis, or treatment.*
