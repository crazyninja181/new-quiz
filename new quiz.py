import ollama 
import pyttsx3
from datetime import date
from random import randint as r
import speech_recognition as sr
import pyaudio
import threading
from pathlib import Path
import csv
import time
downloads = Path.home() / "Downloads"
def speak(text):
    eng=pyttsx3.init()
    eng.setProperty('rate',190)
    voices=eng.getProperty('voices')
    eng.setProperty('voice',voices[1].id)
    eng.say(text)
    eng.runAndWait()
    eng.stop()
def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening..., speak now")
        r.pause_threshold=1
        audio=r.listen(source)
        r.adjust_for_ambient_noise(source,duration=0.2)
        try:
            audio=r.listen(source,timeout=3,phrase_time_limit=3)
            
            print("Recognizing...")
            text=r.recognize_google(audio,language='en-in')
            
            print(f"User said: {text}\n")
            if text in ["quit","stop","exit"]:
                speak("exiting")
                exit()
            else:
                return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("using offline recognition sphinx.")
            try:
                audio=r.listen(source,timeout=5,phrase_time_limit=8)
                text=r.recognize_sphinx(audio)
                speak(f"You said: {text}")
                return text
            except Exception:
                speak("Sorry, I did not understand that.")
                return None
prompt=" "
def generate_questions(Class, subject, num_questions=10):
    global prompt
    f"""
    Generates exactly {num_questions}*6 lines of quiz content.
    Each retry regenerates the quiz if line count is incorrect.
    """
    global data
    data = []
    expected_lines = num_questions * 6
    max_retries = 10
    tries = 0
    if subject.lower()=="maths":
        prompt = f"""
You are a quiz generator AI that only creates school-level mathematics quizzes.

Generate exactly {num_questions} multiple-choice questions for Class {Class} in the subject Mathematics.

Each question must test **only mathematical knowledge**, such as:
- basic arithmetic (addition, subtraction, multiplication, division)
- fractions, percentages, geometry, algebra (depending on class level)
- no questions about English, science, or general knowledge.

Follow this **exact format** with no extra text or blank lines:

Question 1: What is 2 + 3?
1) 4
2) 5
3) 6
4) 7
Answer: Option2: 5

Rules:
- Only mathematics-related questions.
- No story-based or theoretical questions.
- Each question set must have exactly 6 lines.
- The answer line must begin with "Answer:" followed by "Option" and the correct number.
- Output exactly {num_questions * 6} lines, nothing else.
- Keep difficulty level suitable for Class {Class}.
"""
    elif subject.lower()=="english":
        prompt = f"""
You are a quiz generator AI. 
Generate exactly {num_questions} English multiple-choice questions for Class {Class}.

Each question must test English language skills such as grammar, vocabulary, or tenses.
Do not include math, science, or general knowledge.
Format exactly like this (no blank lines):
Question 1: Choose the correct form of the verb.
A) go
B) goes
C) gone
D) going
Answer: OptionB: goes
1. Difficulty must match Class {Class} level. 
    - For Class 1–5 → basic, simple.
    - For Class 6–8 → moderate, conceptual, short reasoning.
    - For Class 9–12 → board exam level, short reasoning.




"""

    else:
        prompt = f"""
    You are a school quiz generator AI.
    Generate exactly {num_questions} multiple-choice questions for a student of Class {Class} (Grade {Class}) in the subject {subject} only.

    The questions must be strictly based on the standard syllabus for that grade level.
    Keep the language simple and concepts appropriate for the age group.

    Follow these strict rules:
    1. Difficulty must match Class {Class} level. 
    - For Class 1–5 → basic, simple.
    - For Class 6–8 → moderate, conceptual, short reasoning.
    - For Class 9–12 → board exam level, short reasoning.
    2. Each question must have 4 options and one correct answer.
    3. Follow this strict format (no blank lines, no explanation):

    Example:
    Question 1: What is the capital of France?
    1) Berlin
    2) Madrid
    3) Paris
    4) Rome
    Answer: Option 3: Paris
    -dont include this  question 
    Rules:
    
    - No blank lines or extra text.
    - Each question set = 6 lines.
    - Answer line starts with 'Answer:'.
    - Output exactly {num_questions * 6} lines total.
    - Do NOT add explanations, hints, or introductions.
    """


    data = []
    tries = 0
    expected_lines = num_questions * 6

    while len(data) < expected_lines and tries < 3:
        print(f"🔁 Attempt {tries + 1}: Generating quiz...")

        response = ollama.chat(
            model="llama3.2:1b-instruct-q4_0",
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": 8192}
        )

        # Clean and process response
        lines = [line.strip() for line in response["message"]["content"].split("\n") if line.strip()]
        # Filter out unwanted model chatter
        lines = [line for line in lines if not line.lower().startswith(("here", "sure", "example", "quiz", "okay", "note"))]
        data.extend(lines)

        if len(data) < expected_lines:
            print(f"⚠️ Only {len(data)} lines generated, retrying...")
            time.sleep(2)
            missing_q = (expected_lines - len(data)) // 6
            prompt += f"\nGenerate {missing_q} more questions continuing numbering in same format."
        tries += 1

    # Trim any extra lines if overshoot
    data = data[:expected_lines]

    print(f"✅ Generated {len(data)//6} questions successfully.")
    return data
    
    try:
        response=ollama.chat(model='llama3.2:1b-instruct-q4_0',
                             messages=[
            {'role':'system','content':'You are a helpful quiz generator.'},
            {'role':'user','content':prompt}
        ])
        text=response['message']['content']
        lines=[line.strip() for line in text.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print("❌ Error generating questions:",e)
        return []
def write_questions_to_file(lines,filename):
    if not lines:
        print("⚠️ No questions to save.")
        return
    with open(filename,'w',encoding='utf-8') as f:
        for line in lines:
            f.write(line+'\n')
        print(f"✅ Saved {len(lines)//2} questions to {filename}")
        speak(f"Saved {len(lines)//2} questions to {filename}")

def Class():
    global class_map
    class_map={
    "first class": 1,"one": 1,"1st class": 1,"1": 1,
    "second class": 2,"two": 2,"2nd class": 2,"2": 2,
        "third class": 3,"three": 3,"3rd class": 3,"3": 3,
        "fourth class": 4,"four": 4,"4th class": 4,"4": 4,
        "fifth class": 5,"five": 5,"5th class": 5,"5": 5,
        "sixth class": 6,"six": 6,"6th class": 6,"6": 6,
        "seventh class": 7,"seven": 7,"7th class": 7,"7": 7,
        "eighth class": 8,"eight": 8,"8th class": 8,"8": 8,
        "ninth class": 9,"nine": 9,"9th class": 9,"9": 9,
        "tenth class": 10,"ten": 10,"10th class": 10,"10": 10,
        "eleventh class": 11,"eleven": 11,"11th class": 11,"11": 11,
        "twelfth class": 12,"twelve": 12,"12th class": 12,"12": 12
    }
    speak("Welcome to the Quiz")
    speak("speak the class like first class, second class, third class and so on")
    class_input=listen()
    
    if class_input is None:
        speak("Could not recognize your class. Please try again.")
        return None
    else:
        if class_input in class_map:
            Class=class_map[class_input]
            speak(f"You selected Class {Class}")
            return Class
        else:
            speak("Invalid class input. Please try again.")
            return None
speak("exit or stop or quit to leave the quiz")
Class=Class()  
if  Class==None:
    speak("Exiting the quiz due to invalid class input.")
    exit()
else:
    
    speak("Starting quiz...")
    answers={"option 1":"1","option 2":"2","option 3":"3","option 4":"4","option one":"1","option two":"2","option three":"3","option four":"4","option for":"4",
             "option a":1,"option b":2,"option c":3,"option d":4,"optiona":1,"optionb":2,"optionc":3,"optiond":4,
             "option A":1,"option B":2,"option C":3,"option D":4,"optionA":1,"optionB":2,"optionC":3,"optionD":4}
    sub = " "
    filename = ""
    def Quiz():
        if Class==1:
            global sub,filename
            score=0
            slno=r(1,5)
            if slno==1:
                filename="class1_1.txt"
                sub="maths"
                speak("Your exam subject is maths")
            elif slno==2:
                sub="science"
                filename="class1_2.txt"
                speak("your exam subject is science")
            elif slno == 3:
                sub = "english"; filename = "class1_3.txt"
                speak("your exam subject is english")
            elif slno == 4:
                sub = "gk"; filename = "class1_3.txt"
                speak("your exam subject is gk")
            else:
                sub = "history"; filename = "class1_5.txt"
                speak("your exam is computer science")
            speak(f"Your exam subject is {sub}")
            downloads_path = downloads / filename
            if not downloads_path.exists():
                speak(f" File {filename} not found in Downloads.")
                return 
            else:
                ob1=open("class1_4.txt","r")
                data=ob1.readlines()
                score = 0
                for line in data:
                    if line.lower().startswith("answer:"):
                        correct_answer_text = line.split(":", 1)[1].strip().lower()
                        print(correct_answer_text)
                        speak("What is your answer?")
                        ans = listen()
                        if ans is None:
                            speak("No response detected.")
                            continue
                        ans_num = answers.get(ans, None)
                        if ans_num is None:
                            speak("Invalid option. Try to say option 1, option a, etc.")
                            continue

                        if correct_answer_text in ans or ans in correct_answer_text:
                            speak("Correct answer!")
                            score += 1
                        else:
                            speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                    else:
                        speak(line)
        elif Class==2:
            
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class2_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class2_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class2_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class2_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class2_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
                
        elif Class==3:
            
               
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class3_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class3_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class3_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class3_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class3_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line) 
        elif Class==4:
            
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class4_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class4_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class4_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class4_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class4_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        elif Class==5:
            
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class5_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class5_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class5_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class5_3.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class5_4.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        elif Class==6:
            
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class6_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class6_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class6_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class6_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class6_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        elif Class==7:
            
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class7_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class7_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class7_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class7_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class7_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        elif Class==8:
            
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class8_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class8_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class8_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class8_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class8_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        elif Class==9:
            
            
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class9_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class9_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class9_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class9_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class9_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        else:
                
                score=0
                slno=r(1,5)
                if slno==1:
                    filename="class10_1.txt"
                    sub="maths"
                    speak("Your exam subject is maths")
                elif slno==2:
                    sub="science"
                    filename="class10_2.txt"
                    speak("your exam subject is science")
                elif slno == 3:
                    sub = "english"; filename = "class10_3.txt"
                    speak("your exam subject is english")
                elif slno == 4:
                    sub = "gk"; filename = "class10_4.txt"
                    speak("your exam subject is gk")
                else:
                    sub = "history"; filename = "class10_5.txt"
                    speak("your exam is computer science")
                speak(f"Your exam subject is {sub}")
                downloads_path = downloads / filename
                if not downloads_path.exists():
                    speak(f" File {filename} not found in Downloads.")
                    return 
                else:
                    ob1=open(filename,"r")
                    data=ob1.readlines()
                    score = 0
                    for line in data:
                        if line.lower().startswith("answer:"):
                            correct_answer_text = line.split(":", 1)[1].strip().lower()
                            speak("What is your answer?")
                            ans = listen()
                            if ans is None:
                                speak("No response detected.")
                                continue
                            ans_num = answers.get(ans, None)
                            if ans_num is None:
                                speak("Invalid option. Try to say option 1, option a, etc.")
                                continue

                            if correct_answer_text in ans or ans in correct_answer_text:
                                speak("Correct answer!")
                                score += 1
                            else:
                                speak(f" Incorrect. The correct answer was {correct_answer_text}.")
                        else:
                            speak(line)
        return score
def parallel():
    results={}
    def task1():
        results["score_data"]=Quiz()
    def task2():
        results["questions"]=generate_questions(Class,sub,10)
    t1=threading.Thread(target=task1,daemon=True)
    t2=threading.Thread(target=task2,daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("both tasks done")
    return results
s=parallel()        
if "questions" in s and s["questions"]:
    out_file = downloads / f"next_quiz_{sub}.txt"
    write_questions_to_file(s["questions"], out_file)
    print(f"🏁 Next quiz generated: {out_file}")
if "score_data" in s and s["score_data"]:
    score1=s["score_data"]
    ob1=open("score.csv","a")
    ob=csv.writer(ob1)
    today=date.today()
    ob.writerow(today,Class,sub,score1)

    
    

            
            
            
    
    
