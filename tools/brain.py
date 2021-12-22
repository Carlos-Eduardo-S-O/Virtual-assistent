from tools.functions import positive, negative, print_answer
import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

CORPUS_LANGUAGE = "portuguese"
SPEECH_LANGUAGE = "pt-BR"

CONFIG_PATH = "Lisa/static/config.json"

def start():
    global recognizer
    global stop_words
    
    global assistant_name
    global questions
    global pasts
    global forms

    recognizer = sr.Recognizer()
    stop_words = set(corpus.stopwords.words(CORPUS_LANGUAGE))
    
    stop_words.remove("como")
    stop_words.remove("qual")
    
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        
        assistant_name = config["name"]
        questions = config["questions"]
        pasts = config["pasts"]
        forms = config["forms"]
        
        config_file.close()
        positive(f"Successfully Loaded, {assistant_name} is running!")           
            
def listen_question():
    global recognizer
    
    question = None
    
    with sr.Microphone() as audio_source:
        recognizer.adjust_for_ambient_noise(audio_source)
        
        print("Como eu posso ajuda-lo?")
        speech = recognizer.listen(audio_source)
        
        try:
            print("Espere um pouco estou tentando enteder o que você acabou de falar...")
            question = str(recognizer.recognize_google(speech, language=SPEECH_LANGUAGE)).lower()

        except sr.UnknownValueError:
            pass
    return question

def remove_stop_words(tokens):
    global stop_words
    
    filtered_tokens = []
    for token in tokens:
        if token not in stop_words:
            filtered_tokens.append(token)
            
    return filtered_tokens

def tokenize_question(question):
    global assistant_name
    parts_question = None
    
    tokens = word_tokenize(question, CORPUS_LANGUAGE)
    
    if tokens:
        
        tokens = remove_stop_words(tokens)
        if len(tokens) > 5:
            if assistant_name == tokens[0]:
                parts_question = [] 
                for i in range(1, len(tokens)):
                    parts_question.append(tokens[i])
    
    return parts_question

def recognize_question(parts_question):
    global questions
    
    valid = False
    auxiliary = ""
    
    if parts_question:
        for i in range(0, len(parts_question)):
            auxiliary += parts_question[i]
        
        for question in questions:
            if len(question) <= len(auxiliary):
                position = auxiliary.find(question)
                if position != -1:
                    position = position + len(question)
                    parts_question = auxiliary[position:]
                    valid = True
                    break 
            
    return valid, parts_question

def recognize_past(parts_question):
    global pasts
    
    valid = False
    
    for past in pasts:
        if len(past) <= len(parts_question):
            position = parts_question.find(past)
            if position != -1:
                valid = True
                break

    return valid

def recognize_form(parts_question):
    global forms
    
    answers = None
    valid = False
    
    for form in forms:
        if len(form) <= len(parts_question):
            position = parts_question.find(form["name"])
            if position != -1:
                answers = form["answers"]
                valid = True
                break
    
    return valid, answers

def recognize(question):
            
    valid_question, valid_past, valid_form = False, False, False
    if question:
        parts_question = tokenize_question(question)

        if parts_question:
            valid_question, parts_question_r = recognize_question(parts_question)
            parts_question = parts_question_r

            if valid_question:
                valid_past = recognize_past(parts_question)
                
                if valid_past:
                    valid_form, answers = recognize_form(parts_question)
                    
                    if valid_form:
                        print_answer(answers)
                
    if not (valid_question and valid_past and valid_form):                
        negative("Desculpe, eu não consegui entender o que você disse. Você poderia repetir")