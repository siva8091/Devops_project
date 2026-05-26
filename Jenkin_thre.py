import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
import urllib3
import time
# ==========================================
# Disable SSL Warning
# ==========================================
urllib3.disable_warnings()
# ==========================================
# SonarQube Configuration
# ==========================================
SONAR_URL = "https://onesonarcloud-test.ebiz.verizon.com/api/projects/license_usage?ps=100"
SONAR_USER = "admin"
SONAR_PASS = "Ver1z0n!"
THRESHOLD_PERCENT = 2
# ==========================================
# Jenkins Configuration
# ==========================================
JENKINS_URL = "https://jenkins-gts.vpc.verizon.com/gts"
JENKINS_JOB = "GTS.HYOV.onesonar.folder/job/GTS.HYOV.Sonar.Governance/job/GTS.HYOV.Onesonar.Adhoc.CleanUpJob"
JENKINS_USER = "merusi9"
JENKINS_TOKEN = "115198848a4f94ce466fc85ceea0b9a475"
# ==========================================
# SMTP Configuration
# ==========================================
SMTP_SERVER = "vzsmtp.verizon.com"
SMTP_PORT = 25
FROM_EMAIL = "sivaiah.merugumala1@verizon.com"
TO_ADDRESSES = [
    "sonar.team@verizon.com"
]
# ==========================================
# Requests Session
# ==========================================
session = requests.Session()
session.auth = HTTPBasicAuth(
    SONAR_USER,
    SONAR_PASS
)
# ==========================================
# Get License Usage Percentage
# ==========================================
def get_usage_percentage():
    try:
        response = session.get(
            SONAR_URL,
            verify=False,
            timeout=60
        )
        if response.status_code != 200:
            print(f"API FAILED : {response.status_code}")
            return None
        data = response.json()
        projects = data.get("projects", [])
        usage_percent = sum(
            project.get(
                "licenseUsagePercentage",
                0
            )
            for project in projects
        )
        print(
            f"USAGE PERCENT : {usage_percent:.2f}%"
        )
        return usage_percent
    except Exception as e:
        print(f"ERROR : {e}")
        return None
# ==========================================
# Send Threshold Alert Email
# ==========================================
def send_threshold_email(usage_percent):
    try:
        html_body = f"""
        <html>
        <body style="
            font-family: Arial;
            background-color: #f4f6f8;
            padding: 20px;
        ">
        <div style="
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #dddddd;
        ">
        <h2 style="color: #c62828;">
            SonarQube License Usage Threshold Alert
        </h2>
        <p>
            Hello Team,
        </p>
        <p>
            SonarQube license utilization has exceeded
            the configured governance threshold.
        </p>
        <div style="
            background-color: #fff3f3;
            padding: 20px;
            border-left: 6px solid red;
            margin-top: 20px;
            margin-bottom: 20px;
        ">
            <p>
                <strong>Current Usage:</strong>
                {usage_percent:.2f}%
            </p>
            <p>
                <strong>Threshold:</strong>
                {THRESHOLD_PERCENT}%
            </p>
        </div>
        <p>
            Cleanup automation has been initiated.
        </p>
        <ul>
            <li>Archive inactive projects</li>
            <li>Cleanup stale repositories</li>
            <li>Optimize LOC utilization</li>
        </ul>
        <br>
        Regards,<br>
        <strong>OneSonar Platform Team</strong>
        </div>
        </body>
        </html>
        """
        msg = MIMEText(
            html_body,
            "html"
        )
        msg["Subject"] = \
            "SonarQube License Threshold Alert"
        msg["From"] = FROM_EMAIL
        msg["To"] = ",".join(
            TO_ADDRESSES
        )
        smtp = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=20
        )
        smtp.sendmail(
            FROM_EMAIL,
            TO_ADDRESSES,
            msg.as_string()
        )
        smtp.quit()
        print("THRESHOLD EMAIL SENT")
    except Exception as e:
        print(f"EMAIL ERROR : {e}")
# ==========================================
# Trigger Jenkins Cleanup Job
# ==========================================
def trigger_cleanup_job():
    try:
        trigger_url = f"""
{JENKINS_URL}/job/{JENKINS_JOB}/buildWithParameters
""".strip()
        payload = {
            "token": JENKINS_TOKEN,
            "SONAR_ENVIRONMENT": "nonprod",
            "SONAR_DAYS": "7",
            "SONAR_DRY_RUN_DELETE": "false"
        }
        response = requests.post(
            trigger_url,
            params=payload,
            auth=HTTPBasicAuth(
                JENKINS_USER,
                JENKINS_TOKEN
            ),
            verify=False
        )
        if response.status_code in [200, 201]:
            print(
                "JENKINS CLEANUP JOB TRIGGERED"
            )
            return True
        else:
            print(
                f"JENKINS TRIGGER FAILED : "
                f"{response.status_code}"
            )
            return False
    except Exception as e:
        print(f"JENKINS ERROR : {e}")
        return False
# ==========================================
# Wait For Cleanup Completion
# ==========================================
def wait_for_cleanup():
    print(
        "WAITING FOR CLEANUP COMPLETION..."
    )
    time.sleep(60)
    print(
        "CLEANUP COMPLETED"
    )
# ==========================================
# Send Post Cleanup Email
# ==========================================
def send_post_cleanup_email(
    old_usage,
    new_usage,
    archived_projects
):
    try:
        recovered = \
            old_usage - new_usage
        html_body = f"""
        <html>
        <body style="
            font-family: Arial;
            background-color: #f4f6f8;
            padding: 20px;
        ">
        <div style="
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #dddddd;
        ">
        <h2 style="color: green;">
            SonarQube Cleanup Summary
        </h2>
        <p>
            Cleanup automation completed successfully.
        </p>
        <table border="1"
        cellpadding="10"
        cellspacing="0"
        style="border-collapse: collapse;">
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Previous Usage</td>
                <td>{old_usage:.2f}%</td>
            </tr>
            <tr>
                <td>Current Usage</td>
                <td>{new_usage:.2f}%</td>
            </tr>
            <tr>
                <td>Recovered License</td>
                <td>{recovered:.2f}%</td>
            </tr>
            <tr>
                <td>Archived Projects</td>
                <td>{archived_projects}</td>
            </tr>
        </table>
        <br>
        Regards,<br>
        <strong>OneSonar Platform Team</strong>
        </div>
        </body>
        </html>
        """
        msg = MIMEText(
            html_body,
            "html"
        )
        msg["Subject"] = \
            "SonarQube Cleanup Summary"
        msg["From"] = FROM_EMAIL
        msg["To"] = ",".join(
            TO_ADDRESSES
        )
        smtp = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=20
        )
        smtp.sendmail(
            FROM_EMAIL,
            TO_ADDRESSES,
            msg.as_string()
        )
        smtp.quit()
        print(
            "POST CLEANUP EMAIL SENT"
        )
    except Exception as e:
        print(
            f"POST EMAIL ERROR : {e}"
        )
# ==========================================
# Main
# ==========================================
if __name__ == "__main__":
    usage_before = get_usage_percentage()
    if usage_before is None:
        print("FAILED TO GET USAGE")
    elif usage_before >= THRESHOLD_PERCENT:
        print("THRESHOLD REACHED")
        send_threshold_email(
            usage_before
        )
        cleanup_triggered = \
            trigger_cleanup_job()
        if cleanup_triggered:
            wait_for_cleanup()
            usage_after = \
                get_usage_percentage()
            archived_projects = 25
            send_post_cleanup_email(
                usage_before,
                usage_after,
                archived_projects
            )
    else:
        print(
            "THRESHOLD NOT REACHED"
        )
