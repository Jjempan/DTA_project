# DTA_project
Project written in Python exploring M/M/1 queueing theory with SimPy, an event simulator for Python.

# Queueing Theory Simulation in Python

This Python simulation explores queueing theory using a library scenario where visitors borrow books (representing servers). The code uses SimPy to simulate the queueing process and calculates different metrics, as arrival rates, service rates, and utilization 

# Project Overview

This simulation models visitors arriving at a library to borrow a book, the book is acting as a server. Costumers may leave (packet-drop) if the queue reaches a certain limit, simulating a system with a maximum queue size. The library has:

- One book (= one server) that are borrowed by visitors.
- A limited loan period with probabilities determining on-time returns.
- A maximum queue length; additional visitors leave if this length is reached.

# Requirements

- Python 3.x
- SimPy
- Matplotlib

# Install required libraries using:

bash:
pip install simpy matplotlib

# Simulation Parameters

RANDOM_SEED: Controls randomness for repeatable results.
NUM_COPIES: Number of copies (servers) for each book.
BOOK_TITLES: List of book titles (simulated servers).
LOAN_DURATION: Borrow duration for each book.
RETURN_PROB: Probability of returning books on time.
SIM_TIME: Total simulation time (days).
MAX_QUEUE_SIZE: Maximum number of visitors in the queue.


# Code Structure

1. Visitor Behavior: Each visitor arrives randomly and tries to borrow a book. If the queue for the book is full, they leave (packet-drop). If they successfully borrow a book, they return it after a set duration, with a 20% probability of delay.

2. Library Setup: Initializes library resources (books) and continuously spawns new visitors.

3. Queue Statistics: Calculates M/M/1 queue statistics:
   - λ (arrival rate), μ(service rate), and ρ (intensity).
   - Average system length (L), wait time (W), queue length (Lq), and queue wait time (Wq).

# Results

The program calculates queue metrics and displays:

Arrival Rate (λ and Service Rate (μ)
System Intensity (ρ): Ratio of arrival rate to service rate.
Average System Length (L): Expected number of visitors in the system.
Average Wait Time (W): Expected time a visitor spends in the system.
Average Queue Length (Lq): Expected number of visitors waiting.
Queue Wait Time (Wq): Expected time a visitor waits in the queue.
Packet-Drops: Number of visitors who leave due to a full queue.

# Visualizations

Wait Times: Average, maximum, and minimum wait times for each book.
Packet Drops: Number of packet-drops for each book.

# Running the Simulation

Run the script directly:

bash
python library_queue_simpy.py





