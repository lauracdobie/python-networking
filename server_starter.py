# The socket server library is a more powerful module for handling sockets, it will help you set up and manage multiple clients in the next step
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary

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

# The socketserver module uses 'Handlers' to interact with connections. When a client connects a version of this class is made to handle it.
class QuizGame(socketserver.BaseRequestHandler):
    # The handle method is what actually handles the connection
    def handle(self):
        #Retrieve Command
        score = 0
        question = 0
        lives = 3
        for command in get_binary(self.request):
            if command[0] == "QUES":
                #Send question
                send_binary(self.request, (1, questions[question].q))
            if command[0] == "ANS":
                if command[1].lower() == questions[question].answer.lower():
                    send_binary(self.request, (2, "Correct!"))
                    score += 1
                else:
                    if lives > 0:
                        lives -= 1
                        send_binary(self.request, (2, "Incorrect, the answer is " + questions[question].answer + ". You have " + str(lives) + " lives left."))
                    else:
                        send_binary(self.request, (2, "Incorrect, the answer is " + questions[question].answer))
                        send_binary(self.request, (4, "End of quiz! Your score is " + str(score)))
                        break
                if question < len(questions) - 1:
                    question += 1
                else:
                    send_binary(self.request, (4, "End of quiz! Your score is " + str(score)))
                    break
            if command[0] == "SCO":
                send_binary(self.request, (3, "Your score is " + str(score)))
            if command[0] == "END":
                send_binary(self.request, (4, "End of quiz! Your score is " + str(score)))
                break    


# Open the quiz server and bind it to a port - creating a socket
# This works similarly to the sockets you used before, but you have to give it both an address pair (IP and port) and a handler for the server.
quiz_server = socketserver.TCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()