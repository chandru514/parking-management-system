pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_USER = 'chandru514'
        IMAGE_NAME = 'parking-system'
        REG_NO = '24MIS0514'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out source code for Reg No: ${REG_NO} - Parking Management System"
                checkout scm
            }
        }

        stage('Lint & Unit Check') {
            steps {
                echo 'Running python syntax & integrity checks...'
                bat '''
                    python -m py_compile app.py v1/app.py v2/app.py v3/app.py
                '''
            }
        }

        stage('Build Docker Images (v1, v2, v3)') {
            steps {
                echo 'Building Docker images tagged v1, v2, and v3...'
                bat """
                    docker build -t %DOCKER_USER%/%IMAGE_NAME%:v1 -f v1/Dockerfile .
                    docker build -t %DOCKER_USER%/%IMAGE_NAME%:v2 -f v2/Dockerfile .
                    docker build -t %DOCKER_USER%/%IMAGE_NAME%:v3 -f v3/Dockerfile .
                """
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo 'Authenticating and pushing images to DockerHub...'
                bat """
                    echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin
                    docker push %DOCKER_USER%/%IMAGE_NAME%:v1
                    docker push %DOCKER_USER%/%IMAGE_NAME%:v2
                    docker push %DOCKER_USER%/%IMAGE_NAME%:v3
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying v1, v2, and v3 deployments and services to Kubernetes cluster...'
                bat """
                    kubectl apply -f k8s/v1-deployment.yaml
                    kubectl apply -f k8s/v2-deployment.yaml
                    kubectl apply -f k8s/v3-deployment.yaml
                """
            }
        }

        stage('Verify Rollout') {
            steps {
                echo 'Verifying rollout status on Kubernetes...'
                bat """
                    kubectl rollout status deployment/parking-system-v1 --timeout=60s
                    kubectl rollout status deployment/parking-system-v2 --timeout=60s
                    kubectl rollout status deployment/parking-system-v3 --timeout=60s
                    kubectl get pods,svc -l app=parking-system
                """
            }
        }
    }

    post {
        success {
            echo "Successfully built, containerized, and deployed all 3 versions for ${REG_NO}!"
        }
        failure {
            echo "Pipeline failed. Check stage logs for troubleshooting."
        }
    }
}
