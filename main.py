from dataclasses import dataclass
from collections import deque
import random

# Définition d'un processus
@dataclass
class Process:
    pid: int
    status : str
    arrival_time : int
    burst_time : int
    bursts : list
    remaining_in_burst : int
    blocked_until : int = None
    start_time : int = None
    finish_time : int = None
    burst_index : int = 0

# Liste de processus (file FIFO)
def generer_processus(n):
    liste_processus = deque()
    for i in range(1, n + 1):
        temps_init = random.randint(0,5)
        bursts_CPU = random.randint(1,5)
        liste_bursts = []
        CPU_tot = 0
        for j in range(0, bursts_CPU):
            CPU = random.randint(1,5)
            IO = random.randint(1,4)
            liste_bursts.append(("CPU", CPU))
            CPU_tot += CPU
            if j < bursts_CPU-1:
                liste_bursts.append(("IO", IO))
        liste_processus.append(Process(pid=i, status="NEW", arrival_time=temps_init, burst_time=CPU_tot, bursts=liste_bursts, remaining_in_burst=liste_bursts[0][1]))
    return liste_processus

incoming = list(generer_processus(3))
queue = deque()
blocked = []

def trie_par_arrive(processus):
    for i in range(len(processus)):
        for j in range(i + 1, len(processus)):
            if processus[i].arrival_time > processus[j].arrival_time:
                processus[i], processus[j] = processus[j], processus[i]
    return processus

incoming_trie = list(trie_par_arrive(incoming))

def roundrobin(running, quantum_left, time, blocked):
    if running.start_time is None:
        running.start_time = time
    running.remaining_in_burst -= 1
    quantum_left -= 1
    if running.remaining_in_burst == 0 and running.bursts[running.burst_index][0] == "CPU" and running.burst_index < len(running.bursts)-1:
        running.burst_index += 1
        running.remaining_in_burst = running.bursts[running.burst_index][1]
        running.status = "BLOCKED"
        blocked.append(running)
        running.blocked_until = time+1+running.remaining_in_burst
        quantum_left = 0
        running = None
        return running
    elif running.remaining_in_burst == 0 and running.burst_index == len(running.bursts) - 1:
        running.finish_time = time+1
        running.status = "FINISHED"
        quantum_left = 0
        print(f"Temps {running.finish_time}: Processus {running.pid} {running.status}, Réponse : {running.start_time - running.arrival_time}, Turnaround : {running.finish_time - running.arrival_time}, Waiting : {(running.finish_time - running.arrival_time)- running.burst_time}")
        return running
    elif quantum_left == 0 and running.remaining_in_burst > 0:
        running.status = "READY"
        quantum_left = 0
        #print(f"Quantum expiré, processus {current.pid} arrêté, nouveau processus en cours.")
    return quantum_left

cpu_trace = []
running = None
time = 0
quantum_left = 0
quantum = 2

print("=== Simulation RR ===")
print("Quantum = ", quantum)

while incoming_trie or queue or blocked or running is  not None:
    while incoming_trie and incoming_trie[0].arrival_time <= time:
        process = incoming_trie.pop(0)
        process.status = "READY"
        queue.append(process)
        print(f"Temps {time}: admission P{process.pid} (arrival={process.arrival_time})")
    still_blocked = []

    for p in blocked:
        if p.blocked_until <= time:
            print(f"Temps {time}: P{p.pid} UNBLOCK -> READY")
            p.status = "READY"
            p.burst_index += 1
            p.remaining_in_burst = p.bursts[p.burst_index][1]
            queue.append(p)
        else:
            still_blocked.append(p)
    blocked = still_blocked
    
    if running is None and queue:
        running = queue.popleft()
        quantum_left = quantum
    
    if running is None:
        print("IDLE")
        cpu_trace.append("IDLE")
        quantum_left = 0
    else :
        cpu_trace.append(running.pid)
        quantum_left, action = roundrobin(running, quantum_left, time, blocked)
    time += 1

print("Simulation terminée.")

start = 0
current = cpu_trace[0]

for t in range(1, len(cpu_trace)):
    if cpu_trace[t] != current:
        print(f"[{start}-{t}] {current}")
        start = t
        current = cpu_trace[t]
print(f"[{start}-{len(cpu_trace)}] {current}")