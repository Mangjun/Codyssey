import pyzipper
import string
import random
import time
import itertools
from datetime import datetime
from multiprocessing import Process, Value, Lock, Manager

ZIP_PATH = 'emergency_storage_key.zip'
TARGET_FILE = 'password.txt'
NUM_WORKERS = 8

LETTERS = string.ascii_lowercase
DIGITS = string.digits

def try_password(zip_path, target_file, password):
    try:
        with pyzipper.ZipFile(zip_path) as zf:
            data = zf.read(target_file, pwd=password.encode())
            return True
    except Exception as e:
        return False

def generate_suffix(pattern_type):
    if pattern_type == "5L1D":
        return [''.join(lp) + d for lp in itertools.product(LETTERS, repeat=3) for d in DIGITS]
    elif pattern_type == "4L2D":
        return [''.join(lp) + ''.join(dp) for lp in itertools.product(LETTERS, repeat=2) for dp in itertools.product(DIGITS, repeat=2)]
    elif pattern_type == "6L":
        return [''.join(pw) for pw in itertools.product(LETTERS, repeat=4)]
    elif pattern_type == "3L3D":
        return [''.join(lp) + ''.join(dp) for lp in itertools.product(LETTERS, repeat=1) for dp in itertools.product(DIGITS, repeat=3)]
    elif pattern_type == "6D":
        return [''.join(pw) for pw in itertools.product(DIGITS, repeat=6)]
    elif pattern_type == "2L4D":
        return [''.join(dp) for dp in itertools.product(DIGITS, repeat=4)]
    elif pattern_type == "1L5D":
        return [''.join(dp) for dp in itertools.product(DIGITS, repeat=5)]
    elif pattern_type == "ALL":
        return [''.join(pw) for pw in itertools.product(LETTERS + DIGITS, repeat=4)]
    else:
        raise NotImplementedError

def run_pattern_by_prefix(pattern_type, found_flag, lock, attempt_count, start_time):
    print(f"▶ Starting pattern: {pattern_type}")

    if pattern_type == "6D":
        prefixes = ['']
    elif pattern_type == "1L5D":
        prefixes = [l for l in LETTERS]
    else:
        prefixes = [''.join(p) for p in itertools.product(LETTERS, repeat=2)]

    random.shuffle(prefixes)
    chunk_size = len(prefixes) // NUM_WORKERS
    chunks = [prefixes[i * chunk_size:(i + 1) * chunk_size] for i in range(NUM_WORKERS - 1)]
    chunks.append(prefixes[(NUM_WORKERS - 1) * chunk_size:])

    suffixes = list(generate_suffix(pattern_type))
    random.shuffle(suffixes)
    processes = []
    for chunk in chunks:
        p = Process(target=worker, args=(chunk, suffixes, found_flag, lock, attempt_count, start_time, pattern_type))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    return found_flag.value

def worker(prefixes, suffixes, found_flag, lock, attempt_count, start_time, pattern_type):
    for prefix in prefixes:
        for suffix in suffixes:
            if found_flag.value:
                return
            pw = prefix + suffix
            if try_password(ZIP_PATH, TARGET_FILE, pw):
                with lock:
                    if not found_flag.value:
                        found_flag.value = True
                        elapsed = time.time() - start_time.value
                        print(f"[SUCCESS] Password found: {pw} (Pattern: {pattern_type}, Attempts: {attempt_count.value}, Elapsed: {elapsed:.2f}s)")
                        with open("password.txt", "w") as f:
                            f.write(pw)
                return
            with lock:
                attempt_count.value += 1
                if attempt_count.value % 10000 == 0:
                    elapsed = time.time() - start_time.value
                    print(f"[{pattern_type}] Attempts: {attempt_count.value}, Elapsed: {elapsed:.2f}s, Trying: {pw}")

def unlock_zip():
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    manager = Manager()
    found_flag = Value('b', False)
    attempt_count = Value('i', 0)
    lock = Lock()
    start_time = Value('d', time.time())

    pattern_order = ["4L2D", "2L4D", "3L3D", "5L1D", "6D", "6L", "1L5D", "ALL"]

    for pattern in pattern_order:
        if run_pattern_by_prefix(pattern, found_flag, lock, attempt_count, start_time):
            break

    if not found_flag.value:
        print("Password not found.")
    else:
        print("Password saved to 'password.txt'")

if __name__ == "__main__":
    unlock_zip()
