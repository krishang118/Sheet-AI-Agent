# BCN Sheet-Editor AI Agent

An intelligent AI Agent for spreadsheet-editing combining natural language processing with deterministic Python execution; allows Excel/CSV file manipulation using plain English or voice commands, complex transformations, and secure data analysis with transparent, LLM-generated commands.

## Key Features

- Natural Language Editing - Modify spreadsheets using plain English or voice commands without any formulas
- Structured Execution - AI generates transparent JSON commands that are executed deterministically by Python
- Comprehensive Operations - Support for row/column manipulation, value transforms, date math, and numeric calculations
- Voice-to-Action - Integrated speech-to-text for hands-free data command and control
- Real-Time Preview - Instant visual feedback with an interactive grid and undo capability
- Secure & Private - User-controlled API keys with local execution of data transformations
- Multi-Format Export - Seamless import/export for CSV and Excel files

## How To Run

1. Make sure you have Python 3.8+ set up, and clone this repository on your local machine.
2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
streamlit run app.py
```

## Contributing

Contributions are welcome!

## License

Distributed under the MIT License. 
