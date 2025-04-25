# Personal Fitness Tool

A Streamlit-based application that helps you manage your fitness journey with AI-powered assistance. Track your personal data, set fitness goals, calculate nutrition macros, and get AI-powered recommendations.

## Features

- Personal profile management (weight, height, age, activity level)
- Fitness goals tracking
- AI-powered macro calculations
- Notes management system
- AI assistant for fitness-related questions

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- langchain >= 0.3.24
- langchain-community >= 0.3.22
- langchain-ollama >= 0.3.2
- streamlit >= 1.44.1

## Usage

Run the application using Streamlit:

```bash
streamlit run main.py
```

### Features Overview

1. **Personal Data Management**
   - Track name, age, weight, height
   - Set gender and activity level
   - Save and update personal information

2. **Goals Setting**
   - Select from multiple fitness goals:
     - Muscle Gain
     - Fat Loss
     - Stay Active

3. **Nutrition Macros**
   - AI-generated macro recommendations
   - Manual macro tracking
   - Track calories, protein, fat, and carbs

4. **Notes System**
   - Add personal notes
   - View and manage existing notes
   - Delete unwanted notes

5. **AI Assistant**
   - Ask fitness-related questions
   - Get personalized recommendations
   - AI-powered guidance

## Data Storage

The application uses ChromaDB for storing:
- User profiles
- Personal notes
- Fitness data

## Contributing

Feel free to submit issues and enhancement requests.
