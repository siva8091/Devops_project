import requests

# SonarQube server details
SONARQUBE_URL = 'http://your-sonarqube-server.com'
SONARQUBE_USERNAME = 'your_username'
SONARQUBE_PASSWORD = 'your_password'

# Quality profiles to set as default for respective languages
quality_profiles = {
    'java': 'Sonar way',
    'javascript': 'Sonar way',
    'python': 'Sonar way',
    # Add more languages and profiles as needed
}

def is_default_quality_profile(language, profile_name):
    endpoint = f'{SONARQUBE_URL}/api/qualityprofiles/search'
    params = {
        'language': language
    }
    response = requests.get(endpoint, params=params, auth=(SONARQUBE_USERNAME, SONARQUBE_PASSWORD))
    
    if response.status_code == 200:
        profiles = response.json().get('profiles', [])
        for profile in profiles:
            if profile['name'] == profile_name and profile['isDefault']:
                return True
    else:
        print(f"Failed to retrieve quality profiles for {language}: {response.status_code} {response.text}")
    return False

def set_default_quality_profile(language, profile_name):
    if is_default_quality_profile(language, profile_name):
        print(f"{profile_name} is already set as the default profile for {language}. Skipping...")
        return
    
    endpoint = f'{SONARQUBE_URL}/api/qualityprofiles/set_default'
    params = {
        'language': language,
        'qualityProfile': profile_name
    }
    response = requests.post(endpoint, params=params, auth=(SONARQUBE_USERNAME, SONARQUBE_PASSWORD))
    
    print(f'Request URL: {response.url}')
    print(f'Request Params: {params}')
    
    if response.status_code == 204:
        print(f'Successfully set {profile_name} as the default profile for {language}.')
    else:
        print(f'Failed to set default profile for {language}: {response.status_code} {response.text}')

def main():
    for language, profile in quality_profiles.items():
        set_default_quality_profile(language, profile)

if __name__ == "__main__":
    main()
