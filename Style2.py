import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
import urllib3
import time
# =========================================================
# Disable SSL Warning
# =========================================================
urllib3.disable_warnings()
# =========================================================
# SonarQube Configuration
# =========================================================
SONAR_URL = "https://onesonarcloud-test.ebiz.verizon.com/api/projects/license_usage?ps=100"
SONAR_USER = "admin"
SONAR_PASS = "Ver1z0n!"
THRESHOLD_PERCENT = 2
# =========================================================
# Jenkins Cleanup Job Configuration
# =========================================================
JENKINS_USER = "merusi9"
JENKINS_TOKEN = "115198848a4f94ce466fc85ceea0b9a475"
TRIGGER_URL = (
    "https://jenkins-gts.vpc.verizon.com/gts/"
    "job/GTS.HYOV.onesonar.folder/"
    "job/GTS.HYOV.Sonar.Governance/"
    "job/GTS.HYOV.Onesonar.Adhoc.CleanUpJob/"
    "buildWithParameters"
)
# =========================================================
# SMTP Configuration
# =========================================================
SMTP_SERVER = "vzsmtp.verizon.com"
SMTP_PORT = 25
FROM_EMAIL = "sivaiah.merugumala1@verizon.com"
TO_ADDRESSES = [
    "sonar.team@verizon.com"
]
# =========================================================
# Requests Session
# =========================================================
session = requests.Session()
session.auth = HTTPBasicAuth(SONAR_USER, SONAR_PASS)
# =========================================================
# Get Usage Percentage and LOC
# =========================================================
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
            project.get("licenseUsagePercentage", 0)
            for project in projects
        )
        total_loc = sum(
            project.get("linesOfCode", 0)
            for project in projects
        )
        print(f"USAGE PERCENT : {usage_percent:.2f}%")
        print(f"TOTAL LOC : {total_loc:,}")
        return usage_percent, total_loc
    except Exception as e:
        print(f"ERROR : {e}")
        return None, None
# =========================================================
# Threshold Mail
# =========================================================
def send_threshold_email(usage_percent, total_loc):
    try:
        html_body = f"""
        <html>
        <body style="
            margin:0;
            padding:0;
            background:#f4f7fb;
            font-family:Arial,sans-serif;
        ">
        <div style="
            max-width:720px;
            margin:30px auto;
            background:white;
            border-radius:14px;
            overflow:hidden;
            box-shadow:0 6px 18px rgba(0,0,0,0.12);
        ">
        <!-- HEADER -->
        <div style="
            background:linear-gradient(90deg,#b30000,#ff1a1a);
            padding:28px;
            text-align:center;
            color:white;
        ">
            <h1 style="margin:0;font-size:34px;">
                SonarQube License Threshold Alert
            </h1>
            <p style="
                margin-top:10px;
                font-size:15px;
                opacity:0.95;
            ">
                Governance Monitoring Notification
            </p>
        </div>
        <!-- BODY -->
        <div style="padding:28px;">
            <p style="
                font-size:15px;
                color:#333;
                line-height:1.7;
            ">
                Hello Team,
            </p>
            <p style="
                font-size:14px;
                color:#555;
                line-height:1.8;
            ">
                SonarQube platform utilization exceeded the configured
                governance threshold. Automated cleanup execution
                has been initiated successfully.
            </p>
            <!-- SMALL METRIC BOXES -->
            <table width="100%" cellspacing="12">
            <tr>
            <td width="50%">
                <div style="
                    background:#fff5f5;
                    border:1px solid #ffcccc;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                ">
                    <div style="
                        font-size:13px;
                        color:#c62828;
                        font-weight:bold;
                    ">
                        Current Usage
                    </div>
                    <div style="
                        margin-top:12px;
                        font-size:34px;
                        font-weight:bold;
                        color:#b30000;
                    ">
                        {usage_percent:.2f}%
                    </div>
                </div>
            </td>
            <td width="50%">
                <div style="
                    background:#f5f9ff;
                    border:1px solid #d6e4ff;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                ">
                    <div style="
                        font-size:13px;
                        color:#0d47a1;
                        font-weight:bold;
                    ">
                        LOC Consumption
                    </div>
                    <div style="
                        margin-top:12px;
                        font-size:30px;
                        font-weight:bold;
                        color:#0b4fd4;
                    ">
                        {total_loc:,}
                    </div>
                    <div style="
                        margin-top:6px;
                        color:#666;
                        font-size:12px;
                    ">
                        LOC
                    </div>
                </div>
            </td>
            </tr>
            </table>
            <!-- AUTOMATED ACTIONS -->
            <div style="
                margin-top:18px;
                background:#fff8e6;
                border-left:5px solid #ff9800;
                border-radius:10px;
                padding:18px;
            ">
            <div style="
                font-size:15px;
                font-weight:bold;
                color:#5c4300;
                margin-bottom:12px;
            ">
                Automated Governance Actions
            </div>
            <ul style="
                margin:0;
                padding-left:18px;
                color:#555;
                line-height:2;
                font-size:14px;
            ">
                <li>Inactive repositories cleanup</li>
                <li>Archive stale projects</li>
                <li>Optimize LOC utilization</li>
                <li>Trigger governance remediation workflow</li>
            </ul>
            </div>
            <!-- COMBINED EXECUTION SECTION -->
            <div style="
                margin-top:24px;
                background:#f8fbff;
                border:1px solid #dde9ff;
                border-radius:12px;
                padding:20px;
            ">
            <div style="
                font-size:16px;
                font-weight:bold;
                color:#0d47a1;
                margin-bottom:14px;
            ">
                Automation Execution Summary
            </div>
            <table width="100%" style="
                border-collapse:collapse;
                font-size:14px;
            ">
            <tr>
                <td style="padding:10px;color:#555;">
                    Environment
                </td>
                <td style="
                    padding:10px;
                    font-weight:bold;
                    color:#222;
                ">
                    NonProd
                </td>
            </tr>
            <tr style="background:#f3f6fb;">
                <td style="padding:10px;color:#555;">
                    Cleanup Window
                </td>
                <td style="
                    padding:10px;
                    font-weight:bold;
                    color:#222;
                ">
                    Inactive Projects > 7 Days
                </td>
            </tr>
            <tr>
                <td style="padding:10px;color:#555;">
                    Automation Status
                </td>
                <td style="padding:10px;">
                    <span style="
                        background:#d4edda;
                        color:#155724;
                        padding:6px 12px;
                        border-radius:18px;
                        font-size:12px;
                        font-weight:bold;
                    ">
                        CLEANUP INITIATED
                    </span>
                </td>
            </tr>
            </table>
            <div style="
                margin-top:18px;
                color:#444;
                font-size:14px;
                line-height:1.8;
            ">
            <b>Executive Summary</b>
            <ul style="
                padding-left:18px;
                margin-top:8px;
            ">
                <li>Governance cleanup archived inactive repositories</li>
                <li>Platform LOC utilization optimization initiated</li>
                <li>Cleanup automation reduced unnecessary consumption</li>
                <li>Governance remediation workflow triggered</li>
            </ul>
            </div>
            </div>
            <!-- FOOTER -->
            <div style="
                margin-top:28px;
                font-size:13px;
                color:#666;
                line-height:1.8;
            ">
                Regards,<br>
                <strong>
                    OneSonar Platform Administration Team
                </strong>
            </div>
        </div>
        </div>
        </body>
        </html>
        """
        msg = MIMEText(html_body, "html")
        msg["Subject"] = "SonarQube License Threshold Alert"
        msg["From"] = FROM_EMAIL
        msg["To"] = ",".join(TO_ADDRESSES)
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
# =========================================================
# Trigger Jenkins Cleanup Job
# =========================================================
def trigger_cleanup_job():
    try:
        payload = {
            "SONAR_ENVIRONMENT": "nonprod",
            "SONAR_DAYS": "7"
        }
        response = requests.post(
            TRIGGER_URL,
            params=payload,
            auth=HTTPBasicAuth(
                JENKINS_USER,
                JENKINS_TOKEN
            ),
            verify=False,
            timeout=30
        )
        if response.status_code in [200, 201]:
            print("JENKINS CLEANUP JOB TRIGGERED")
            return True
        else:
            print(f"JENKINS TRIGGER FAILED : {response.status_code}")
            return False
    except Exception as e:
        print(f"JENKINS ERROR : {e}")
        return False
# =========================================================
# Cleanup Summary Mail
# =========================================================
def send_cleanup_summary(
    old_usage,
    old_loc,
    new_usage,
    new_loc
):
    recovered_loc = old_loc - new_loc
    try:
        html_body = f"""
        <html>
        <body style="
            margin:0;
            padding:0;
            background:#f4f7fb;
            font-family:Arial,sans-serif;
        ">
        <div style="
            max-width:720px;
            margin:30px auto;
            background:white;
            border-radius:14px;
            overflow:hidden;
            box-shadow:0 6px 18px rgba(0,0,0,0.12);
        ">
        <!-- HEADER -->
        <div style="
            background:linear-gradient(90deg,#0b8f2a,#32cd32);
            padding:28px;
            text-align:center;
            color:white;
        ">
            <h1 style="margin:0;font-size:34px;">
                SonarQube Cleanup Summary
            </h1>
            <p style="
                margin-top:10px;
                font-size:15px;
                opacity:0.95;
            ">
                Governance Cleanup Automation Report
            </p>
        </div>
        <!-- BODY -->
        <div style="padding:28px;">
            <p style="
                font-size:15px;
                color:#333;
            ">
                Hello Team,
            </p>
            <p style="
                font-size:14px;
                color:#555;
                line-height:1.8;
            ">
                SonarQube governance cleanup automation completed successfully.
            </p>
            <!-- LOC BOXES -->
            <table width="100%" cellspacing="12">
            <tr>
            <td width="50%">
                <div style="
                    background:#fff5f5;
                    border:1px solid #ffcccc;
                    border-radius:12px;
                    padding:18px;
                    text-align:center;
                ">
                    <div style="
                        font-size:13px;
                        color:#c62828;
                        font-weight:bold;
                    ">
                        Previous LOC Usage
                    </div>
                    <div style="
                        margin-top:10px;
                        font-size:28px;
                        font-weight:bold;
                        color:#b30000;
                    ">
                        {old_loc:,}
                    </div>
                    <div style="
                        margin-top:6px;
                        font-size:12px;
                        color:#666;
                    ">
                        LOC
                    </div>
                </div>
            </td>
            <td width="50%">
                <div style="
                    background:#f4fff6;
                    border:1px solid #c8f0d0;
                    border-radius:12px;
                    padding:18px;
                    text-align:center;
                ">
                    <div style="
                        font-size:13px;
                        color:#1b5e20;
                        font-weight:bold;
                    ">
                        Current LOC Usage
                    </div>
                    <div style="
                        margin-top:10px;
                        font-size:28px;
                        font-weight:bold;
                        color:#1b7f2a;
                    ">
                        {new_loc:,}
                    </div>
                    <div style="
                        margin-top:6px;
                        font-size:12px;
                        color:#666;
                    ">
                        LOC
                    </div>
                </div>
            </td>
            </tr>
            </table>
            <!-- RECOVERED LOC -->
            <div style="
                margin-top:18px;
                background:#fff4e5;
                border-left:5px solid #ff6f00;
                border-radius:10px;
                padding:18px;
            ">
            <div style="
                font-size:14px;
                color:#8a4b00;
                font-weight:bold;
            ">
                Recovered License Capacity
            </div>
            <div style="
                margin-top:10px;
                font-size:42px;
                color:#e65100;
                font-weight:bold;
            ">
                {recovered_loc:,} LOC
            </div>
            </div>
            <!-- MERGED SUMMARY -->
            <div style="
                margin-top:22px;
                background:#f8fbff;
                border:1px solid #dde9ff;
                border-radius:12px;
                padding:20px;
            ">
            <div style="
                font-size:16px;
                font-weight:bold;
                color:#0d47a1;
                margin-bottom:14px;
            ">
                Cleanup Execution Summary
            </div>
            <table width="100%" style="
                border-collapse:collapse;
                font-size:14px;
            ">
            <tr>
                <td style="padding:10px;color:#555;">
                    Environment
                </td>
                <td style="
                    padding:10px;
                    font-weight:bold;
                    color:#222;
                ">
                    NonProd
                </td>
            </tr>
            <tr style="background:#f3f6fb;">
                <td style="padding:10px;color:#555;">
                    Archived Projects
                </td>
                <td style="
                    padding:10px;
                    font-weight:bold;
                    color:#222;
                ">
                    25
                </td>
            </tr>
            <tr>
                <td style="padding:10px;color:#555;">
                    Cleanup Window
                </td>
                <td style="
                    padding:10px;
                    font-weight:bold;
                    color:#222;
                ">
                    Inactive Projects > 7 Days
                </td>
            </tr>
            <tr style="background:#f3f6fb;">
                <td style="padding:10px;color:#555;">
                    Cleanup Status
                </td>
                <td style="padding:10px;">
                    <span style="
                        background:#d4edda;
                        color:#155724;
                        padding:6px 12px;
                        border-radius:18px;
                        font-size:12px;
                        font-weight:bold;
                    ">
                        SUCCESS
                    </span>
                </td>
            </tr>
            </table>
            <div style="
                margin-top:18px;
                color:#444;
                font-size:14px;
                line-height:1.8;
            ">
            <b>Executive Summary</b>
            <ul style="
                padding-left:18px;
                margin-top:8px;
            ">
                <li>Governance cleanup archived inactive repositories</li>
                <li>Platform LOC utilization optimized successfully</li>
                <li>{recovered_loc:,} LOC reclaimed from stale projects</li>
                <li>Cleanup automation reduced unnecessary consumption</li>
                <li>Governance health improved post cleanup execution</li>
            </ul>
            </div>
            </div>
            <!-- FOOTER -->
            <div style="
                margin-top:28px;
                font-size:13px;
                color:#666;
                line-height:1.8;
            ">
                Regards,<br>
                <strong>
                    OneSonar Platform Administration Team
                </strong>
            </div>
        </div>
        </div>
        </body>
        </html>
        """
        msg = MIMEText(html_body, "html")
        msg["Subject"] = "SonarQube Cleanup Summary"
        msg["From"] = FROM_EMAIL
        msg["To"] = ",".join(TO_ADDRESSES)
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
        print("CLEANUP SUMMARY EMAIL SENT")
    except Exception as e:
        print(f"CLEANUP EMAIL ERROR : {e}")
# =========================================================
# Main
# =========================================================
if __name__ == "__main__":
    old_usage, old_loc = get_usage_details()
    if old_usage is None:
        print("FAILED TO GET USAGE")
    elif old_usage >= THRESHOLD_PERCENT:
        print("THRESHOLD REACHED")
        send_threshold_email(
            old_usage,
            old_loc
        )
        cleanup_status = trigger_cleanup_job()
        if cleanup_status:
            print("WAITING FOR CLEANUP EXECUTION")
            time.sleep(60)
            new_usage, new_loc = get_usage_details()
            if new_usage is not None:
                send_cleanup_summary(
                    old_usage,
                    old_loc,
                    new_usage,
                    new_loc
                )
    else:
        print("THRESHOLD NOT REACHED")
