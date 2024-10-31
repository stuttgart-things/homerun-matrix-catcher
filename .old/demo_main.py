import subprocess

def call_file(condition):    
    if condition=="True":
        subprocess.call(['sudo','python','-E','demo_stdin.py'])
    else:
        print("Not Run")

condition=input("Run File? ")
call_file(condition)

