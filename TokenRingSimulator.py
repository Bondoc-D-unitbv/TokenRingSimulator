import random
from collections import deque

class Computer:
    def __init__(self, id, ip):
        self.id = id
        self.ip = ip
        self.received_messages = []

    def receive_message(self, message):
        self.received_messages.append(message)
        print(f"Computer {self.id} ({self.ip}) received message: {message}")

class Token:
    def __init__(self):
        self.source_ip = None
        self.destination_ip = None
        self.message = None
        self.reached_destination = False
        self.free = True
        self.history = []
        self.full_journey = []
        self.previous_path = []

    def reset(self):
        self.source_ip = None
        self.destination_ip = None
        self.message = None
        self.reached_destination = False
        self.free = True
        self.history.clear()
        self.full_journey.clear()
        self.previous_path.clear()


def generate_unique_ips(n):
    return random.sample([f"192.168.1.{i}" for i in range(1, 256)], n)


def initialize_network():
    computers = []
    unique_ips = generate_unique_ips(10)
    for i in range(1, 11):
        computers.append(Computer(i, unique_ips[i - 1]))
    return computers


def token_ring_simulation():
    computers = initialize_network()
    ring = deque(computers)
    token = Token()

    direction_input = input("Choose direction (1 for clockwise, 2 for counterclockwise): ")
    while direction_input not in ["1", "2"]:
        direction_input = input("Invalid input. Choose 1 for clockwise or 2 for counterclockwise: ")
    direction = "clockwise" if direction_input == "1" else "counterclockwise"

    source = random.choice(computers)  # Starting point remains from the last source

    for _ in range(10):  # 10 simulations

        print("Message number:", _ + 1)

        destination = random.choice([c for c in computers if c.id != source.id])
        token.source_ip = source.ip
        token.destination_ip = destination.ip
        token.message = f"Hello from {source.id} to {destination.id}!"
        token.free = False

        print(f"Sending message from {source.id} ({source.ip}) to {destination.id} ({destination.ip})")

        # Track journey from previous source to current source
        token.previous_path.clear()
        while ring[0].ip != source.ip:
            token.previous_path.append(ring[0].id)
            ring.rotate(-1 if direction == "clockwise" else 1)
        token.previous_path.append(source.id)  # Append current source

        # Track full journey from source -> destination -> source
        reached_destination = False

        while not reached_destination:
            current_pc = ring[0]
            token.history.append(current_pc.id)
            if not token.full_journey or token.full_journey[-1] != current_pc.id:
                token.full_journey.append(current_pc.id)

            if current_pc.ip == token.destination_ip:
                current_pc.receive_message(token.message)
                token.reached_destination = True
                reached_destination = True

            ring.rotate(-1 if direction == "clockwise" else 1)

            if ring[0].ip == token.source_ip and not reached_destination:
                print("Message failed to reach destination!")
                break

        # Append return journey from destination back to source
        while ring[0].ip != token.source_ip:
            current_pc = ring[0]
            if not token.full_journey or token.full_journey[-1] != current_pc.id:
                token.full_journey.append(current_pc.id)
            ring.rotate(-1 if direction == "clockwise" else 1)
        token.full_journey.append(source.id)  # Final return to source
        print("Previous source path:", " -> ".join(map(str, token.previous_path)))
        print("Token history (Path taken):", " -> ".join(map(str, token.history)))
        print("Full journey (Complete round-trip):", " -> ".join(map(str, token.full_journey)))

        token.reset()
        print("---------------------------------")

        source = destination  # Set next source as the last destination


token_ring_simulation()
