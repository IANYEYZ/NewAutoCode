import os
from dotenv import load_dotenv
import typer
import logging
import helper
import gpt
from pathlib import Path

GPT = gpt.chatgpt()
app = typer.Typer()
fr = helper.FileReader(Path(__file__).parent)

def load_API_KEY():
    if os.getenv("OPENAI_API_KEY") is None:
        load_dotenv()
    GPT.set_api_key("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")

pr_path = Path("")

def clarify():
    """
    Let AI clarify the instructions
    """
    #print("Worked here.")
    GPT.add_message(fr.read_file('clarify'))
    inp = fr.read_file("UserPrompt")
    while True:
        #print(inp)
        message = ""
        for i in GPT.get_response(inp):
            print(i,end='')
            message += i
        GPT.add_message(message)
        print()
        if message.lower().startswith("no"):
            #print("Nothing more to clarify")
            break

        print()
        inp = input('(answer in text,or press enter)\n')
        print()

        if inp == '' or not inp:
            print("(Letting AutoCode make its own decision)")
            print()
            message = ""
            for i in GPT.get_response("Make your own assumptions and state them explicitly before starting"):
                print(i,end='')
                message += i
            GPT.add_message(message)
            print()
            return
        inp += (
            "\n\n"
            "Is anything else unclear? If yes, only answer in the form:\n"
            "{remaining unclear areas} remaining questions.\n"
            "{Next question}\n"
            'If everything is sufficiently clear, only answer "Nothing more to clarify.".'
            'Note that if you ask some questions and the user didn\'t answer all of them,you should know that the rest of these questions are unclear\n'
            'E.G. If you ask five questions,and the user only answer one\n'
            'then you should output like:\n'
            '{remaining unclear areas} remaining questions.\n'
            '{Next question}'
        )
    print()
    return

def setup_sys_prompt():
    return (
        fr.read_file("roadmap")
        + fr.read_file("generate")
        + "\nUseful to know:\n"
        + fr.read_file("philosophy")
    )
def setup_tdd_prompt():
    return (
        fr.read_file("testdata")
        + "\nUseful to know:\n"
        + fr.read_file("tdphilosophy")
    )
def setup_codereviewer_prompt():
    return (
        fr.read_file("codereviewer")
        + "\nUseful to know:\n"
        + fr.read_file("crphilosophy")
    )

def gen_tdd():
    message = ""
    GPT.add_message(setup_tdd_prompt(),"system")
    for i in GPT.get_response(fr.read_file("testdata")):
        print(i,end='')
        message += i
    print()
    GPT.add_message(message)
    return

def gen_code():
    message = ""
    GPT.add_message(setup_sys_prompt(),"system")
    for i in GPT.get_response(fr.read_file("generate")):
        print(i,end='')
        message += i
    print()
    GPT.add_message(message)
    return

def code_reviwer():
    message = ""
    GPT.add_message(setup_codereviewer_prompt(),"system")
    for i in GPT.get_response(fr.read_file("codereviewer")):
        print(i,end='')
        message += i
    print()
    GPT.add_message(message)
    return

def main():
    #logging.info("In function main,recieved {},start to run".format(path))
    load_API_KEY()
    #data_base = {"user_prompt" : "{}".format(helper.read_file(path))}
    #pr_path = Path(path)
    #print("Worked in main.")
    clarify()
    gen_code()
    gen_tdd()
    code_reviwer()

if __name__ == "__main__":
    main()