curl -k -u "svc-user:YourPassword" \
"https://jenkins.company.com/crumbIssuer/api/json"


curl -k -X POST \
-u "svc-user:YourPassword" \
-H "Content-Type: application/json" \
-H "Jenkins-Crumb: abc123xyz" \
-d '{"newTokenName":"automation-token"}' \
"https://jenkins.company.com/user/svc-user/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken"

curl -k -u svc-user https://jenkins.company.com/crumbIssuer/api/json
