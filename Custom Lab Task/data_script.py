import csv
import random
import datetime

# This file is used to create fake data for processes that were active on a host device over a day

normal_names = ['chrome.exe', 'explorer.exe', 'notepad.exe', 'svchost.exe', 'cmd.exe', 'python.exe', 'code.exe']
suspicious_names = ['svhost.exe', 'mimikatz.exe', 'evil.exe', 'trojan.exe', 'backdoor123.exe', 'pwstealer.exe']
normal_paths = ['C:\\Program Files\\', 'C:\\Windows\\System32\\', 'C:\\Users\\Public\\']
suspicious_paths = ['C:\\Users\\Bob\\AppData\\Roaming\\', 'C:\\Temp\\', 'D:\\Games\\', 'C:\\FakeDir\\']
users = ['SYSTEM', 'Admin', 'Bob', 'Alice', 'Service']

TOTAL_ENTRIES = 50000
SUSPICIOUS_RATE = 0.1  # Increased suspicious rate for more diversity

def generate_process(pid):
    # Define if the process is suspicious or not based on a higher suspicious rate
    is_suspicious = random.random() < SUSPICIOUS_RATE

    # Process name and path
    name = random.choice(suspicious_names if is_suspicious else normal_names)
    path = random.choice(suspicious_paths if is_suspicious else normal_paths)
    full_path = path + name

    # CPU and memory usage
    cpu = round(random.uniform(60, 95) if is_suspicious else random.uniform(0.1, 20.0), 2)
    mem = round(random.uniform(500, 1000) if is_suspicious else random.uniform(10, 250), 1)

    # Parent process ID
    parent_pid = random.randint(1, pid-1) if pid > 1 else 0

    # Start time (randomized in the last 30 days)
    start_time = datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 2592000))

    # User and signature info
    user = random.choice(users)
    signed = 'No' if is_suspicious else random.choice(['Yes', 'Yes', 'Yes', 'No'])

    # Network connections
    network_conns = random.randint(40, 100) if is_suspicious else random.randint(0, 15)

    # Integrity levels (more likely for suspicious processes to be "High" or "System")
    integrity = random.choices(['Low', 'Medium', 'High', 'System'], weights=[1, 6, 2, 1])[0]

    # Mismatch and injection checks
    mismatch = 'True' if is_suspicious and 'svchost' in name.lower() and 'Users' in path else 'False'
    injected = 'True' if is_suspicious and random.random() < 0.6 else 'False'

    # Combine results into a dictionary
    return {
        'PID': pid,
        'ProcessName': name,
        'CPU%': cpu,
        'MemMB': mem,
        'ParentPID': parent_pid,
        'StartTime': start_time.strftime("%Y-%m-%d %H:%M"),
        'CmdLine': f"{full_path} --run" if is_suspicious else full_path,
        'User': user,
        'Signed': signed,
        'NetworkConnections': network_conns,
        'IntegrityLevel': integrity,
        'ImagePathMismatch': mismatch,
        'Injected': injected,
        'Class': 1 if is_suspicious else 0  # Class is 1 for suspicious processes, 0 for normal
    }

# Write the generated data to a CSV file
with open('processes_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['PID', 'ProcessName', 'CPU%', 'MemMB', 'ParentPID', 'StartTime', 'CmdLine',
                  'User', 'Signed', 'NetworkConnections', 'IntegrityLevel',
                  'ImagePathMismatch', 'Injected', 'Class']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for pid in range(1, TOTAL_ENTRIES + 1):
        writer.writerow(generate_process(pid))

print(f"Generated {TOTAL_ENTRIES} entries in 'processes_data.csv'")
