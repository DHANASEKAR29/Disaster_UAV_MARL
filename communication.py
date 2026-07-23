class Communication:

    def __init__(self):
        self.messages = []

    def send(self, sender, message):

        msg = f"{sender} : {message}"

        self.messages.append(msg)

        print(f"[COMM] {msg}")

    def receive(self, receiver, sender, message):

        msg = f"{receiver} received '{message}' from {sender}"

        self.messages.append(msg)

        print(f"[COMM] {msg}")

    def mission_accepted(self, drone):

        msg = f"{drone} : MISSION ACCEPTED"

        self.messages.append(msg)

        print(f"[COMM] {msg}")

    def show_messages(self):

        print("\n========== COMMUNICATION LOG ==========")

        if len(self.messages) == 0:
            print("No Messages")
            return

        for msg in self.messages:
            print(msg)