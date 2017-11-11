import adv.basic as adv


# Startup functions


def get_player():
    name = input("What is your name? ")
    return adv.Player(name)


def begin(player, adventure, parser, factory):
    while adventure.proceed:
        myInput = parser.get_command()
        myCommand = factory.create_command(myInput.split())
        if myCommand is None:
            responses = [adv.Response("INPUT", "Not a valid command")]
        else:
            responses = myCommand.execute(player, adventure)
        for r in responses:
            print("[" + r.source + "] " + r.text)
