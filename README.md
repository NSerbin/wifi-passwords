# Wi-Fi Password Retrieval Script
This script retrieves stored Wi-Fi passwords for all available Wi-Fi profiles on your system using nmcli commands in a Linux environment. It uses concurrent processing to fetch passwords for multiple profiles in parallel, making the retrieval process faster.

## Prerequisites

- Ensure you are running a Linux distribution.

- The nmcli command-line tool must be installed and accessible. nmcli is typically included with NetworkManager, which is common on many Linux distributions.

## How It Works

### Retrieve Wi-Fi Profiles:

- The script uses nmcli to fetch a list of all available Wi-Fi profiles on the system.

- Fetch Passwords:
    - For each Wi-Fi profile, the script attempts to retrieve the stored Wi-Fi password using nmcli.
    - It handles errors gracefully by returning "No stored password" if a password cannot be retrieved.

- Concurrent Execution:
    - The script employs ThreadPoolExecutor to fetch passwords for multiple profiles concurrently, improving efficiency.

### Output:

The script prints out each Wi-Fi profile along with its corresponding password (or an error message if the password is not available).

### Usage

To use this script, follow these steps:

### Clone or Download:

Save the script to your local machine.

### Run the Script:

- Open a terminal.

- Navigate to the directory where the script is saved.

- Execute the script using Python:
```bash
python wifi_password_retrieval.py
```

### View Results:

- The script will output a list of Wi-Fi profiles and their corresponding passwords.

```python
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Function to get Wi-Fi password for a given profile
def get_wifi_password(profile):
    try:
        result = subprocess.check_output(
            ['nmcli', '-s', '-g', '802-11-wireless-security.psk', 'connection', 'show', profile],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return (profile, result)
    except subprocess.CalledProcessError:
        return (profile, "No stored password")

# Get the list of Wi-Fi profiles
network = subprocess.check_output(
    ['nmcli', '-t', '-f', 'NAME', 'connection', 'show'],
    stderr=subprocess.DEVNULL
).decode('utf-8').split('\n')
profiles = [i for i in network if i]  # Remove empty strings

# Create a thread pool to fetch passwords in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(get_wifi_password, profiles)

# Print the results
for profile, password in results:
    print("{:<30}|  {:<}".format(profile, password))
```    

### Notes

- The script assumes that nmcli is installed and properly configured on your system.

- Running the script may require appropriate permissions to access network settings.

- The script has been designed for educational purposes; use it responsibly.