pipeline {
    agent { label 'west' }

    parameters {
        choice(
            name: 'INPUT_FILE',
            choices: [
                'jenkins_vbg1_jobs.txt',
                'jenkins_vbg2_jobs.txt',
                'jenkins_vbg3_jobs.txt'
            ],
            description: 'Select controller input file'
        )

        string(name: 'OUTPUT_CSV', defaultValue: 'output.csv')
    }

    stages {
        stage('Run Script') {
            steps {
                sh '''
                echo "Selected input file: $INPUT_FILE"
                echo "Workspace: $WORKSPACE"

                python3 scripts/jenkins_prod/gitlab_svc_removal.py \
                  --input "scripts/jenkins_prod/$INPUT_FILE" \
                  --output "$OUTPUT_CSV"
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: "${OUTPUT_CSV}", onlyIfSuccessful: true
        }
    }
}
