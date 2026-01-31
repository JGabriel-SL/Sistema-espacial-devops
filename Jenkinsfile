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
            agent {
                docker {
                    // Usa a imagem oficial do Python
                    image 'python:3.12'
                    // Garante que o container use o mesmo workspace do Jenkins
                    reuseNode true
                }
            }
            steps {
                script {
                    echo '🧪 Rodando testes DENTRO do container Python...'
                    
                    // Como estamos dentro do container, é Linux/Unix.
                    // Não usamos 'bat', usamos 'sh'.
                    // Não precisamos de venv, pois o container é descartável.
                    
                    sh 'pip install -r requirements.txt pytest pytest-cov'
                    
                    // Roda os testes e gera os arquivos no workspace compartilhado
                    sh 'pytest tests --cov=app --cov-report=xml:coverage.xml --junitxml=test-results.xml'
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