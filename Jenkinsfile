pipeline {
    agent any

    environment {
        // Nome do serviço no docker-compose.yml
        COMPOSE_PROJECT_NAME = 'sistema-espacial' 
        
        // Nome da ferramenta configurada no Jenkins (Manage Jenkins > Tools)
        SCANNER_HOME = tool 'sonar-scanner'
    }

    stages {
        // 1. Baixar o código
        stage('Checkout') {
            steps {
                cleanWs() // Limpa o workspace para evitar lixo antigo
                checkout scm
            }
        }

        // 2. Preparar Ambiente e Rodar Testes
        stage('Unit Tests & Coverage') {
            steps {
                script {
                    echo '🧪 Instalando dependências e rodando testes...'
                    bat """
                        python -m venv venv
                        call venv\\Scripts\\activate
                        
                        echo Instalando requirements...
                        pip install --upgrade pip
                        pip install -r requirements.txt
                                                
                        echo Rodando Pytest...
                        @REM --cov=app: calcula cobertura da pasta 'app'
                        @REM --cov-report=xml: gera o arquivo que o Sonar lê
                        pytest --cov=app --cov-report=xml:coverage.xml --junitxml=test-results.xml
                    """
                }
            }
        }

        // 3. Garantir que o SonarQube está rodando
        stage('Start SonarQube') {
            steps {
                script {
                    echo '🔌 Subindo infraestrutura de suporte...'
                    // Sobe o Sonar (definido no compose) em background
                    bat "docker-compose up -d sonarqube"
                }
            }
        }

        // 4. Análise de Código (SonarQube)
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo '🔍 Analisando qualidade...'
                    // Aguarda alguns segundos para garantir que o Sonar está respondendo
                    sleep 10
                    
                    // "sonar-server" é o nome configurado em Manage Jenkins > System
                    withSonarQubeEnv('sonar-server') {
                        // Ele vai ler automaticamente o sonar-project.properties e o coverage.xml
                        bat "${SCANNER_HOME}/bin/sonar-scanner"
                    }
                }
            }
        }

        // 5. Build da Imagem da Aplicação
        stage('Build App Image') {
            steps {
                script {
                    echo '🏗️ Construindo a aplicação via Compose...'
                    // --build garante que ele recrie a imagem com o código novo
                    bat "docker-compose build app"
                }
            }
        }

        // 6. Scan de Segurança (Trivy)
        stage('Security Scan (Trivy)') {
            steps {
                script {
                    echo '🛡️ Verificando segurança da imagem...'
                    // O nome da imagem criada pelo compose geralmente é "pasta_servico"
                    // Ajuste "sistema-espacial_app" se o nome da sua pasta for diferente
                    bat """
                        docker run --rm -v //var/run/docker.sock:/var/run/docker.sock ^
                        aquasec/trivy image --severity HIGH,CRITICAL --exit-code 0 ^
                        sistema-espacial-app
                    """
                }
            }
        }

        // 7. Deploy Final
        stage('Deploy') {
            steps {
                script {
                    echo '🚀 Atualizando a aplicação...'
                    // Sobe apenas o app (o sonar já está rodando) e recria o container
                    bat "docker-compose up -d --force-recreate app"
                }
            }
        }
    }

    post {
        always {
            echo '🏁 Pipeline finalizada.'
            // Opcional: Publicar resultados do JUnit no Jenkins
            junit 'test-results.xml'
        }
        failure {
            echo '❌ Falha no processo. Verifique os logs.'
        }
    }
}