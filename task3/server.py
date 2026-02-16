import socket
import threading
import time
import random

# Predefined set of trivia questions and answers
QUESTIONS = [
    ("What is the capital of France?", "Paris"),
    ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee"),
    ("What is the smallest prime number?", "2"),
    ("Which planet is known as the Red Planet?", "Mars"),
    ("What is the chemical symbol for water?", "H2O"),
    ("What color is the sky on a clear day?", "Blue"),
    ("What is 5 + 3?", "8"),
    ("Is the sun a star? (True/False)", "True"),
    ("What is the opposite of 'hot'?", "Cold"),
    ("Do fish live in water? (True/False)", "True"),
    ("How many legs does a spider have?", "8"),
    ("Is an elephant bigger than a mouse? (True/False)", "True"),
    ("What fruit is known for having seeds on the outside?", "Strawberry"),
    ("Is chocolate made from cocoa beans? (True/False)", "True"),
    ("What is the first letter of the English alphabet?", "A"),
    ("Do birds have feathers? (True/False)", "True"),
    ("How many days are in a week?", "7"),
    ("Is 2 + 2 equal to 5? (True/False)", "False"),
    ("What shape has three sides?", "Triangle"),
    ("Does the moon produce its own light? (True/False)", "False"),
    ("What is 10 divided by 2?", "5"),
    ("Is water wet? (True/False)", "True"),
    ("What do cows drink?", "Water"),
    ("Is fire cold? (True/False)", "False"),
    ("What is the color of bananas?", "Yellow"),
    ("Is Earth a planet? (True/False)", "True"),
    ("What is 1 + 1?", "2"),
    ("Is ice hot? (True/False)", "False"),
    ("What color are most leaves?", "Green"),
    ("Do cats bark? (True/False)", "False"),
    ("Which animal is known as 'man's best friend'?", "Dog"),
    ("Can humans breathe underwater without equipment? (True/False)", "False"),
    ("What do bees make?", "Honey"),
    ("Is the moon closer to Earth than the sun? (True/False)", "True"),
    ("What is 6 - 4?", "2"),
    ("Is snow white? (True/False)", "True"),
    ("What do you call a baby dog?", "Puppy"),
    ("Can fish fly? (True/False)", "False"),
    ("What is the number after 9?", "10"),
    ("Do apples grow on trees? (True/False)", "True"),
    ("Is the ocean salty? (True/False)", "True"),
    ("What is the color of the sun?", "Yellow"),
    ("What is 3 x 3?", "9"),
    ("Is chocolate sweet? (True/False)", "True"),
    ("Do chickens lay eggs? (True/False)", "True"),
    ("What animal says 'meow'?", "Cat"),
    ("Is fire orange? (True/False)", "True"),
    ("How many fingers does a human hand have?", "5"),
    ("Can airplanes fly? (True/False)", "True"),
]

MIN_PLAYERS = 2
ROUND_DELAY = 10
ANSWER_TIME = 30


class TriviaServer:
    def __init__(self, host='127.0.0.1', port=5689):
        self.server_address = (host, port)
        self.clients = {}
        self.scores = {}
        self.round_answers = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        print(f"Server started on {host}:{port}")
        self.current_question = None
        self.current_question_time = None
        self.running = True

    def start(self):
        threading.Thread(target=self.listen_for_clients, daemon=True).start()
        print(f"Waiting for at least {MIN_PLAYERS} players to join...")
        while len(self.clients) < MIN_PLAYERS:
            time.sleep(1)
        print(f"{MIN_PLAYERS} players have joined. Starting the game!")
        try:
            while self.running:
                if len(self.clients) >= MIN_PLAYERS:
                    self.play_round()
                else:
                    print("Not enough players. Exiting server...")
                    self.broadcast_message("Server is shutting down. Not enough players.")
                    self.running = False
                    self.sock.close()
                    exit()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
            self.broadcast_message("Server is shutting down. Goodbye!")
            self.running = False
            self.sock.close()

    def listen_for_clients(self):
        while self.running:
            try:
                message, client_address = self.sock.recvfrom(1024)
                message = message.decode('utf-8').strip()
                if client_address in self.clients:
                    if message.lower() == "quit":
                        self.remove_client(client_address, reason="Quit the game")
                    else:
                        threading.Thread(
                            target=self.process_answer, args=(message, client_address), daemon=True
                        ).start()
                elif message.lower() != "quit":
                    threading.Thread(
                        target=self.add_client, args=(message, client_address), daemon=True
                    ).start()
            except Exception as e:
                print(f"Error in listen_for_clients: {e}")

    def add_client(self, message, client_address):
        self.clients[client_address] = message
        self.scores[client_address] = 0
        print(f"New client joined: {client_address} ({message})")
        self.sock.sendto("Welcome to the trivia game!".encode('utf-8'), client_address)
        self.broadcast_message(f"{message} has joined the game!")

    def process_answer(self, message, client_address):
        if self.round_answers.get(client_address):  # Check if the client has already answered
            self.sock.sendto("You have already answered this question.".encode('utf-8'), client_address)
            return

        client_answer = message
        print(f"Answer received from {self.clients[client_address]} {client_address}: {client_answer}")

        if self.current_question and (time.time() - self.current_question_time <= ANSWER_TIME):
            if client_answer.lower() == self.current_question[1].lower():
                self.scores[client_address] += int(ANSWER_TIME - (time.time() - self.current_question_time))
                self.sock.sendto("Correct!".encode('utf-8'), client_address)
            else:
                self.sock.sendto("Wrong answer.".encode('utf-8'), client_address)

            self.round_answers[client_address] = True  # Mark client as having answered

    def play_round(self):
        print("Starting a new round...")
        self.broadcast_message("A new round is starting soon!")
        time.sleep(ROUND_DELAY)

        # Select a random set of questions for this round
        questions = random.sample(QUESTIONS, 4)

        # Track players who didn't answer any question in this round
        unresponsive_clients = set(self.clients.keys())

        for idx, (question, answer) in enumerate(questions, start=1):
            # Reset round_answers at the start of each question
            self.round_answers = {client: False for client in self.clients}

            # Set the current question and start the timer
            self.current_question = (question, answer)
            self.current_question_time = time.time()

            # Broadcast the question to all clients
            self.broadcast_message(f"Question {idx}: {question}")
            print(f"Broadcasted question {idx}: {question}")

            # Wait for the answer time to elapse
            time.sleep(ANSWER_TIME)

            # Remove players who responded to the question from the unresponsive set
            for client, answered in self.round_answers.items():
                if answered:
                    unresponsive_clients.discard(client)

            # Broadcast the correct answer and display scores
            self.broadcast_message(f"\nThe correct answer was: {answer}")
            print(f"The correct answer was: {answer}")
            self.display_scores()

            # If there are not enough players left after a question, stop the game
            if len(self.clients) < MIN_PLAYERS:
                print("Not enough players to continue. Server shutting down.")
                self.broadcast_message("Not enough players to continue. Server shutting down.")
                self.running = False
                self.sock.close()
                exit()

        # After all questions, kick unresponsive clients
        for client in unresponsive_clients:
            self.remove_client(client, reason="Did not respond during the entire round")

    def remove_client(self, client_address, reason="Quit the game"):
        if client_address in self.clients:
            client_name = self.clients[client_address]
            print(f"Removing client {client_name} ({client_address}): {reason}")
            del self.clients[client_address]
            del self.scores[client_address]
            if client_address in self.round_answers:
                del self.round_answers[client_address]
            self.sock.sendto("You have been removed from the game.".encode('utf-8'), client_address)
            self.broadcast_message(f"{client_name} has left the game!")

    def broadcast_message(self, message):
        for client in self.clients.keys():
            self.sock.sendto(message.encode('utf-8'), client)

    def display_scores(self):
        leaderboard = "\nLeaderboard:\n"
        for client, score in sorted(self.scores.items(), key=lambda x: x[1], reverse=True):
            leaderboard += f"{self.clients[client]}: {score} points\n"
        print(leaderboard)
        self.broadcast_message(leaderboard)


if __name__ == "__main__":
    server = TriviaServer()
    server.start()
