import adv.adventure as adv
import adv.command as command


def get_player():
    name = input("What is your name? ")
    return adv.Player(name)


def go(player, adventure, parser, factory):
    while adventure.proceed:
        myInput = parser.get_command()
        myCommand = factory.create_command(myInput.split())
        if myCommand is None:
            responses = [("INPUT", "Not a valid command")]
        else:
            responses = myCommand.execute(player, adventure)
        for r in responses:
            print("[" + r[0] + "] " + r[1])


def main(myAdventure):
    p = get_player()
    go(p, myAdventure(p), command.Parser(), command.Factory())