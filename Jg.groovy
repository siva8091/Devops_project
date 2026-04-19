pipeline {
    agent { label 'west' }

    parameters {
        choice(
            name: 'INPUT_FILE',
            choices: [
                'jenkins_vbg1_jobs.txt',
                'jenkins_vbg2_jobs.txt',
                'jenkins_vbg3_jobs.txt',
                'jenkins_vcg1_jobs.txt',
                'jenkins_vcg2_jobs.txt',
                'jenkins_vcg3_jobs.txt',
                'jenkins_vcg4_jobs.txt',
                'jenkins_vcg5_jobs.txt',
                'jenkins_vcg6_jobs.txt'
            ],
            description: 'Select controller input file'
        )

        string(
            name: 'JENKINS_BASE',
            defaultValue: 'https://jenkins-url',
            description: 'Jenkins Base URL'
        )

        password(
            name: 'J_TOKEN',
            defaultValue: '',
            description: 'Jenkins API Token'
        )
    }

    stages {
        stage('Run Script') {
            steps {
                script {
                    // Full input file path
                    def inputPath = "scripts/jenkins_prod/${params.INPUT_FILE}"

                    // Extract controller name (vcg1, vbg2, etc.)
                    def controller = params.INPUT_FILE
                        .replace("jenkins_", "")
                        .replace("_jobs.txt", "")

                    // Final output file
                    def outputFile = "${controller}.csv"

                    sh """
                    echo "Workspace: \$WORKSPACE"
                    echo "Input File: ${inputPath}"
                    echo "Controller: ${controller}"
                    echo "Output File: ${outputFile}"

                    ls -R

                    python3 scripts/jenkins_prod/gitlab_svc_removal.py \
                      --input "${inputPath}" \
                      --output "${outputFile}" \
                      --jenkins_base "${params.JENKINS_BASE}" \
                      --token "${params.J_TOKEN}"
                    """
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: "*.csv", onlyIfSuccessful: true
        }
    }
}
