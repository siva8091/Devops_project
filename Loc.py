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
TOTAL_LICENSE_LOC = 250000000
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
# Get License Usage
# ==========================================
def get_usage_details():
    try:
        response = session.get(
            SONAR_URL,
            verify=False,
            timeout=60
        )
        if response.status_code != 200:
            print(f"API FAILED : {response.status_code}")
            return None, None
        data = response.json()
        projects = data.get("projects", [])
        usage_percent = sum(
            project.get(
                "licenseUsagePercentage",
                0
            )
            for project in projects
        )
        used_loc = int(
            (usage_percent / 100)
            * TOTAL_LICENSE_LOC
        )
        print(
            f"USAGE PERCENT : {usage_percent:.2f}%"
        )
        print(
            f"USED LOC : {used_loc}"
        )
        return usage_percent, used_loc
    except Exception as e:
        print(f"ERROR : {e}")
        return None, None
# ==========================================
# Send Threshold Alert Email
# ==========================================
def send_threshold_email(
    usage_percent,
    used_loc
):
    try:
        html_body = f"""
        <html>
        <body style="
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 25px;
        ">
        <div style="
            max-width: 850px;
            margin: auto;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #dcdcdc;
            box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
        ">
            <div style="
                background-color: #c62828;
                color: white;
                padding: 25px;
                text-align: center;
            ">
                <h1>
                    SonarQube License Threshold Alert
                </h1>
            </div>
            <div style="padding: 35px;">
                <p>Hello Team,</p>
                <p>
                    SonarQube license utilization has
                    exceeded the configured governance threshold.
                </p>
                <table width="100%"
                cellpadding="12"
                cellspacing="0"
                style="
                    border-collapse: collapse;
                    margin-top: 25px;
                ">
                    <tr style="
                        background-color: #1a73e8;
                        color: white;
                    ">
                        <th align="left">Metric</th>
                        <th align="left">Value</th>
                    </tr>
                    <tr>
                        <td>
                            Current Usage
                        </td>
                        <td>
                            <strong>
                                {usage_percent:.2f}%
                            </strong>
                        </td>
                    </tr>
                    <tr style="
                        background-color: #f8f9fa;
                    ">
                        <td>
                            Current LOC Consumption
                        </td>
                        <td>
                            <strong>
                                {used_loc:,} LOC
                            </strong>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Threshold
                        </td>
                        <td>
                            <strong>
                                {THRESHOLD_PERCENT}%
                            </strong>
                        </td>
                    </tr>
                </table>
                <br>
                <p>
                    Cleanup automation has been initiated.
                </p>
                <ul>
                    <li>
                        Archive inactive projects
                    </li>
                    <li>
                        Cleanup stale repositories
                    </li>
                    <li>
                        Optimize LOC utilization
                    </li>
                </ul>
                <br>
                Regards,<br>
                <strong>
                    OneSonar Platform Team
                </strong>
            </div>
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
        print(
            "THRESHOLD EMAIL SENT"
        )
    except Exception as e:
        print(
            f"EMAIL ERROR : {e}"
        )
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
        print(
            f"JENKINS ERROR : {e}"
        )
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
# Send Cleanup Summary Email
# ==========================================
def send_post_cleanup_email(
    old_loc,
    new_loc,
    archived_projects
):
    try:
        recovered_loc = \
            old_loc - new_loc
        html_body = f"""
        <html>
        <body style="
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 25px;
        ">
        <div style="
            max-width: 850px;
            margin: auto;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #dcdcdc;
            box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
        ">
            <div style="
                background: linear-gradient(
                    90deg,
                    #0f9d58,
                    #34a853
                );
                color: white;
                padding: 24px;
                text-align: center;
            ">
                <h1>
                    SonarQube Cleanup Summary
                </h1>
                <p>
                    Governance Cleanup Automation Report
                </p>
            </div>
            <div style="padding: 35px;">
                <p>Hello Team,</p>
                <p>
                    SonarQube cleanup automation completed
                    successfully.
                </p>
                <table width="100%"
                cellpadding="12"
                cellspacing="0"
                style="
                    border-collapse: collapse;
                    margin-top: 25px;
                ">
                    <tr style="
                        background-color: #1a73e8;
                        color: white;
                    ">
                        <th align="left">
                            Metric
                        </th>
                        <th align="left">
                            Value
                        </th>
                    </tr>
                    <tr>
                        <td>
                            Environment
                        </td>
                        <td>
                            NonProd
                        </td>
                    </tr>
                    <tr style="
                        background-color: #f8f9fa;
                    ">
                        <td>
                            Previous LOC Usage
                        </td>
                        <td>
                            <strong style="
                                color: #d32f2f;
                            ">
                                {old_loc:,} LOC
                            </strong>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Current LOC Usage
                        </td>
                        <td>
                            <strong style="
                                color: #0f9d58;
                            ">
                                {new_loc:,} LOC
                            </strong>
                        </td>
                    </tr>
                    <tr style="
                        background-color: #f8f9fa;
                    ">
                        <td>
                            Recovered LOC
                        </td>
                        <td>
                            <strong style="
                                color: #ef6c00;
                            ">
                                {recovered_loc:,} LOC
                            </strong>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Archived Projects
                        </td>
                        <td>
                            {archived_projects}
                        </td>
                    </tr>
                    <tr style="
                        background-color: #f8f9fa;
                    ">
                        <td>
                            Cleanup Window
                        </td>
                        <td>
                            Inactive Projects > 7 Days
                        </td>
                    </tr>
                    <tr>
                        <td>
                            Cleanup Status
                        </td>
                        <td style="
                            color: green;
                            font-weight: bold;
                        ">
                            SUCCESS
                        </td>
                    </tr>
                </table>
                <div style="
                    margin-top: 30px;
                    background-color: #eef7ff;
                    border-left: 6px solid #1a73e8;
                    padding: 18px;
                    border-radius: 6px;
                ">
                    Cleanup automation optimized
                    SonarQube license utilization
                    by archiving stale and inactive
                    projects.
                </div>
                <br><br>
                Regards,<br>
                <strong>
                    OneSonar Platform Team
                </strong>
            </div>
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
    usage_before_percent, \
    usage_before_loc = \
        get_usage_details()
    if usage_before_percent is None:
        print(
            "FAILED TO GET USAGE"
        )
    elif usage_before_percent >= \
        THRESHOLD_PERCENT:
        print(
            "THRESHOLD REACHED"
        )
        send_threshold_email(
            usage_before_percent,
            usage_before_loc
        )
        cleanup_triggered = \
            trigger_cleanup_job()
        if cleanup_triggered:
            wait_for_cleanup()
            usage_after_percent, \
            usage_after_loc = \
                get_usage_details()
            archived_projects = 25
            send_post_cleanup_email(
                usage_before_loc,
                usage_after_loc,
                archived_projects
            )
    else:
        print(
            "THRESHOLD NOT REACHED"
        )
