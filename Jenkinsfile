pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "pulsecheck-backend:latest"
        FRONTEND_IMAGE = "pulsecheck-frontend:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('backend') {
                    sh 'docker build -t pulsecheck-backend:latest .'
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                dir('frontend') {
                    sh 'docker build -t pulsecheck-frontend:latest .'
                }
            }
        }

        stage('Load Images into Minikube') {
            steps {
                sh 'minikube image load pulsecheck-backend:latest'
                sh 'minikube image load pulsecheck-frontend:latest'
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get pods'
                sh 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }

        failure {
            echo 'Deployment Failed!'
        }
    }
}
