import requests
from github_token import GITHUB_TOKEN
import matplotlib.pyplot as plt

headers = {'Authorization': f'token {GITHUB_TOKEN}'}

def count_lines_in_file(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text.count('\n')

def couint_lines_in_repo(directory_url):
    total_lines = 0
    response = requests.get(directory_url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file['type'] == 'file' and file['name'].endswith('.py') or file['type'] == 'file' and file['name'].endswith('.cpp') or file['type'] == 'file' and file['name'].endswith('.js') or file['type'] == 'file' and file['name'].endswith('.jsx'):
                file_url = file['download_url']
                total_lines += count_lines_in_file(file_url) 
            elif file['type'] == 'dir': 
                subdirectory_url = file['url']
                total_lines += couint_lines_in_repo(subdirectory_url)
    return total_lines

def main():
    
    data_count = {}
    data_proportional = {}

    personal_repos = ['nate-adkins/myactuator','nate-adkins/controls']
    
    urc_repos_names = ["pico_interface_pkg", 
                       "ros2-rover-gui", 
                       "CameraManager", 
                       "isaac_reinforcement_standalone",
                       "autonomy_2025",
                       "rf-modem-stuff",
                       "Ros2CommsSettings2025",
                    ]
    
    urc_repos =  [f'wvu-urc/' + name for name in urc_repos_names ]

    repos = personal_repos + urc_repos
    for repo in repos:
        url = f'https://api.github.com/repos/{repo}/contents/'
        total_lines = couint_lines_in_repo(url)
        
        name = repo.split('/')[1]
        print(f"Total lines in {name}: {total_lines}")
        
        data_count[name] = total_lines
        
    total = sum(data_count.values())

    for key, val in data_count.items():
        data_proportional[key] = val / total
    print(data_proportional)
    print(total)
    
    plt.figure(figsize=(10, 6))
    plt.pie(data_count.values(), labels=data_count.keys(), autopct=lambda p: f'{int(p * total / 100)} ({p:.1f}%)')
    plt.title(f'Lines of Code Written in Last Month ({total} lines total)')
    plt.show()

if __name__ == '__main__':
    main()