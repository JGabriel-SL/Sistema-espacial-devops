pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'sistema-espacial'
        SCANNER_HOME = tool 'sonar-scanner'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        // --- ESTÁGIO DE TESTES COM DOCKER ---
        stage('Unit Tests & Coverage') {
            steps {
                script {
                    echo '🧪 Testando com Docker Manual (Fix PYTHONPATH)...'
                    
                    // Mudança: Adicionamos 'export PYTHONPATH=.'
                    // Isso diz ao Python: "Procure módulos na pasta atual (/app) também"
                    
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

        stage('Preparar Infra (Sonar)') {
            steps {
                script {
                    echo '🔌 Iniciando SonarQube...'
                    bat "docker-compose up -d sonarqube"
                    sleep 15
                }
            }
        }

        stage('Análise SonarQube') {
            steps {
                script {
                    echo '🔍 Analisando qualidade...'
                    withSonarQubeEnv('sonar-server') {
                        bat "${SCANNER_HOME}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Build & Deploy App') {
            steps {
                script {
                    echo '🚀 Construindo e Subindo a Aplicação...'
                    bat "docker-compose build app"
                    bat "docker-compose up -d app"
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Falha no pipeline.'
        }
    }
}