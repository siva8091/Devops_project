import requests

# SonarQube server and authentication details
SONARQUBE_URL = 'http://your-sonarqube-server'
API_TOKEN = 'your_api_token'

# Headers for authentication
headers = {
    'Authorization': f'Basic {API_TOKEN}',
    'Content-Type': 'application/json'
}

def get_all_projects():
    """Get the list of all projects in SonarQube."""
    url = f"{SONARQUBE_URL}/api/projects/search"
    projects = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={'p': page})
        response.raise_for_status()
        data = response.json()
        projects.extend(data.get('components', []))
        if page >= data.get('paging', {}).get('total', 0):
            break
        page += 1
    return projects

def get_project_admins(project_key):
    """Get the list of project administrators for a given project."""
    url = f"{SONARQUBE_URL}/api/permissions/users?projectKey={project_key}&permission=admin"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    admins = response.json().get('users', [])
    return [admin['login'] for admin in admins]

def get_quality_profile(project_key):
    """Get the quality profile details for a given project."""
    url = f"{SONARQUBE_URL}/api/qualityprofiles/search?project={project_key}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    profiles = response.json().get('profiles', [])
    return profiles

def grant_quality_profile_edit_permission(profile_key, user_login):
    """Grant edit permission for a quality profile to a user."""
    url = f"{SONARQUBE_URL}/api/qualityprofiles/add_user"
    payload = {
        'profileKey': profile_key,
        'login': user_login,
        'permission': 'profileadmin'
    }
    response = requests.post(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()

def main():
    # Get all projects
    projects = get_all_projects()

    for project in projects:
        project_key = project['key']
        project_name = project['name']
        print(f"Processing project: {project_name} (Key: {project_key})")

        # Get project admins
        admins = get_project_admins(project_key)
        print(f"  Project Admins: {admins}")

        # Get project quality profiles
        profiles = get_quality_profile(project_key)
        if not profiles:
            print(f"  No quality profiles found for project: {project_name}")
            continue
        
        for profile in profiles:
            profile_key = profile['key']
            profile_name = profile['name']
            print(f"  Quality Profile: {profile_name} (Key: {profile_key})")

            # Grant edit permission to each admin
            for admin in admins:
                try:
                    result = grant_quality_profile_edit_permission(profile_key, admin)
                    print(f"    Granted edit permission for profile '{profile_name}' to admin '{admin}'")
                except requests.exceptions.RequestException as e:
                    print(f"    Error granting permission to '{admin}' for profile '{profile_name}': {e}")

if __name__ == "__main__":
    main()
