pipeline {
    agent {
        kubernetes {
            // Use a simple pod template with Python
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: python
    image: python:3.9-slim
    command: ['sleep']
    args: ['infinity']
    volumeMounts:
      - name: workspace-volume
        mountPath: /home/jenkins/agent
  volumes:
    - name: workspace-volume
      emptyDir: {}
"""
        }
    }
    
    environment {
        DOCKER_IMAGE = 'text-emotion-detection'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                container('python') {
                    sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                container('python') {
                    echo 'Running tests...'
                    // Uncomment when you have tests
                    // sh 'python -m pytest tests/'
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                container('python') {
                    sh '''
                    # Install required tools
                    apt-get update && apt-get install -y wget unzip
                    
                    # Download and extract sonar-scanner
                    wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
                    unzip sonar-scanner-cli-4.8.0.2856-linux.zip
                    
                    # Run sonar-scanner (will use sonar-project.properties for configuration)
                    ./sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner
                    '''
                }
            }
        }
        
        stage('Build & Push') {
            steps {
                script {
                    echo 'Docker build would happen here'
                    // docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Kubernetes deployment would happen here'
                    // sh 'kubectl apply -f k8s/'
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            deleteDir()
        }
    }
}
