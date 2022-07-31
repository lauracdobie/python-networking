import socket
# Import the functions from the networking tools module
from fl_networking_tools import get_binary, send_binary

'''
Responses
LIST YOUR RESPONSE CODES HERE
1 - Question
2 - Answer
3 - Score
4 - End
5 - Join
'''
team_name = input("Enter a team name > ")
print("Greetings, " + team_name + ", welcome to the quiz!")

ip_address = input("Enter the IP address that the quiz is running on > ")
print("Connecting to " + ip_address + "...")

# A flag used to control the quiz loop.
playing = True

quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

quiz_server.connect((ip_address, 2065))

# Sending a command to the server.
send_binary(quiz_server, ["JOIN", team_name])
send_binary(quiz_server, ["QUES", ""])

while playing:
    # The get_binary function returns a list of messages - loop over them
    for response in get_binary(quiz_server):
        if response[0] == 5:
            print(response[1])
        # response is the command/response tuple - response[0] is the code
        if response[0] == 1: # The question response
            # Display it to the user.
            print(response[1])
            answer = input("Enter your answer > ")
            if answer.lower() != "end":
                send_binary(quiz_server, ["ANS", [answer, team_name]])
                send_binary(quiz_server, ["SCO", team_name]) 
            else:
                send_binary(quiz_server, ["END", team_name])
        if response[0] == 2:
            print(response[1])
        if response[0] == 3:
            print(response[1])
            send_binary(quiz_server, ["QUES", ""])
        if response[0] == 4:
            print(response[1])
            playing = False
            break

quiz_server.close()