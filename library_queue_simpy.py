import simpy
import random
 
# Konstantinställningar
RANDOM_SEED = 42
NUM_COPIES = 1  # Antal kopior av varje bok
BOOK_TITLE = "Server 1"

LOAN_DURATION = 4  # Lånetid i dagar (motsvarar servertime)
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
        print(f"{env.now:.2f} dagar: {name} kunde inte gå med i kön (queue full).")
        return
    
    print(f"{env.now:.2f} dagar: {name} har anlänt och ställt sig i kö.")

    with library.request() as request:
        yield request
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        print(f"{env.now:.2f} dagar: {name} börjar låna boken. Väntetid: {wait_time:.2f} dagar.")
        
        # Logga upptagen tid för empirisk utilization
        loan_time = LOAN_DURATION
        busy_time += loan_time
        
        yield env.timeout(loan_time)
        
        print(f"{env.now:.2f} dagar: {name} lämnar tillbaka boken efter {loan_time} dagar.")
        
        # Returnera boken med viss sannolikhet
        if random.uniform(0, 1) >= RETURN_PROB:
            delay = random.randint(1, 7)
            busy_time += delay
            print(f"{env.now:.2f} dagar: {name} är försenad och håller boken {delay} extra dagar.")
            yield env.timeout(delay)
            print(f"{env.now:.2f} dagar: {name} har slutligen lämnat tillbaka boken efter förseningen.")

def setup(env, num_copies, book_title):
    """Setup av biblioteket med resurs för boken."""
    library = simpy.Resource(env, num_copies)
    
    i = 0
    while True:
        yield env.timeout(random.randint(1, 10))  # Ny besökare var 1-10 dag
        i += 1
        env.process(visitor(env, f'Besökare {i}', library))

# Starta simuleringen
print("Bibliotekssimulering startar...")
random.seed(RANDOM_SEED)
env = simpy.Environment()
env.process(setup(env, NUM_COPIES, BOOK_TITLE))

# Kör simuleringen
env.run(until=SIM_TIME)

# Beräkningar för M/M/1/k
λ = len(arrival_times) / SIM_TIME  # Ankomsttakt
μ = 1 / LOAN_DURATION  # Tjänstetakt
ρ = λ / μ  # Teoretisk intensitet
empirical_utilization = busy_time / SIM_TIME
average_queue_length = sum(queue_lengths) / len(queue_lengths) if queue_lengths else 0  # Genomsnittlig kölängd


successful_loans = len(wait_times)
throughput_per_loan_period = successful_loans / (SIM_TIME / LOAN_DURATION)


print(f'\nKöstatistik för {BOOK_TITLE}:')
print(f"Ankomsttakt (λ): {λ:.2f}")
print(f"Tjänstetakt (μ): {μ:.2f}")
print(f"Teoretisk intensitet (ρ): {ρ:.2f}")
print(f"Empirisk intensitet: {empirical_utilization:.2f}")
print(f"Genomsnittlig kölängd: {average_queue_length:.2f}")
print(f"Antal packet-drops: {queue_drops}")
print(f"Genomströmning (Throughput) per låneperiod: {throughput_per_loan_period:.2f} lån per låneperiod")
