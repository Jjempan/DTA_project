import simpy
import random
import matplotlib.pyplot as plt
# Konstantinställningar

RANDOM_SEED = 42
NUM_COPIES = 1  # Antal kopior av varje bok
BOOK_TITLES = [
    "Server 1",
    "Server 2"
]

LOAN_DURATION = 15  # Lånetid i dagar (motsvarar servertime)
RETURN_PROB = 0.8  # Sannolikheten för att boken lämnas tillbaka i tid
SIM_TIME = 365  # Simuleringstid i dagar
MAX_QUEUE_SIZE = 10  # Max antal personer i kön
# Variabler för att logga data
wait_times = {title: [] for title in BOOK_TITLES}
queue_drops = {title: 0 for title in BOOK_TITLES}
arrival_times = {title: [] for title in BOOK_TITLES}
def visitor(env, name, library, book_title):
    """Simulerar en besökare som vill låna en bok och senare lämna tillbaka den."""
    arrival_time = env.now
    queue_length = len(library[book_title].queue)
    
    # Logga ankomsttiden för beräkning av ankomsttakt
    arrival_times[book_title].append(arrival_time)
    
    # Om kön är full, hoppar besökaren av (packet-drop)

    if queue_length >= MAX_QUEUE_SIZE:
        queue_drops[book_title] += 1
        print(f'{env.now:.1f} - {name} försökte låna "{book_title}" men kön är full (packet-drop)')
        return
    
    print(f'{env.now:.1f} - {name} önskar låna "{book_title}"')
    with library[book_title].request() as request:
        # Besökaren står i kö för att låna boken
        yield request
        wait_time = env.now - arrival_time
        wait_times[book_title].append(wait_time)
        print(f'{env.now:.1f} - {name} lånar "{book_title}" (väntetid: {wait_time:.1f} dagar)')
        
        # Lånetid
        loan_time = LOAN_DURATION
        yield env.timeout(loan_time)
        
        # Returnera boken med viss sannolikhet
        if random.uniform(0, 1) < RETURN_PROB:
            print(f'{env.now:.1f} - {name} lämnar tillbaka "{book_title}" i tid')
        else:
            # Om besökaren är försenad med att lämna tillbaka boken
            delay = random.randint(1, 7)
            yield env.timeout(delay)
            print(f'{env.now:.1f} - {name} lämnar tillbaka "{book_title}" försenat med {delay} dagar')
def setup(env, num_copies, book_titles):
    """Setup av biblioteket med resurser för varje bok."""
    # Skapa en resurs för varje bok i biblioteket
    library = {title: simpy.Resource(env, num_copies) for title in book_titles}
    
    # Fortsätt skapa nya besökare under simuleringen
    i = 0
    while True:
        yield env.timeout(random.randint(1, 5))  # Ny besökare var 1-5 dag
        i += 1
        book = random.choice(book_titles)
        env.process(visitor(env, f'Besökare {i}', library, book))
# Starta simuleringen

print("Bibliotekssimulering startar...")
random.seed(RANDOM_SEED)
env = simpy.Environment()
env.process(setup(env, NUM_COPIES, BOOK_TITLES))
# Kör simuleringen

env.run(until=SIM_TIME)
# Beräkningar för M/M/1-köstatistik

arrival_rates = {title: len(arrival_times) / SIM_TIME for title, arrival_times in arrival_times.items()}
service_rates = {title: 1 / LOAN_DURATION for title in BOOK_TITLES}
# Logga köstatistik

queue_statistics = {}
for title in BOOK_TITLES:
    λ = arrival_rates[title]  # Ankomsttakt
    μ = service_rates[title]  # Tjänstetakt
    ρ = λ / μ  # Intensitet
    L = λ / (μ - λ) if μ > λ else float('inf')  # Genomsnittligt antal i systemet
    W = 1 / (μ - λ) if μ > λ else float('inf')  # Genomsnittlig tid i systemet
    Lq = (λ ** 2) / (μ * (μ - λ)) if μ > λ else float('inf')  # Genomsnittligt antal i kön
    Wq = λ / (μ * (μ - λ)) if μ > λ else float('inf')  # Genomsnittlig tid i kön
    
    queue_statistics[title] = {
        'λ': λ,
        'μ': μ,
        'ρ': ρ,
        'L': L,
        'W': W,
        'Lq': Lq,
        'Wq': Wq,
        'drops': queue_drops[title]
    }
# Visa köstatistik

for title, stats in queue_statistics.items():
    print(f'\nKöstatistik för {title}:')
    print(f"Ankomsttakt (λ): {stats['λ']:.2f}")
    print(f"Tjänstetakt (μ): {stats['μ']:.2f}")
    print(f"Intensitet (ρ): {stats['ρ']:.2f}")
    print(f"Genomsnittligt antal i systemet (L): {stats['L']:.2f}")
    print(f"Genomsnittlig tid i systemet (W): {stats['W']:.2f} dagar")
    print(f"Genomsnittligt antal i kön (Lq): {stats['Lq']:.2f}")
    print(f"Genomsnittlig tid i kön (Wq): {stats['Wq']:.2f} dagar")
    print(f"Antal packet-drops: {stats['drops']}")

# Visualisera resultaten med en mer modern och stilren design

plt.style.use('ggplot')
# Average, Max, and Min waiting time för varje bok

plt.figure(figsize=(12, 6))
bar_width = 0.2
index = range(len(BOOK_TITLES))
avg_wait_times = [sum(wait_times[title]) / len(wait_times[title]) if wait_times[title] else 0 for title in BOOK_TITLES]
max_wait_times = [max(wait_times[title]) if wait_times[title] else 0 for title in BOOK_TITLES]
min_wait_times = [min(wait_times[title]) if wait_times[title] else 0 for title in BOOK_TITLES]

plt.bar([i - bar_width for i in index], avg_wait_times, bar_width, color='#6baed6', label='Average Wait Time')
plt.bar(index, max_wait_times, bar_width, color='#fd8d3c', label='Max Wait Time')
plt.bar([i + bar_width for i in index], min_wait_times, bar_width, color='#74c476', label='Min Wait Time')
plt.xticks(index, BOOK_TITLES)
plt.ylabel('Väntetid (dagar)')
plt.title('Väntetider för varje bok (server)')
plt.legend()
plt.tight_layout()
plt.show()
# Visualisera packet-drops för varje bok

plt.figure(figsize=(12, 6))
plt.bar(queue_drops.keys(), queue_drops.values(), color='#9e9ac8')
plt.xlabel('Bok (Server)')
plt.ylabel('Antal packet-drops')
plt.title('Antal packet-drops per bok (server)')
plt.tight_layout()
plt.show()
