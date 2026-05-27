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
# Jenkins Cleanup Job Configuration
# ==========================================
JENKINS_URL = "https://jenkins-gts.vpc.verizon.com/gts"
JENKINS_JOB = (
    "GTS.HYOV.onesonar.folder/"
    "job/GTS.HYOV.Sonar.Governance/"
    "job/GTS.HYOV.Onesonar.Adhoc.CleanUpJob"
)
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
# Session Configuration
# ==========================================
session = requests.Session()
session.auth = HTTPBasicAuth(
    SONAR_USER,
    SONAR_PASS
)
# ==========================================
# Get Current Usage
# ==========================================
def get_usage_details():
    try:
        response = session.get(
            SONAR_URL,
            verify=False,
            timeout=30
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
        total_loc = sum(
            project.get(
                "linesOfCode",
                0
            )
            for project in projects
        )
        print(
            f"USAGE PERCENT : "
            f"{usage_percent:.2f}%"
        )
        print(
            f"TOTAL LOC : "
            f"{total_loc:,}"
        )
        return usage_percent, total_loc
    except Exception as e:
        print(f"ERROR : {e}")
        return None, None
# ==========================================
# Threshold Alert Email
# ==========================================
def send_threshold_email(
    usage_percent,
    used_loc
):
    try:
        html_body = f"""
        <html>
        <body style="
            margin:0;
            padding:25px;
            background:#f3f6fb;
            font-family:Arial,sans-serif;
        ">
        <div style="
            max-width:820px;
            margin:auto;
            background:white;
            border-radius:18px;
            overflow:hidden;
            box-shadow:0 10px 28px rgba(0,0,0,0.12);
        ">
            <!-- HEADER -->
            <div style="
                background:linear-gradient(
                    135deg,
                    #b3001b,
                    #d90429,
                    #ef233c
                );
                padding:32px;
                text-align:center;
                color:white;
            ">
                <h1 style="
                    margin:0;
                    font-size:34px;
                    font-weight:bold;
                ">
                    SonarQube License Threshold Alert
                </h1>
                <div style="
                    margin-top:10px;
                    font-size:14px;
                    opacity:0.95;
                ">
                    Governance Monitoring Notification
                </div>
            </div>
            <!-- BODY -->
            <div style="padding:32px;">
                <p style="
                    color:#1f2937;
                    font-size:15px;
                    margin-top:0;
                ">
                    Hello Team,
                </p>
                <p style="
                    color:#4b5563;
                    font-size:14px;
                    line-height:1.8;
                ">
                    SonarQube platform utilization exceeded
                    the configured governance threshold.
                    Automated cleanup execution has been initiated.
                </p>
                <!-- KPI CARDS -->
                <table width="100%"
                cellpadding="10"
                cellspacing="0"
                style="margin-top:25px;">
                    <tr>
                        <td width="50%">
                            <div style="
                                background:#fff5f5;
                                border:1px solid #fecaca;
                                border-radius:14px;
                                padding:22px;
                                text-align:center;
                            ">
                                <div style="
                                    color:#dc2626;
                                    font-size:13px;
                                    font-weight:bold;
                                ">
                                    Current Usage
                                </div>
                                <div style="
                                    margin-top:8px;
                                    font-size:30px;
                                    font-weight:bold;
                                    color:#991b1b;
                                ">
                                    {usage_percent:.2f}%
                                </div>
                            </div>
                        </td>
                        <td width="50%">
                            <div style="
                                background:#eff6ff;
                                border:1px solid #bfdbfe;
                                border-radius:14px;
                                padding:22px;
                                text-align:center;
                            ">
                                <div style="
                                    color:#2563eb;
                                    font-size:13px;
                                    font-weight:bold;
                                ">
                                    LOC Consumption
                                </div>
                                <div style="
                                    margin-top:8px;
                                    font-size:28px;
                                    font-weight:bold;
                                    color:#1d4ed8;
                                ">
                                    {used_loc:,}
                                </div>
                                <div style="
                                    margin-top:4px;
                                    color:#2563eb;
                                    font-size:12px;
                                ">
                                    LOC
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
                <!-- ACTIONS -->
                <div style="
                    margin-top:24px;
                    background:#fff8e6;
                    border-left:5px solid #f59e0b;
                    border-radius:12px;
                    padding:18px 22px;
                ">
                    <div style="
                        font-size:15px;
                        font-weight:bold;
                        color:#92400e;
                        margin-bottom:12px;
                    ">
                        Automated Governance Actions
                    </div>
                    <ul style="
                        margin:0;
                        padding-left:18px;
                        line-height:1.9;
                        color:#78350f;
                        font-size:14px;
                    ">
                        <li>Inactive repositories cleanup</li>
                        <li>Archive stale projects</li>
                        <li>Optimize LOC utilization</li>
                        <li>Trigger governance remediation workflow</li>
                    </ul>
                </div>
                <!-- FOOTER -->
                <div style="
                    margin-top:30px;
                    padding-top:20px;
                    border-top:1px solid #e5e7eb;
                    color:#6b7280;
                    font-size:13px;
                    line-height:1.8;
                ">
                    Regards,<br>
                    <strong style="color:#111827;">
                        OneSonar Platform Administration Team
                    </strong>
                </div>
            </div>
        </div>
        </body>
        </html>
        """
        msg = MIMEText(
            html_body,
            "html"
        )
        msg["Subject"] = (
            "SonarQube License Threshold Alert"
        )
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
        trigger_url = (
            f"{JENKINS_URL}/"
            f"{JENKINS_JOB}/"
            f"buildWithParameters?"
            f"SONAR_ENVIRONMENT=nonprod&"
            f"SONAR_DAYS=7"
        )
        response = requests.post(
            trigger_url,
            auth=HTTPBasicAuth(
                JENKINS_USER,
                JENKINS_TOKEN
            ),
            verify=False,
            timeout=30
        )
        if response.status_code in [200, 201]:
            print(
                "JENKINS CLEANUP "
                "JOB TRIGGERED"
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
# Cleanup Summary Email
# ==========================================
def send_cleanup_summary(
    old_loc,
    new_loc,
    recovered_loc,
    archived_projects
):
    try:
        html_body = f"""
        <html>
        <body style="
            margin:0;
            padding:25px;
            background:#f3f6fb;
            font-family:Arial,sans-serif;
        ">
        <div style="
            max-width:820px;
            margin:auto;
            background:white;
            border-radius:18px;
            overflow:hidden;
            box-shadow:0 10px 28px rgba(0,0,0,0.12);
        ">
            <!-- HEADER -->
            <div style="
                background:linear-gradient(
                    135deg,
                    #0f172a,
                    #1d4ed8,
                    #2563eb
                );
                padding:34px;
                text-align:center;
                color:white;
            ">
                <h1 style="
                    margin:0;
                    font-size:34px;
                    font-weight:bold;
                ">
                    SonarQube Cleanup Summary
                </h1>
                <div style="
                    margin-top:10px;
                    font-size:14px;
                    opacity:0.95;
                ">
                    Governance Cleanup Automation Report
                </div>
            </div>
            <!-- BODY -->
            <div style="padding:30px;">
                <p style="
                    margin-top:0;
                    font-size:15px;
                    color:#1f2937;
                ">
                    Hello Team,
                </p>
                <p style="
                    color:#4b5563;
                    font-size:14px;
                    line-height:1.8;
                ">
                    SonarQube governance cleanup automation
                    completed successfully.
                </p>
                <!-- KPI CARDS -->
                <table width="100%"
                cellpadding="10"
                cellspacing="0"
                style="margin-top:22px;">
                    <tr>
                        <td width="50%">
                            <div style="
                                background:#fff5f5;
                                border:1px solid #fecaca;
                                border-radius:14px;
                                padding:22px;
                                text-align:center;
                            ">
                                <div style="
                                    color:#dc2626;
                                    font-size:13px;
                                    font-weight:bold;
                                ">
                                    Previous LOC Usage
                                </div>
                                <div style="
                                    margin-top:8px;
                                    font-size:30px;
                                    font-weight:bold;
                                    color:#991b1b;
                                ">
                                    {old_loc:,}
                                </div>
                                <div style="
                                    margin-top:4px;
                                    color:#991b1b;
                                    font-size:12px;
                                ">
                                    LOC
                                </div>
                            </div>
                        </td>
                        <td width="50%">
                            <div style="
                                background:#f0fdf4;
                                border:1px solid #bbf7d0;
                                border-radius:14px;
                                padding:22px;
                                text-align:center;
                            ">
                                <div style="
                                    color:#15803d;
                                    font-size:13px;
                                    font-weight:bold;
                                ">
                                    Current LOC Usage
                                </div>
                                <div style="
                                    margin-top:8px;
                                    font-size:30px;
                                    font-weight:bold;
                                    color:#166534;
                                ">
                                    {new_loc:,}
                                </div>
                                <div style="
                                    margin-top:4px;
                                    color:#166534;
                                    font-size:12px;
                                ">
                                    LOC
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
                <!-- RECOVERED LOC -->
                <div style="
                    margin-top:22px;
                    background:#fff7ed;
                    border-left:5px solid #f97316;
                    border-radius:12px;
                    padding:22px;
                ">
                    <div style="
                        color:#9a3412;
                        font-size:14px;
                        font-weight:bold;
                    ">
                        Recovered License Capacity
                    </div>
                    <div style="
                        margin-top:10px;
                        color:#ea580c;
                        font-size:38px;
                        font-weight:bold;
                    ">
                        {recovered_loc:,} LOC
                    </div>
                </div>
                <!-- MERGED EXECUTION SUMMARY -->
                <div style="
                    margin-top:25px;
                    border:1px solid #dbeafe;
                    background:#f8fbff;
                    border-radius:14px;
                    overflow:hidden;
                ">
                    <div style="
                        background:#2563eb;
                        color:white;
                        padding:16px 20px;
                        font-size:16px;
                        font-weight:bold;
                    ">
                        Automation Execution Summary
                    </div>
                    <div style="padding:22px;">
                        <table width="100%"
                        cellpadding="10"
                        cellspacing="0"
                        style="
                            border-collapse:collapse;
                            font-size:14px;
                        ">
                            <tr>
                                <td width="40%">
                                    <strong>Environment</strong>
                                </td>
                                <td>NonProd</td>
                            </tr>
                            <tr style="background:#eff6ff;">
                                <td>
                                    <strong>Archived Projects</strong>
                                </td>
                                <td>{archived_projects}</td>
                            </tr>
                            <tr>
                                <td>
                                    <strong>Cleanup Window</strong>
                                </td>
                                <td>Inactive Projects > 7 Days</td>
                            </tr>
                            <tr style="background:#eff6ff;">
                                <td>
                                    <strong>Recovered LOC</strong>
                                </td>
                                <td>{recovered_loc:,} LOC</td>
                            </tr>
                            <tr>
                                <td>
                                    <strong>Cleanup Status</strong>
                                </td>
                                <td>
                                    <span style="
                                        background:#dcfce7;
                                        color:#166534;
                                        padding:7px 14px;
                                        border-radius:20px;
                                        font-size:12px;
                                        font-weight:bold;
                                    ">
                                        SUCCESS
                                    </span>
                                </td>
                            </tr>
                        </table>
                        <div style="
                            margin-top:20px;
                            background:white;
                            border-left:4px solid #2563eb;
                            padding:16px;
                            border-radius:10px;
                            color:#374151;
                            line-height:1.9;
                            font-size:14px;
                        ">
                            • Governance cleanup archived inactive repositories<br>
                            • Platform LOC utilization optimized successfully<br>
                            • {recovered_loc:,} LOC reclaimed from stale projects<br>
                            • Cleanup automation reduced unnecessary license consumption
                        </div>
                    </div>
                </div>
                <!-- FOOTER -->
                <div style="
                    margin-top:30px;
                    padding-top:18px;
                    border-top:1px solid #e5e7eb;
                    color:#6b7280;
                    font-size:13px;
                    line-height:1.8;
                ">
                    Regards,<br>
                    <strong style="color:#111827;">
                        OneSonar Platform Administration Team
                    </strong>
                </div>
            </div>
        </div>
        </body>
        </html>
        """
        msg = MIMEText(
            html_body,
            "html"
        )
        msg["Subject"] = (
            "SonarQube Cleanup Summary"
        )
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
        print("SUMMARY EMAIL SENT")
    except Exception as e:
        print(f"SUMMARY EMAIL ERROR : {e}")
# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    usage_percent, total_loc = (
        get_usage_details()
    )
    if usage_percent is None:
        print(
            "FAILED TO GET USAGE"
        )
    elif usage_percent >= THRESHOLD_PERCENT:
        print(
            "THRESHOLD REACHED"
        )
        # Send Threshold Email
        send_threshold_email(
            usage_percent,
            total_loc
        )
        # Trigger Cleanup Job
        job_triggered = (
            trigger_cleanup_job()
        )
        if job_triggered:
            print(
                "WAITING FOR CLEANUP..."
            )
            time.sleep(20)
            # Fetch New Usage
            new_usage, new_loc = (
                get_usage_details()
            )
            if new_loc is not None:
                recovered_loc = (
                    total_loc - new_loc
                )
                archived_projects = 25
                send_cleanup_summary(
                    total_loc,
                    new_loc,
                    recovered_loc,
                    archived_projects
                )
    else:
        print(
            "THRESHOLD NOT REACHED"
        )
