pipeline {
    agent any

    environment {
        PROJECT_DIR = "liver_disease_prediction_project"
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo "Repo is automatically cloned by Jenkins"
            }
        }

        stage('Install Dependencies') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip install --upgrade pip'
                    sh '.pip install -r requirements.txt'
                }
            }
        }

        stage('Train Model') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh './venv/bin/python train.py'
                }
            }
        }

        stage('Run App') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh 'nohup ./venv/bin/python run.py &'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Build and Run Successful!'
        }
        failure {
            echo '❌ Build Failed. Check logs.'
        }
    }
}

