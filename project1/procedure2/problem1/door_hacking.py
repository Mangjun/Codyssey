import pyzipper
import itertools
import string
import random
import time
from datetime import datetime
from multiprocessing import Process, Value, Lock, Manager

# 접근 방식: 사람들이 자주 사용하는 패턴을 기반으로 암호를 추측

ZIP_PATH = 'emergency_storage_key.zip'
TARGET_FILE = 'password.txt'
NUM_WORKERS = 8 # CPU 코어 수

LETTERS = string.ascii_lowercase # [a-z]
DIGITS = string.digits # [0-9]

# ZIP 파일 암호 해제
def try_password(zip_path, target_file, password):
    try:
        with pyzipper.ZipFile(zip_path) as zf:
            data = zf.read(target_file, pwd=password.encode())
            return True
    except Exception as e:
        return False

# 패턴에 따라 접미사(뒤 4자리) 생성
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
        return [''.join(pw) for pw in itertools.product(DIGITS, repeat=4)]
    elif pattern_type == "2L4D":
        return [''.join(dp) for dp in itertools.product(DIGITS, repeat=4)]
    elif pattern_type == "1L5D":
        return [''.join(dp) for dp in itertools.product(DIGITS, repeat=4)]
    elif pattern_type == "ALL":
        return [''.join(pw) for pw in itertools.product(LETTERS + DIGITS, repeat=4)]
    else:
        raise NotImplementedError

# 프로세스에게 케이스 나눠서 실행
def run_pattern_by_prefix(pattern_type, found_flag, lock, attempt_count, start_time):
    print(f"▶ Starting pattern: {pattern_type}")

    # 패턴에 따라 접두사(앞 2자리) 생성
    if pattern_type == "6D":
        prefixes = [''.join(p) for p in itertools.product(DIGITS, repeat=2)]
    elif pattern_type == "1L5D":
        prefixes = [''.join(lp) + ''.join(dp) for lp in itertools.product(LETTERS, repeat=1) for dp in itertools.product(DIGITS, repeat=1)]
    elif pattern_type == 'ALL':
        prefixes = [''.join(p) for p in itertools.product(LETTERS + DIGITS, repeat=2)]
    else:
        prefixes = [''.join(p) for p in itertools.product(LETTERS, repeat=2)]

    random.shuffle(prefixes) # 시간 단축을 위해 랜덤하게 섞어줌
    chunk_size = len(prefixes) // NUM_WORKERS # 프로세스 수에 맞게 나누기
    chunks = [prefixes[i * chunk_size:(i + 1) * chunk_size] for i in range(NUM_WORKERS - 1)]
    chunks.append(prefixes[(NUM_WORKERS - 1) * chunk_size:])

    suffixes = list(generate_suffix(pattern_type))
    random.shuffle(suffixes) # 시간 단축을 위해 랜덤하게 섞어줌
    processes = []
    for chunk in chunks:
        p = Process(target=worker, args=(chunk, suffixes, found_flag, lock, attempt_count, start_time, pattern_type))
        p.start()
        processes.append(p)

    for p in processes:
        p.join() # 모든 프로세스가 종료될 때까지 대기
    return found_flag.value

# 프로세스에서 실행할 함수
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
