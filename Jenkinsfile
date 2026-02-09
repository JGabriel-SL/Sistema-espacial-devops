pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'sistema-espacial'
        SCANNER_HOME = tool 'sonar-scanner'
        
        VERSION_TAG = "v1.0.${BUILD_NUMBER}"
        TAG_DEPLOY = "v1.0.${BUILD_NUMBER}"
        GIT_CREDENTIAL_ID = 'token-git' 
    }

    stages {
        stage('1. Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('2. Unit Tests (Docker Isolated)') {
            steps {
                script {
                    echo '🧪 Testando aplicação...'
                    bat """
                        docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.12 ^
                        /bin/sh -c "export PYTHONPATH=. && pip install -r requirements.txt pytest pytest-cov && pytest tests --cov=app --cov-report=xml:coverage.xml --junitxml=test-results.xml"
                    """
                }
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('3. Análise SonarQube') {
            steps {
                script {
                    echo '🔍 Analisando qualidade...'
                    withSonarQubeEnv('sonar-server') {
                        bat "${SCANNER_HOME}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('4. Trivy Scan (Repositório)') {
            steps {
                script {
                    echo '🛡️ Escaneando arquivos do código (Filesystem)...'
                    bat """
                        docker run --rm -v "%WORKSPACE%:/root/.cache/" -v "%WORKSPACE%:/src" ^
                        aquasec/trivy fs --severity HIGH,CRITICAL --exit-code 1 /src
                    """
                }
            }
        }

        stage('5. Build App Image') {
            steps {
                script {
                    echo '🏗️ Construindo Imagem...'
                    bat "docker-compose build app"
                    bat "docker tag sistema-espacial-app sistema-espacial:${VERSION_TAG}"
                }
            }
        }


        stage('6. Trivy Image Scan') {
            steps {
                echo '🛡️ Verificando vulnerabilidades na imagem...'
                bat "docker run --rm -v //var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity HIGH,CRITICAL --exit-code 1 ${APP_IMAGE}:${env.VERSION_TAG}"
            }
        }
      

        stage('7. Git Tag Release') {
            steps {
                script {
                    echo "🏷️ Criando Tag: ${VERSION_TAG}"
                    withCredentials([usernamePassword(credentialsId: GIT_CREDENTIAL_ID, usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        bat """
                            git config user.email "jenkins@ci.com"
                            git config user.name "Jenkins CI"
                            
                            git tag -a ${VERSION_TAG} -m "Release via Jenkins Build #${BUILD_NUMBER}"
                            
                            @REM Seta a URL com o Token para o push funcionar
                            git remote set-url origin https://%GIT_USER%:%GIT_PASS%@github.com/JGabriel-SL/Sistema-espacial-devops.git
                            
                            git push origin ${VERSION_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Pipeline falhou. Verifique os logs.'
        }
        success {
            echo '✅ Pipeline finalizada com Sucesso!'
        }
    }
}