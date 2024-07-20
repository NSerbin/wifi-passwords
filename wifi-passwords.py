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
