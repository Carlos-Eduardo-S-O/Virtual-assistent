import sys
from random import randrange
from time import sleep
# Control variables 
TYPE_SPEED = 0.1
# Text manipulations
def negative(msg):
    print(f"\033[31m{msg}\033[m")

def positive(msg):
    print(f"\033[32m{msg}\033[m")

def typewriter(msg):
    print("")
    for c in msg:
        sys.stdout.write(c)
        sys.stdout.flush()
        #Caso deseje usar uma digitação mas parecida com uma real use esse código abaixo. Caso não tenha conhecimento técnico basta retirar as (""") envolta do código e adicionar uma # na frente da linha 'seconds = TYPE_SPEED'
        """
        seconds = "0." + str(randrange(1, 4, 1))
        seconds = float(seconds)
        """
        seconds = TYPE_SPEED
        sleep(seconds)

    
def print_answer(list):
    for dict in list:
        typewriter(dict["answer"])
        typewriter(dict["exemple"])

def clear(text):
    return unidecode(text)  