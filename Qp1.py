import requests
import json

# SonarQube server details
SONARQUBE_URL = 'http://your-sonarqube-server.com'
SONARQUBE_TOKEN = 'your_sonarqube_token'

# Quality profiles to set as default for respective languages
quality_profiles = {
    'java': 'Sonar way',
    'javascript': 'Sonar way',
    'python': 'Sonar way',
    # Add more languages and profiles as needed
}

def set_default_quality_profile(language, profile_name):
    endpoint = f'{SONARQUBE_URL}/api/qualityprofiles/set_default'
    params = {
        'language': language,
        'qualityProfile': profile_name
    }
    response = requests.post(endpoint, params=params, auth=(SONARQUBE_TOKEN, ''))
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
