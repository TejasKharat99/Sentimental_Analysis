pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: text-emotion-pipeline
spec:
  containers:
  - name: python
    image: python:3.9-slim
    command: ['cat']
    tty: true
    volumeMounts:
    - name: workspace-volume
      mountPath: /home/jenkins/agent

  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli
    command: ['cat']
    tty: true

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ['cat']
    tty: true
    securityContext:
      runAsUser: 0
      readOnlyRootFilesystem: false
    volumeMounts:
    - name: kubeconfig-secret
      mountPath: /kube/config
      subPath: kubeconfig

  - name: dind
    image: docker:dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""

  volumes:
  - name: kubeconfig-secret
    secret:
      secretName: kubeconfig-secret
  - name: workspace-volume
    emptyDir: {}
'''
        }
    }

    environment {
        DOCKER_IMAGE = "emotion-2401100"
        DOCKER_REGISTRY = "your-registry-address" // Update with your registry
        K8S_NAMESPACE = "emotion-2401100"
        SONAR_HOST_URL = "http://localhost:9000"
    }

    stages {
        stage('Checkout') {
            steps {
                container('python') {
                    checkout scm
                }
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
                    sh '''
                    echo 'Running tests...'
                    # Uncomment when you have tests
                    # python -m pytest tests/
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=Emotion_2401100 \
                            -Dsonar.projectName=Emotion_2401100 \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=sqp_9600400ad1bc19cfe53d8530d54bbf8ae4067ab4 \
                            -Dsonar.sources=. \
                            -Dsonar.python.version=3.9
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh '''
                    docker build -t ${DOCKER_IMAGE}:latest .
                    docker tag ${DOCKER_IMAGE}:latest ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Push to Registry') {
            steps {
                container('dind') {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker-registry-creds',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {
                        sh '''
                        echo $DOCKER_PASS | docker login ${DOCKER_REGISTRY} -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    script {
                        dir('k8s') {
                            sh """
                            kubectl get namespace ${K8S_NAMESPACE} || kubectl create namespace ${K8S_NAMESPACE}
                            kubectl apply -f deployment.yaml -n ${K8S_NAMESPACE}
                            kubectl apply -f service.yaml -n ${K8S_NAMESPACE}
                            
                            # Force rollout to pick up new image
                            kubectl rollout restart deployment/text-emotion-deployment -n ${K8S_NAMESPACE}
                            
                            # Wait for rollout to complete
                            kubectl rollout status deployment/text-emotion-deployment -n ${K8S_NAMESPACE}
                            """
                        }
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                container('kubectl') {
                    sh """
                    echo "========== PODS =========="
                    kubectl get pods -n ${K8S_NAMESPACE}

                    echo "========== SERVICES =========="
                    kubectl get svc -n ${K8S_NAMESPACE}

                    echo "========== DEPLOYMENT STATUS =========="
                    kubectl get deployment -n ${K8S_NAMESPACE}

                    echo "========== LATEST POD LOGS =========="
                    kubectl logs -l app=text-emotion -n ${K8S_NAMESPACE} --tail=50 || true
                    """
                }
            }
        }
    }

    post {
        always {
            container('kubectl') {
                echo 'Pipeline completed'
            }
        }
    }
}
