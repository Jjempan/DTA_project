import simpy
import random
import matplotlib.pyplot as plt

# Konstantinställningar
RANDOM_SEED = 42
NUM_COPIES = 1  # Antal kopior av varje bok
BOOK_TITLE = "Server 1"

LOAN_DURATION = 5  # Lånetid i dagar (motsvarar servertime)
RETURN_PROB = 0.8  # Sannolikheten för att boken lämnas tillbaka i tid
SIM_TIME = 365  # Simuleringstid i dagar
MAX_QUEUE_SIZE = 10  # Max antal personer i kön

# Variabler för att logga data
wait_times = []
queue_drops = 0
arrival_times = []
busy_time = 0  # Empirical utilization
queue_lengths = []  # För att logga köns längd över tid

def visitor(env, name, library):
    """Simulerar en besökare som vill låna en bok och senare lämna tillbaka den."""
    global busy_time
    arrival_time = env.now
    queue_length = len(library.queue)
    
    # Logga ankomsttiden och kölängden för att beräkna genomsnittlig kölängd
    arrival_times.append(arrival_time)
    queue_lengths.append(queue_length)
    
    # Om kön är full, hoppar besökaren av (packet-drop)
    if queue_length >= MAX_QUEUE_SIZE:
        global queue_drops
        queue_drops += 1
        return
    
    with library.request() as request:
        yield request
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        # Logga upptagen tid för empirisk utilization
        loan_time = LOAN_DURATION
        busy_time += loan_time
        
        yield env.timeout(loan_time)
        
        # Returnera boken med viss sannolikhet
        if random.uniform(0, 1) >= RETURN_PROB:
            delay = random.randint(1, 7)
            busy_time += delay
            yield env.timeout(delay)

def setup(env, num_copies, book_title):
    """Setup av biblioteket med resurs för boken."""
    library = simpy.Resource(env, num_copies)
    
    i = 0
    while True:
        yield env.timeout(random.randint(1, 5))  # Ny besökare var 1-5 dag
        i += 1
        env.process(visitor(env, f'Besökare {i}', library))

# Starta simuleringen
print("Bibliotekssimulering startar...")
random.seed(RANDOM_SEED)
env = simpy.Environment()
env.process(setup(env, NUM_COPIES, BOOK_TITLE))

# Kör simuleringen
env.run(until=SIM_TIME)

# Beräkningar för M/M/1-köstatistik
λ = len(arrival_times) / SIM_TIME  # Ankomsttakt
μ = 1 / LOAN_DURATION  # Tjänstetakt
ρ = λ / μ  # Teoretisk intensitet
L = λ / (μ - λ) if μ > λ else float('inf')  # Genomsnittligt antal i systemet
W = 1 / (μ - λ) if μ > λ else float('inf')  # Genomsnittlig tid i systemet
Lq = (λ ** 2) / (μ * (μ - λ)) if μ > λ else float('inf')  # Genomsnittligt antal i kön
Wq = λ / (μ * (μ - λ)) if μ > λ else float('inf')  # Genomsnittlig tid i kön
empirical_utilization = busy_time / SIM_TIME
average_queue_length = sum(queue_lengths) / len(queue_lengths) if queue_lengths else 0  # Genomsnittlig kölängd

# Visa köstatistik
print(f'\nKöstatistik för {BOOK_TITLE}:')
print(f"Ankomsttakt (λ): {λ:.2f}")
print(f"Tjänstetakt (μ): {μ:.2f}")
print(f"Teoretisk intensitet (ρ): {ρ:.2f}")
print(f"Empirisk intensitet: {empirical_utilization:.2f}")
print(f"Genomsnittligt antal i systemet (L): {L:.2f}")
print(f"Genomsnittlig tid i systemet (W): {W:.2f} dagar")
print(f"Genomsnittligt antal i kön (Lq): {Lq:.2f}")
print(f"Genomsnittlig tid i kön (Wq): {Wq:.2f} dagar")
print(f"Genomsnittlig kölängd: {average_queue_length:.2f}")
print(f"Antal packet-drops: {queue_drops}")

# Visualisera packet-drops och empirisk intensitet
plt.style.use('ggplot')

# Visualisera packet-drops
plt.figure(figsize=(10, 6))
plt.bar(["Packet Drops"], [queue_drops], color='#9e9ac8')
plt.ylabel('Antal packet-drops')
plt.title('Antal packet-drops')
plt.show()

# Visualisera empirisk intensitet och genomsnittlig kölängd
plt.figure(figsize=(10, 6))
plt.bar(["Empirisk Intensitet", "Genomsnittlig Kö"], [empirical_utilization, average_queue_length], color=['#74c476', '#6baed6'])
plt.ylabel('Värde')
plt.title('Empirisk Intensitet och Genomsnittlig Kö')
plt.show()
