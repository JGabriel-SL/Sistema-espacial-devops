pipeline {
    agent any

    environment {
        // Nome da imagem e do container
        IMAGE_NAME = 'sistema-espacial'
        CONTAINER_NAME = 'meu-espacial'
        PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                // Se você usar Git, o Jenkins fará o git pull aqui automaticamente
                // Se for pasta local, ele usa o workspace atual
                checkout scm
            }
        }

        stage('Build da Imagem') {
            steps {
                script {
                    echo '🏗️ Construindo a imagem Docker...'
                    // 'bat' é o comando para Windows. Se fosse Linux seria 'sh'
                    bat "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Limpeza (Stop/Remove)') {
            steps {
                script {
                    echo '🧹 Parando container antigo se existir...'
                    // O try/catch evita que o build falhe se não tiver nada rodando
                    try {
                        bat "docker stop ${CONTAINER_NAME}"
                        bat "docker rm ${CONTAINER_NAME}"
                    } catch (Exception e) {
                        echo 'Nenhum container anterior encontrado. Seguindo...'
                    }
                }
            }
        }

        stage('Deploy (Run)') {
            steps {
                script {
                    echo '🚀 Subindo nova versão...'
                    // Atenção ao volume do banco de dados!
                    // %WORKSPACE% é a variável onde o Jenkins baixou seu código
                    bat """
                        docker run -d -p ${PORT}:5000 ^
                        -v "%WORKSPACE%/instance/database.db:/app/instance/database.db" ^
                        --name ${CONTAINER_NAME} ^
                        ${IMAGE_NAME}
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Sucesso! Aplicação rodando em http://localhost:5000'
        }
        failure {
            echo '❌ Falha no deploy.'
        }
    }
}