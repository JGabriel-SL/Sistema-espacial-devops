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
            // Removemos o 'agent { docker }' para não dar erro de caminho
            steps {
                script {
                    echo '🧪 Testando com Docker Manual (Fix Windows)...'
                    
                    // O PULO DO GATO:
                    // 1. -v "%WORKSPACE%:/app" -> Mapeia a pasta do Jenkins (Windows) para /app (Linux)
                    // 2. -w /app -> Diz pro container trabalhar dentro de /app (caminho Linux válido!)
                    // 3. /bin/sh -c "..." -> Roda os comandos Linux lá dentro
                    
                    bat """
                        docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.12 ^
                        /bin/sh -c "pip install -r requirements.txt pytest pytest-cov && pytest tests --cov=app --cov-report=xml:coverage.xml --junitxml=test-results.xml"
                    """
                }
            }
            post {
                always {
                    // O allowEmptyResults evita que o pipeline trave se o teste falhar
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