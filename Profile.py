import requests
import openpyxl

# === Configuration ===
SONAR_URL = "https://your-sonarqube-url"  # Update with your SonarQube URL
USERNAME = "your-username"                # Update with your SonarQube username or token
PASSWORD = "your-password"                # Update with your SonarQube password or leave empty if using a token
OUTPUT_FILE = "custom_sonar_profiles.xlsx"

# === Excel Setup ===
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Custom Profiles"
ws.append([
    "Profile Name", "Language", "Active Rule Count",
    "Associated Projects", "Is Inherited", "Parent Profile"
])

# === Function: Get All Quality Profiles ===
def get_custom_profiles():
    url = f"{SONAR_URL}/api/qualityprofiles/search"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    response.raise_for_status()
    profiles = response.json().get("profiles", [])
    
    # Filter out default or built-in profiles
    custom_profiles = [
        p for p in profiles
        if not p.get("isDefault", False) and not p.get("isBuiltIn", False)
    ]
    return custom_profiles

# === Main Function ===
def main():
    profiles = get_custom_profiles()

    for profile in profiles:
        name = profile.get("name", "")
        language = profile.get("language", "")
        active_rule_count = profile.get("activeRuleCount", 0)
        project_count = profile.get("projectCount", 0)
        is_inherited = profile.get("isInherited", False)
        parent_name = profile.get("parentName", "") if is_inherited else "N/A"

        ws.append([
            name,
            language,
            active_rule_count,
            project_count,
            "Yes" if is_inherited else "No",
            parent_name
        ])
    
    wb.save(OUTPUT_FILE)
    print(f"Data successfully saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
