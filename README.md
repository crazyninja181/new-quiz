# 🎯 AI Voice Quiz

An **AI-powered voice-based quiz application** built with Python. The project allows students to take quizzes by **speaking their answers**, making the learning experience more interactive and accessible.

The application supports students from **Class 1 to Class 10** and provides subject-based quizzes with multiple-choice questions.

## ✨ Features

* 🎤 **Voice-based interaction** – Speak your answers instead of typing.
* 🔊 **Text-to-Speech** – Questions and instructions are spoken aloud.
* 🤖 **AI Question Generation** – Uses a local Ollama model to generate quiz questions.
* 📚 **Class-wise Quizzes** – Supports Classes 1–10.
* 🧮 **Multiple Subjects** – Includes subjects such as:

  * Mathematics
  * Science
  * English
  * General Knowledge
  * History
* 🎲 **Random Subject Selection** – A subject is selected randomly for the quiz.
* ✅ **Automatic Answer Checking** – Answers are evaluated automatically.
* 📊 **Score Tracking** – Keeps track of the student's score.
* 📴 **Offline Recognition Fallback** – Uses Sphinx recognition when Google speech recognition is unavailable.
* 💾 **Question File Storage** – Quiz questions can be stored and loaded from text files.

## 🛠️ Technologies Used

* **Python**
* **Ollama**
* **Llama 3.2**
* **SpeechRecognition**
* **PyAudio**
* **pyttsx3**
* **CSV**
* **Threading**
* **Pathlib**

## 🤖 AI Model

The project uses the following Ollama model:

```text
llama3.2:1b-instruct-q4_0
```

The model is used to generate class-appropriate multiple-choice questions based on the selected subject.

## 📂 Project Structure

```text
new-quiz/
│
├── new quiz.py
│
├── class1_1.txt
├── class1_2.txt
├── class1_3.txt
├── class1_4.txt
├── class1_5.txt
│
├── class2_1.txt
├── class2_2.txt
├── ...
│
├── class10_1.txt
├── class10_2.txt
├── class10_3.txt
├── class10_4.txt
├── class10_5.txt
│
└── README.md
```

The `.txt` files contain quiz questions and their corresponding answers for different classes and subjects.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/crazyninja181/new-quiz.git
cd new-quiz
```

### 2. Install Python dependencies

```bash
pip install ollama pyttsx3 SpeechRecognition PyAudio
```

If PyAudio causes installation issues on Windows, install a compatible PyAudio package for your Python version.

### 3. Install Ollama

Install Ollama on your system and download the required model:

```bash
ollama pull llama3.2:1b-instruct-q4_0
```

Make sure Ollama is running before starting the application.

## ▶️ How to Run

Run the Python program:

```bash
python "new quiz.py"
```

The application will:

1. Welcome the user.
2. Ask for the class using voice input.
3. Select a quiz subject.
4. Load or generate questions.
5. Speak the questions aloud.
6. Listen for the user's answer.
7. Check the answer.
8. Provide voice feedback.

## 🎤 Voice Commands

The application accepts answers such as:

```text
Option 1
Option 2
Option 3
Option 4
```

It also supports:

```text
Option A
Option B
Option C
Option D
```

To exit the application, the user can say:

```text
quit
stop
exit
```

## 🧠 How It Works

```text
User
  ↓
Voice Input
  ↓
Speech Recognition
  ↓
Class Selection
  ↓
Subject Selection
  ↓
Quiz Questions
  ↓
Question is Spoken
  ↓
User Speaks Answer
  ↓
Speech Recognition
  ↓
Answer Checking
  ↓
Score
  ↓
Voice Feedback
```

## 🎓 Educational Purpose

This project was created to make quizzes more **interactive and voice-driven**.

Instead of requiring students to constantly interact with a keyboard or mouse, the application allows them to communicate with the quiz using their voice.

This can make learning more engaging and can also provide a foundation for developing **more accessible educational applications**.

## 🚀 Future Improvements

Some possible improvements include:

* Add Classes 11 and 12
* Add more subjects
* Improve answer validation
* Add a graphical user interface
* Add difficulty selection
* Add a leaderboard
* Store student scores
* Add detailed performance reports
* Improve speech recognition accuracy
* Generate questions dynamically for every quiz
* Add support for multiple languages
* Add a timer for each question
* Reduce repeated code using functions/classes

## 👨‍💻 Author

**crazyninja181**

GitHub:
https://github.com/crazyninja181

## 📄 License

This project is available for educational and learning purposes.
