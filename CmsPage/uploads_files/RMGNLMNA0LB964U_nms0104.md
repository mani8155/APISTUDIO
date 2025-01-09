# Jenkins Pipeline Script: Download File and Backup

This Jenkins Pipeline script performs two main stages: downloading a file from an API and executing a backup process.

```groovy
pipeline {
    agent {
        node {
            label 'node_label_name'
        }
    }

    environment {
        WORKSPACE_DIR = 'dowloaded file path'
    }

    stages {
        stage('Download File from API') {
            steps {
                script {
                    try {
                        def url = "your_api_url"
                        def response = httpRequest(url: url, httpMode: 'GET', validResponseCodes: '200')
                        writeFile file: "${env.WORKSPACE_DIR}/file_name.py", text: response.content
                        echo "File downloaded and written successfully."
                    } catch (Exception e) {
                        echo "Failed to download and write the file: ${e.getMessage()}"
                        error("Stopping the pipeline due to failure.")
                    }
                }
            }
        }

        stage('Backup') {
            steps {
                script {
                    try {
                        // Change to the directory containing the virtual environment
                        dir('/apistudio/Nmsapi') {
                            // Activate the virtual environment
                            sh 'source venv/bin/activate'
                            
                            // Run the Python script
                            sh 'python3 /project_path/file_name.py'
                            
                            // Deactivate the virtual environment
                            sh 'deactivate'
                        }
                    } catch (Exception e) {
                        echo "Failed during backup process: ${e.getMessage()}"
                        error("Stopping the pipeline due to failure.")
                    }
                }
            }
        }
    }
}
