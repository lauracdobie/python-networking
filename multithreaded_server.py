import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary
from threading import Event
from player import Player

'''
Commands:
PLACE YOUR COMMANDS HERE
QUES - question command
ANS - answer command
SCO - score command
END - end command
'''

# Named tuples are extensions of the tuple structure, with contents you can refer to by name. In this case, the question will be held in a variable named q and the answer in answer.
# This is just the set up of the question - it will be sent to the client using the send_binary function when a request is made.
Question = namedtuple('Question', ['q', 'answer'])

q1 = Question("Who won the Booker Prize in 2020?", "Douglas Stuart")
q2 = Question("Who wrote Circe?", "Madeleine Miller")
q3 = Question("What is the name of the lion in The Lion, The Witch and The Wardrobe?", "Aslan")
q4 = Question("Margaret Atwood's Hag-Seed is based on which Shakespeare play?", "The Tempest")
q5 = Question("What is the name of the fictional Sicilian town where the Inspector Montalbano books set?", "Vigata")

questions = [q1, q2, q3, q4, q5]

NUMBER_OF_PLAYERS = 2
players = []
answers = 0
commands = []

ready_to_start = Event()
wait_for_answers = Event()

# The socketserver module uses 'Handlers' to interact with connections. When a client connects a version of this class is made to handle it.
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class QuizGame(socketserver.BaseRequestHandler):
    # The handle method is what actually handles the connection
    def handle(self):
        #Retrieve Command
        question = 0
        for command in get_binary(self.request):
            global players # Make sure this is global
            global answers

            if command[0] == "JOIN":
                team_name = command[1]
                player = Player(team_name)
                players.append(player)

                if len(players) == NUMBER_OF_PLAYERS:
                    # If correct number of players
                    ready_to_start.set()
                    # Trigger the event
                    # Send the confirmation response
                    send_binary(self.request, [5, "Let's go! To exit the quiz at any time, type end"])
                else:
                    send_binary(self.request, [5, "Waiting for others to join..."])
                # Wait for the ready to start event
                ready_to_start.wait()
            if command[0] == "QUES":
                #Send question
                send_binary(self.request, (1, questions[question].q))
            if command[0] == "ANS":
                answers += 1
                current_player = get_current_player(players, command[1][1])

                if answers < NUMBER_OF_PLAYERS:
                    send_binary(self.request, [5, "Waiting for others to answer..."])
                    wait_for_answers.wait()

                wait_for_answers.set()
                answers = 0

                if wait_for_answers.isSet():
                    if command[1][0].lower() == questions[question].answer.lower():
                        current_player.score += 1
                        send_binary(self.request, (2, "Correct!"))
                    else:
                        if current_player.lives > 0:
                            current_player.lives -= 1
                            send_binary(self.request, (2, "Incorrect, the answer is " + questions[question].answer + "."))
                        else:
                            send_binary(self.request, (2, "Incorrect, the answer is " + questions[question].answer))
                            send_binary(self.request, (4, "End of quiz! Your score is " + str(current_player.score)))
                            break

                if question < len(questions) - 1:
                    question += 1
                    wait_for_answers.clear()
                else:
                    send_binary(self.request, (4, "End of quiz! Your score is " + str(current_player.score)))
                    break

            if command[0] == "SCO":
                current_player = get_current_player(players, command[1])
                send_binary(self.request, (3, "Your score is " + str(current_player.score)))

            if command[0] == "END":
                current_player = get_current_player(players, command[1])
                send_binary(self.request, (4, "End of quiz! Your score is " + str(current_player.score)))
                break    

def get_current_player(players, team_name_in_command):
    for player in players:
        if player.team_name == team_name_in_command:
            current_player = player
    return current_player

# Open the quiz server and bind it to a port - creating a socket
# This works similarly to the sockets you used before, but you have to give it both an address pair (IP and port) and a handler for the server.
quiz_server = ThreadedTCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()