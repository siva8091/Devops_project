import requests
import json

try:
    # --------------------------------------------------
    # CCP Configuration (From your screenshot)
    # --------------------------------------------------
    CCP_URL = "https://cyberarkccp.verizon.com/AIMWebService/api/Accounts"

    params = {
        "AppID": "CCP_IOUV_N_GTS",
        "Safe": "APP_IOUV_N_GTS_VDSI",
        "UserName": "SVC-jenkinsplatform",
        "PlatformID": "VZ_RPA_SSHKeys"
    }

    CERT_FILE = "/jn-home-gts/cyberark/jenkins-cyberark_ebiz_verizon_com.crt"
    KEY_FILE = "/jn-home-gts/cyberark/jenkins-cyberark.ebiz.verizon.com_private.key"
    CA_FILE = "/jn-home-gts/cyberark/TrustedRoot.crt"

    # --------------------------------------------------
    # Step 1 – Retrieve Secret from CCP
    # --------------------------------------------------
    response = requests.get(
        CCP_URL,
        params=params,
        cert=(CERT_FILE, KEY_FILE),
        verify=CA_FILE
    )

    if response.status_code != 200:
        raise Exception("Failed to retrieve credential from CCP")

    secret_data = response.json()

    # CCP returns password in:
    api_secret = secret_data["Content"]

    # --------------------------------------------------
    # Step 2 – Use Secret Securely (DO NOT PRINT)
    # --------------------------------------------------
    jenkins_url = "https://jenkins-gts.ebiz.verizon.com/gts/scriptText"

    jenkins_response = requests.post(
        jenkins_url,
        auth=("SVC-jenkinsplatform", api_secret),
        data={'script': "println InetAddress.localHost.hostAddress"},
        verify=False
    )

    print("Jenkins call successful")
    print(jenkins_response.text)

except Exception as e:
    print("Error:", str(e))
