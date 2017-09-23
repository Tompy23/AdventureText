import adv.basic as adv
import adv.command as command


# Startup functions


def get_player():
    name = input("What is your name? ")
    return adv.Player(name)


def start(player, adventure):
    parser = command.CommandParser()
    factory = command.CommandFactory()
    while adventure.proceed:
        myInput = parser.get_command()
        myCommand = factory.create_command(myInput.split())
        if myCommand is None:
            responses = [adv.Response("COMMAND", "Not a valid command")]
        else:
            responses = myCommand.execute(player, adventure)
        for r in responses:
            print("[" + r.source + "] " + r.text)
