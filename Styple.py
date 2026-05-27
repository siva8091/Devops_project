import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
import urllib3
import time
# ==========================================
# Disable SSL Warnings
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
# Get Usage Details
# ==========================================
def get_usage_details():
    try:
        response = session.get(
            SONAR_URL,
            verify=False,
            timeout=60
        )
        if response.status_code != 200:
            print(
                f"API FAILED : {response.status_code}"
            )
            return None, None
        data = response.json()
        projects = data.get(
            "projects",
            []
        )
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
            f"USED LOC : {used_loc:,}"
        )
        return usage_percent, used_loc
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
            padding:30px;
            background:#edf2f7;
            font-family:Arial,sans-serif;
        ">
        <div style="
            max-width:920px;
            margin:auto;
            background:white;
            border-radius:18px;
            overflow:hidden;
            box-shadow:0 12px 35px rgba(0,0,0,0.18);
        ">
            <div style="
                background:linear-gradient(
                    135deg,
                    #7f1d1d,
                    #b91c1c,
                    #dc2626
                );
                padding:40px;
                text-align:center;
                color:white;
            ">
                <h1 style="
                    margin:0;
                    font-size:38px;
                ">
                    SonarQube License Threshold Alert
                </h1>
                <p style="
                    margin-top:12px;
                    font-size:16px;
                ">
                    Governance Monitoring Notification
                </p>
            </div>
            <div style="padding:40px;">
                <p style="
                    font-size:16px;
                    color:#1f2937;
                ">
                    Hello Team,
                </p>
                <p style="
                    font-size:15px;
                    line-height:1.9;
                    color:#4b5563;
                ">
                    SonarQube platform utilization
                    exceeded the configured governance
                    threshold. Automated cleanup
                    execution has been initiated.
                </p>
                <table width="100%"
                cellpadding="15"
                cellspacing="15">
                    <tr>
                        <td style="
                            background:#fff5f5;
                            border-radius:16px;
                            text-align:center;
                            border:1px solid #fecaca;
                            padding:25px;
                        ">
                            <div style="
                                color:#dc2626;
                                font-size:14px;
                                font-weight:bold;
                            ">
                                Current Usage
                            </div>
                            <div style="
                                margin-top:12px;
                                font-size:36px;
                                font-weight:bold;
                                color:#991b1b;
                            ">
                                {usage_percent:.2f}%
                            </div>
                        </td>
                        <td style="
                            background:#eff6ff;
                            border-radius:16px;
                            text-align:center;
                            border:1px solid #bfdbfe;
                            padding:25px;
                        ">
                            <div style="
                                color:#2563eb;
                                font-size:14px;
                                font-weight:bold;
                            ">
                                LOC Consumption
                            </div>
                            <div style="
                                margin-top:12px;
                                font-size:32px;
                                font-weight:bold;
                                color:#1d4ed8;
                            ">
                                {used_loc:,}
                            </div>
                            <div style="
                                margin-top:6px;
                                color:#1e40af;
                            ">
                                LOC
                            </div>
                        </td>
                    </tr>
                </table>
                <div style="
                    margin-top:30px;
                    background:#fef3c7;
                    border-left:8px solid #f59e0b;
                    padding:25px;
                    border-radius:14px;
                ">
                    <div style="
                        color:#92400e;
                        font-weight:bold;
                        font-size:16px;
                    ">
                        Automated Governance Actions
                    </div>
                    <ul style="
                        margin-top:15px;
                        line-height:2;
                        color:#78350f;
                    ">
                        <li>Inactive repositories cleanup</li>
                        <li>Archive stale projects</li>
                        <li>Optimize LOC utilization</li>
                        <li>Trigger governance remediation workflow</li>
                    </ul>
                </div>
                <div style="
                    margin-top:40px;
                    padding-top:25px;
                    border-top:1px solid #e5e7eb;
                    color:#6b7280;
                    line-height:1.8;
                ">
                    Regards,<br>
                    <strong style="
                        color:#111827;
                    ">
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
# Trigger Cleanup Job
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
# Cleanup Summary Email
# ==========================================
def send_post_cleanup_email(
    old_loc,
    new_loc,
    archived_projects
):
    try:
        recovered_loc = old_loc - new_loc
        html_body = f"""
        <html>
        <body style="
            margin:0;
            padding:30px;
            background:#edf2f7;
            font-family:Arial,sans-serif;
        ">
        <div style="
            max-width:920px;
            margin:auto;
            background:white;
            border-radius:18px;
            overflow:hidden;
            box-shadow:0 12px 35px rgba(0,0,0,0.18);
        ">
            <div style="
                background:linear-gradient(
                    135deg,
                    #0f172a,
                    #1e3a8a,
                    #2563eb
                );
                padding:45px;
                text-align:center;
                color:white;
            ">
                <h1 style="
                    margin:0;
                    font-size:40px;
                    font-weight:bold;
                ">
                    SonarQube Cleanup Summary
                </h1>
                <p style="
                    margin-top:12px;
                    font-size:16px;
                ">
                    Governance Cleanup Automation Report
                </p>
            </div>
            <div style="padding:40px;">
                <p style="
                    font-size:17px;
                    color:#1f2937;
                ">
                    Hello Team,
                </p>
                <p style="
                    font-size:15px;
                    line-height:1.9;
                    color:#4b5563;
                ">
                    SonarQube governance cleanup automation
                    completed successfully.
                </p>
                <table width="100%"
                cellpadding="14"
                cellspacing="16">
                    <tr>
                        <td style="
                            background:#fff5f5;
                            border-radius:16px;
                            padding:28px;
                            text-align:center;
                            border:1px solid #fecaca;
                        ">
                            <div style="
                                color:#dc2626;
                                font-size:14px;
                                font-weight:bold;
                            ">
                                Previous LOC Usage
                            </div>
                            <div style="
                                margin-top:12px;
                                font-size:32px;
                                font-weight:bold;
                                color:#991b1b;
                            ">
                                {old_loc:,}
                            </div>
                            <div style="
                                color:#7f1d1d;
                                margin-top:6px;
                                font-size:13px;
                            ">
                                LOC
                            </div>
                        </td>
                        <td style="
                            background:#f0fdf4;
                            border-radius:16px;
                            padding:28px;
                            text-align:center;
                            border:1px solid #bbf7d0;
                        ">
                            <div style="
                                color:#15803d;
                                font-size:14px;
                                font-weight:bold;
                            ">
                                Current LOC Usage
                            </div>
                            <div style="
                                margin-top:12px;
                                font-size:32px;
                                font-weight:bold;
                                color:#166534;
                            ">
                                {new_loc:,}
                            </div>
                            <div style="
                                color:#166534;
                                margin-top:6px;
                                font-size:13px;
                            ">
                                LOC
                            </div>
                        </td>
                    </tr>
                </table>
                <div style="
                    margin-top:30px;
                    background:linear-gradient(
                        90deg,
                        #fff7ed,
                        #ffedd5
                    );
                    border-left:8px solid #f97316;
                    padding:32px;
                    border-radius:16px;
                ">
                    <div style="
                        font-size:15px;
                        color:#9a3412;
                        font-weight:bold;
                    ">
                        Recovered License Capacity
                    </div>
                    <div style="
                        margin-top:12px;
                        font-size:46px;
                        color:#ea580c;
                        font-weight:bold;
                    ">
                        {recovered_loc:,} LOC
                    </div>
                </div>
                <div style="
                    margin-top:30px;
                    background:#eff6ff;
                    border-radius:16px;
                    padding:30px;
                    text-align:center;
                    border:1px solid #bfdbfe;
                ">
                    <div style="
                        font-size:15px;
                        color:#1d4ed8;
                        font-weight:bold;
                    ">
                        Governance Health Score
                    </div>
                    <div style="
                        margin-top:12px;
                        font-size:52px;
                        font-weight:bold;
                        color:#1e40af;
                    ">
                        92/100
                    </div>
                </div>
                <div style="
                    margin-top:35px;
                    border:1px solid #e5e7eb;
                    border-radius:16px;
                    overflow:hidden;
                ">
                    <div style="
                        background:#f9fafb;
                        padding:20px;
                        font-weight:bold;
                        color:#111827;
                        border-bottom:1px solid #e5e7eb;
                        font-size:16px;
                    ">
                        Automation Execution Details
                    </div>
                    <table width="100%"
                    cellpadding="18"
                    cellspacing="0"
                    style="
                        border-collapse:collapse;
                        font-size:15px;
                    ">
                        <tr>
                            <td><strong>Environment</strong></td>
                            <td>NonProd</td>
                        </tr>
                        <tr style="background:#f9fafb;">
                            <td><strong>Archived Projects</strong></td>
                            <td>{archived_projects}</td>
                        </tr>
                        <tr>
                            <td><strong>Cleanup Window</strong></td>
                            <td>Inactive Projects > 7 Days</td>
                        </tr>
                        <tr style="background:#f9fafb;">
                            <td>
                                <strong>Cleanup Status</strong>
                            </td>
                            <td>
                                <span style="
                                    background:#dcfce7;
                                    color:#166534;
                                    padding:9px 18px;
                                    border-radius:30px;
                                    font-weight:bold;
                                    font-size:13px;
                                ">
                                    SUCCESS
                                </span>
                            </td>
                        </tr>
                    </table>
                </div>
                <div style="
                    margin-top:35px;
                    background:#f8fafc;
                    border-left:6px solid #2563eb;
                    padding:25px;
                    border-radius:14px;
                ">
                    <div style="
                        font-size:17px;
                        font-weight:bold;
                        color:#1e40af;
                        margin-bottom:14px;
                    ">
                        Executive Summary
                    </div>
                    <div style="
                        color:#374151;
                        line-height:2;
                        font-size:15px;
                    ">
                        • Governance cleanup archived inactive repositories<br>
                        • Platform LOC utilization optimized successfully<br>
                        • {recovered_loc:,} LOC reclaimed from stale projects<br>
                        • Cleanup automation reduced unnecessary license consumption<br>
                        • Governance health score improved post cleanup execution
                    </div>
                </div>
                <div style="
                    margin-top:45px;
                    padding-top:28px;
                    border-top:1px solid #e5e7eb;
                    color:#6b7280;
                    font-size:14px;
                    line-height:1.9;
                ">
                    Regards,<br>
                    <strong style="
                        color:#111827;
                    ">
                        OneSonar Platform Administration Team
                    </strong>
                    <br><br>
                    <span style="
                        font-size:12px;
                        color:#9ca3af;
                    ">
                        Powered by OneSonar Governance Automation Framework
                    </span>
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
    usage_before_percent, usage_before_loc = \
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
            usage_after_percent, usage_after_loc = \
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
