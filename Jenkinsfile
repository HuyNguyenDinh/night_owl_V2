pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }

    stages {
        stage('Print python version') {
            steps {
                sh 'python -V'
            }
        }
    }
}
