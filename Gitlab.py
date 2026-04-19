pipeline {
    agent { label 'my-agent' }

    parameters {
        file(name: 'INPUT_FILE', description: 'Upload input file')
        string(name: 'OUTPUT_CSV', defaultValue: 'output.csv')
        string(name: 'J_TOKEN', defaultValue: '')
        string(name: 'JENKINS_BASE', defaultValue: '')
    }

    stages {
        stage('Run Script') {
            steps {
                sh '''
                python3 Jenkins_Gitlab_scanner.py \
                  --input "$INPUT_FILE" \
                  --output "$OUTPUT_CSV"
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: '**/${OUTPUT_CSV}', onlyIfSuccessful: true
        }
    }
}
