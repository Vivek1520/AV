
import os
import hashlib

# Set of known malware hashes
malware_hashes = {
    "d41d8cd98f00b204e9800998ecf8427e",  # example hash
    "098f6bcd4621d373cade4e832627b4f6",  # example hash
    "1dcca23355272056f04fe8bf20edfce0",  # example hash
    # Add more hashes as needed
}

# Folders and drives to scan
paths_to_scan = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    "C:\\", "D:\\", "E:\\", "F:\\"
]


# Step 1: List all files in the specified paths (only top-level files)
def list_files(paths):
    files_list = []
    for path in paths:
        if os.path.exists(path):
            # Check only top-level files in the specified directory
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):  # Check if it's a file
                    print(f"Found file: {file_path}")
                    files_list.append(file_path)
        else:
            print(f"[WARNING] Path does not exist: {path}")
    return files_list


# Step 2: Calculate and print hashes for each file
def calculate_and_print_hashes(files_list):
    print("\nCalculating and printing hash for each file:")
    file_hashes = {}
    for file_path in files_list:
        try:
            hash_func = hashlib.md5()  # MD5 hash algorithm
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            file_hash = hash_func.hexdigest()
            print(f"Hash for {file_path}: {file_hash}")
            file_hashes[file_path] = file_hash
        except (PermissionError, OSError) as e:
            print(f"[WARNING] Could not access {file_path}: {e}")
    return file_hashes


# Step 3: Scan files to check if any are malware
def scan_for_malware(file_hashes, malware_hashes):
    print("\nScanning for malware:")
    infected_files = []
    for file_path, file_hash in file_hashes.items():
        if file_hash in malware_hashes:
            print(f"[ALERT] Malware detected: {file_path}")
            infected_files.append(file_path)
    return infected_files


# Main function
if __name__ == "__main__":
    # Run steps in sequence
    files_list = list_files(paths_to_scan)  # Step 1: List files in specified paths
    file_hashes = calculate_and_print_hashes(files_list)  # Step 2: Calculate hashes
    infected_files = scan_for_malware(file_hashes, malware_hashes)  # Step 3: Scan for malware

    # Final result
    if infected_files:
        print("\nScan complete. Malware found in the following files:")
        for infected_file in infected_files:
            print(f"- {infected_file}")
    else:
        print("\nScan complete. No malware detected.")
