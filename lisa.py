# Lisa, Como é feito o passado simples em inglês para frases afirmativas?
# Lisa, Como passar um verbo para a forma negativa usando passado simples?
# Lisa, Como funciona o passado simples para frases interrogativas?

from tools.brain import start, listen_question, recognize

def run():
    start()
    
    keep_working =  True
    while keep_working:
        try:
            question = listen_question()
            recognize(question)
    
        except KeyboardInterrupt:
            print("\nGoodbye") 
            keep_working = False

if __name__ == "__main__":
    run()