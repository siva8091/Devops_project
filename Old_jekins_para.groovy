sh '''
echo "Workspace: $WORKSPACE"
echo "Input file actual path: $INPUT_FILE"
ls -l

python3 jenkins/scripts/jenkins_prod/gitlab_svc_removal.py \
  --input "$INPUT_FILE" \
  --output "$OUTPUT_CSV"
'''


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
                    // Dynamic output file name
                    def outputFile = "${params.INPUT_FILE}.csv"

                    sh """
                    echo "Workspace: \$WORKSPACE"
                    echo "Selected input file: ${params.INPUT_FILE}"
                    echo "Output file: ${outputFile}"

                    ls -R

                    python3 scripts/jenkins_prod/gitlab_svc_removal.py \
                      --input "scripts/jenkins_prod/${params.INPUT_FILE}" \
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
            script {
                archiveArtifacts artifacts: "${params.INPUT_FILE}.csv", onlyIfSuccessful: true
            }
        }
    }
}
