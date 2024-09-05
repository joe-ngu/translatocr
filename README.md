<h1 align="center">
  <br>
  <a href="https://github.com/joe-ngu/translatocr"><img src="https://raw.githubusercontent.com/joe-ngu/translatocr/main/assets/logo.jpeg" alt="TranslatOCR" width="200"></a>
  <br>
  TranslatOCR
  <br>
</h1>

<h4 align="center">An OCR program that extracts text from images, translates it, and re-renders the images with the translated text.</h4>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"/>
  </a>
 <a href="https://github.com/JaidedAI/EasyOCR">
    <img src="https://img.shields.io/badge/EasyOCR-003399.svg?style=for-the-badge&logo=ai&logoColor=white" alt="EasyOCR"/>
  </a>
  <a href="https://www.langchain.com"/>
    <img src="https://img.shields.io/badge/langchain-%230D1C49.svg?style=for-the-badge&logo=langchain&logoColor=white" alt="Langchain"/>
  </a>
  <a href="https://llama.meta.com/">
    <img src="https://img.shields.io/badge/Llama%203-%231877F2.svg?style=for-the-badge" alt="Llama 3"/>
  </a> 
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#quickstart">Quick Start</a> •
  <a href="#design">Design</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features
- **Automated Text Extraction**  
  - Uses EasyOCR, a powerful Optical Character Recognition (OCR) module
  - Supports over 80 languages
  - Detects text from various sources, including:
    - Documents
    - Photos

- **Accurate Translation with Grammar and Spell Checking**  
  - Leverages the Google Translate API for reliable translation
  - Built-in grammar and spell-check functionality
  - Ensures polished and accurate translations

- **Llama 3.1 Integration**  
  - Integrated with Meta’s state of the art, open-source LLM, Llama 3.1
  - Provides additional context for translated images
  - Enhances understanding and accuracy of translations


## Quickstart

To clone and run this application, you'll need [Git](https://git-scm.com), [Python 3.12+](https://www.python.org/downloads/), and [Ollama](https://ollama.com/download) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/joe-ngu/translatocr.git

# Navigate into the repository
$ cd translatocr

# Create and activate a virtual environment (optional but recommended)
$ python3 -m venv venv
$ source venv/bin/activate

# Install the required packages
$ pip install -r requirements.txt

# Download LLama3.1 locally
$ ollama pull llama3.1

# Run the program
$ python3 main.py

```

To test the code with your own images, you'll need to update the `image_info` variable to reflect your custom images and desired translation languages. The `image_info` variable should be modified as follows:

```python
  image_info = [
      ("your_image_file_name.jpg", Language.SOURCE_LANGUAGE, Language.DESTINATION_LANGUAGE),
      # Add more tuples as needed
  ]
```
**Key Points:**
- Replace `"your_image_file_name.jpg"` with the file_name and ensure that image file is placed in the `original_images` folder
- Set `Language.SOURCE_LANGUAGE` to the language of the text in your image (e.g., `Language.SPANISH`)
- Set `Language.DESTINATION_LANGUAGE` to the language you want the text to be translated into (e.g., `Language.ENGLISH`)
- Ensure that the language identifiers match those defined in your codebase. If the language is not present modify the Language enum, but
  consult [EasyOCR documentation](https://github.com/JaidedAI/EasyOCR) on supported languages

This will allow the script to process your custom images and apply the desired translations.


## Design

### Application Architecture
This application follows a modular architecture designed for scalability and flexibility. Each component is loosely coupled to allow for independent updates and smooth integration:

- **Text Extraction Engine**  
  - Powered by EasyOCR for detecting and reading text from images
  - Handles image preprocessing, text region detection, and extraction

- **Translation and Grammar Check Module**  
  - Uses Google Translate for automatic translation
  - Integrated grammar and spell-checking to improve translation quality
  - Modular setup allows easy swapping of translation services

- **Llama 3.1 Context Provider**  
  - Integrates Meta’s Llama 3.1 to add context and refine translations
  - Enhances accuracy, especially for nuanced content

- **Image Processing Unit**  
  - Overlays translated text onto images, replacing the original text
  - Ensures readability while maintaining image integrity

![TranslatORC Architecture Diagram](link here)


## Credits
The images used in this project are for educational and demonstrative purposes only. All rights to these images are retained by their respective sources:

- https://lechefswife.com/simple-french-riviera-spring-menu/
- https://www.open.edu/openlearn/languages/french/beginners-french-food-and-drink/content-section-2.1
- https://bible.usccb.org/es/bible/lecturas/090324.cfm
- https://bible.usccb.org/es/bible/lecturas/090424.cfm
- https://montrealgazette.com/opinion/opinion-safety-should-trump-language-for-quebec-highway-signs
- imgflip.com (for creating the file english_meme.jpg)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.