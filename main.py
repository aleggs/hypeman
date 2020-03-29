import cam, trainer, recognizer

def new_user():
    cam.new_user()
    
def train():
    trainer.train()
    
def run():
    recognizer.run()

while(True):
    user_input = input("Enter a command: $ ").lower()
    if user_input == "quit" or user_input == "q":
        break
    elif user_input == "new user" or user_input == "n":
        new_user()
    elif user_input == "train" or user_input == "t":
        train()
    elif user_input == "run" or user_input == "r":
        run()
    elif user_input == "help":
        print("q = quit, n = new user, t = train, r = run")
    elif user_input == "songs":
        print("allstar, johncena, kashmir, nyancat, pokemon, rickroll, takethepowerback")
    else:
        print("Invalid input! Type 'help' if you need help.")