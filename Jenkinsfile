pipeline {
  agent none
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        bat 'python3 ChangeResolution.py'
      }
    }
  }
}