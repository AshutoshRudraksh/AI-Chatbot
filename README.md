## Advanced Local Chatbot with Ollama and Streamlit

A powerful, feature-rich local chatbot implementation that combines Ollama's language models with Streamlit's interactive interface capabilities. This chatbot supports streaming responses, advanced model parameters, conversation management, and markdown/code formatting.

## Features

### Core Functionality
- 🤖 Multiple Ollama model support (llama2, mistral, codellama, neural-chat)
- 💬 Streaming responses for real-time interaction
- 📝 Markdown and code syntax highlighting
- 🔄 Conversation history management

### Advanced Parameters
- 🌡️ Temperature control
- 🎯 Top-K and Top-P sampling
- 🔁 Repeat penalty adjustment
- 📊 Context length configuration

### Conversation Management
- 💾 Export conversations to JSON
- 📥 Import conversation history
- 🕒 Message timestamps
- 🗑️ Clear chat history
- 📤 Download conversation feature

## Prerequisites

1. **Python 3.7+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **Required Python packages**:
```bash
pip install streamlit requests markdown pygments
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ollama-streamlit-chatbot.git
cd ollama-streamlit-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install desired Ollama models:
```bash
ollama pull llama2
ollama pull mistral
ollama pull codellama
ollama pull neural-chat
```

## Usage

1. Start the Ollama service:
```bash
ollama serve
```

2. Run the Streamlit app:
```bash
streamlit run chatbot.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Configuration

### Model Parameters

The chatbot provides several adjustable parameters in the sidebar:

| Parameter | Range | Default | Description |
|-----------|--------|---------|-------------|
| Temperature | 0.0 - 2.0 | 0.7 | Controls response randomness |
| Top K | 1 - 100 | 40 | Limits token selection pool |
| Top P | 0.0 - 1.0 | 0.9 | Nucleus sampling threshold |
| Repeat Penalty | 1.0 - 2.0 | 1.1 | Penalizes repeated tokens |
| Context Length | 512 - 4096 | 2048 | Maximum context window |

### Conversation Management

- **Export**: Click "Export Chat" to download conversation as JSON
- **Import**: Upload previous conversations using the file uploader
- **Clear**: Use "Clear History" to start a new conversation

## Features in Detail

### Markdown Support
The chatbot supports full Markdown syntax including:
- Code blocks with syntax highlighting
- Tables
- Lists
- Bold/Italic text
- Links
- And more!

### Code Highlighting
```python
# Example of syntax highlighted code
def hello_world():
    print("Hello, World!")
```

### Message Formatting
- User messages are displayed with a light background
- Assistant responses have a white background
- Code blocks use Monokai theme

## File Structure

```
ollama-streamlit-chatbot/
├── chatbot.py          # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── .gitignore         # Git ignore file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Known Issues

1. The Streamlit warning about ScriptRunContext may appear in some environments
2. Large conversation exports might be slow with the current implementation
3. Some markdown features might not render correctly in older browsers

## Future Improvements

- [ ] Chat session management (multiple conversations)
- [ ] System prompt templates
- [ ] Model parameter presets
- [ ] Chat summarization
- [ ] Conversation search functionality
- [ ] Custom CSS themes
- [ ] API documentation
- [ ] Better error handling

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- [Ollama](https://ollama.ai) for the local LLM implementation
- [Streamlit](https://streamlit.io) for the web interface framework
- [Python-Markdown](https://python-markdown.github.io) for markdown support
- [Pygments](https://pygments.org) for code highlighting

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
