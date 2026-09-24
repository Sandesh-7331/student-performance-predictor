pipeline {

    agent any

    environment {

        DOCKER_IMAGE = "sandesh6/student-performance-predictor"

    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }


        stage('Install Dependencies') {

            steps {

                sh '''
                python3 -m venv .jenkins-venv
                . .jenkins-venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''

            }

        }


        stage('Run Tests') {

            steps {

                sh '''
                . .jenkins-venv/bin/activate
                python -m unittest test_app.py
                '''

            }

        }


        stage('Build Docker Image') {

            steps {

                sh '''
                docker build \
                -t $DOCKER_IMAGE:$BUILD_NUMBER \
                -t $DOCKER_IMAGE:latest \
                .
                '''

            }

        }


        stage('Docker Login') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {

                    sh '''
                    echo "$DOCKER_TOKEN" | \
                    docker login \
                    -u "$DOCKER_USER" \
                    --password-stdin
                    '''

                }

            }

        }


        stage('Push Docker Image') {

            steps {

                sh '''
                docker push $DOCKER_IMAGE:$BUILD_NUMBER
                docker push $DOCKER_IMAGE:latest
                '''

            }

        }


        stage('Deploy to Kubernetes') {

            steps {

                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                kubectl set image \
                deployment/student-performance-app \
                student-performance=$DOCKER_IMAGE:$BUILD_NUMBER

                kubectl rollout status \
                deployment/student-performance-app \
                --timeout=120s
                '''

            }

        }


        stage('Verify Deployment') {

            steps {

                sh '''
                kubectl get pods
                kubectl get services
                '''

            }

        }

    }


    post {

        success {

            echo "CI/CD PIPELINE SUCCESSFUL!"

        }

        failure {

            echo "CI/CD PIPELINE FAILED!"

        }

        always {

            sh 'rm -rf .jenkins-venv || true'
            sh 'docker logout || true'

        }

    }

}
