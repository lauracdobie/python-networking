import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary
from threading import Event
from player import Player
from random import choice

'''
Commands:
PLACE YOUR COMMANDS HERE
JOIN - join command
QUES - question command
ANS - answer command
SCO - score command
STAT - stat command
END - end command
'''

# Named tuples are extensions of the tuple structure, with contents you can refer to by name. In this case, the question will be held in a variable named q and the answer in answer.
# This is just the set up of the question - it will be sent to the client using the send_binary function when a request is made.
Question = namedtuple('Question', ['q', 'answer', 'options'])

q1 = Question("Who won the Booker Prize in 2020?", "Douglas Stuart", ["Kazuo Ishiguro", "Bernardine Evaristo", "Douglas Stuart", "Jon MacGregor"])
q2 = Question("Who wrote Circe?", "Madeleine Miller", ["Madeleine Miller", "Pat Barker", "Ann Patchet", "Stephen Fry"])
q3 = Question("What is the name of the lion in The Lion, The Witch and The Wardrobe?", "Aslan", ["Leonardo", "Macavity", "Fluffy", "Aslan"])
q4 = Question("Margaret Atwood's Hag-Seed is based on which Shakespeare play?", "The Tempest", ["Hamlet", "Twelfth Night", "The Tempest", "The Winter's Tale"])
q5 = Question("What is the name of the fictional Sicilian town where the Inspector Montalbano books set?", "Vigata", ["Punta Secca", "Vigata", "Palermita", "Ragusa"])

questions = [q1, q2, q3, q4, q5]

NUMBER_OF_PLAYERS = 2
players = []
answers = 0
current_question = None
current_player = None
scores = {}

ready_to_start = Event()
wait_for_answers = Event()

# The socketserver module uses 'Handlers' to interact with connections. When a client connects a version of this class is made to handle it.
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class QuizGame(socketserver.BaseRequestHandler):
    # The handle method is what actually handles the connection
    def handle(self):
        #Retrieve Command

        for command in get_binary(self.request):
            global players # Make sure this is global
            global answers
            global current_question
            global current_player
            global scores
            questions

            if command[0] == "JOIN":
                team_name = command[1]
                player = Player(team_name)
                players.append(player)
                scores[team_name] = 0

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
                if current_question == None:
                    if len(questions) > 0:
                        current_question = choice(questions)
                    # Un-set the event for answers
                    wait_for_answers.clear()
                if current_question != None:
                    # Send the question text
                    send_binary(self.request, (1, current_question.q, current_question.options))
                else:
                    send_binary(self.request, (4, "End of quiz! Your score is " + str(current_player.score) + "."))
                    break
            
            if command[0] == "ANS":
                answers += 1
                current_player = get_current_player(players, command[1][1])
                                
                if command[1][0].lower() == current_question.answer.lower():
                    current_player.score += 1
                    send_binary(self.request, (2, "Correct! Your score is " + str(current_player.score) + "."))
                    scores[current_player.team_name] += 1
                else:
                    if current_player.lives > 0:
                        current_player.lives -= 1
                        if current_player.lives != 1:
                            send_binary(self.request, (2, "Incorrect, the answer is " + current_question.answer + ". You have " + str(current_player.lives) + " lives remaining. Your score is " + str(current_player.score) + "."))
                        else:
                            send_binary(self.request, (2, "Incorrect, the answer is " + current_question.answer + ". You have 1 life remaining. Your score is " + str(current_player.score) + "."))
                    else:
                        send_binary(self.request, (2, "Incorrect, the answer is " + current_question.answer + ". Your score is " + str(current_player.score) + "."))
                        players.remove(current_player)
                        send_binary(self.request, (4, "Game over!"))
                        answers -= 1
                
                if answers == len(players):
                    answers = 0
                    # Remove the current question from the list
                    questions.remove(current_question)
                    # Reset the current question variable
                    current_question = None
                    wait_for_answers.set()

                wait_for_answers.wait()

            if command[0] == "SCO":
                send_binary(self.request, (3, str(scores)))
            
            if command[0] == "STAT":
                if ready_to_start.isSet() and not wait_for_answers.isSet():
                    send_binary(self.request, [6, "Quiz is starting!"])
                elif ready_to_start.isSet() and wait_for_answers.isSet():
                    send_binary(self.request, [6, "Quiz continuing."])
            
            if command[0] == "END":
                current_player = get_current_player(players, command[1])
                players.remove(current_player)
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