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
            valid, responses = myCommand.validate(player, adventure)
            if valid:
                responses.extend(myCommand.execute(player, adventure))
        for r in responses:
            print("[" + r[adv.RESPONSE_SOURCE] + "] " + r[adv.RESPONSE_TEXT])


def main(myAdventure):
    p = get_player()
    go(p, myAdventure(p), command.Parser(), command.Factory())