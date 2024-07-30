# OllamaMedVoice

## Overview

**OllamaMedVoice** is a cutting-edge project that integrates the Ollama-based model and ChatGPT with audio recognition technology to provide accurate and efficient medical question answering. This project aims to enhance the accessibility and responsiveness of medical information through voice interactions.

## Features

- **Audio Recognition**: Converts spoken medical questions into text.
- **Medical Question Answering**: Uses advanced AI models to provide accurate answers to medical queries.
- **Integration with ChatGPT**: Leverages the power of ChatGPT for natural language understanding and generation.
- **Ollama-based Model**: Incorporates Ollama's specialized model for improved medical context comprehension.
- **User-Friendly Interface**: Simple and intuitive interface for seamless user experience.

## Getting Started

### Prerequisites

- Python 3.8+
- Pip (Python package installer)
- Git
- Virtual Environment (optional but recommended)

### Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/your-username/OllamaMedVoice.git
    cd OllamaMedVoice
    ```

2. **Create a Virtual Environment**

    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
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
    python app.py
    ```

## Usage

1. **Open the Application**

    Access the application through your web browser at `http://localhost:5000`.

2. **Ask a Medical Question**

    Use your microphone to ask a medical question. The system will recognize your voice, process the query, and provide an answer based on the integrated AI models.

## Contributing

We welcome contributions to enhance OllamaMedVoice. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch to your fork.
4. Submit a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [OpenAI](https://www.openai.com/) for ChatGPT
- [Ollama](https://ollama.com/) for the specialized medical model
- The open-source community for various tools and libraries

## Contact

For any inquiries or support, please open an issue on the GitHub repository or contact the project maintainer at your-email@example.com.

---

*This project is for educational and informational purposes only. It is not intended as a substitute for professional medical advice, diagnosis, or treatment.*
