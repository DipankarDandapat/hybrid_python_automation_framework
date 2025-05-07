pipeline {
    agent any
    environment {
        PYTHON_VERSION = "3.10"
        python_location = 'C:\\Program Files\\Python313\\python.exe'
        VENV_DIR = "venv"
        BS_CREDENTIALS_ID = "browserstack-credentials"
        LT_CREDENTIALS_ID = "lambdatest-credentials"
    }
    parameters {
        string(name: 'GIT_REPO_URL', defaultValue: 'https://github.com/DipankarDandapat/hybrid_python_automation_framework.git', description: 'Git repository URL for the automation framework')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to checkout')
        choice(name: 'ENVIRONMENT', choices: ["staging", "prod"], description: 'Select the target environment')
        choice(name: 'TEST_TYPE', choices: ["api", "ui", "all"], description: 'Select the type of tests to run')
        choice(name: 'TEST_CASE_TYPE', choices: ["Positive", "Negative", "Semantic","Smoke","Regression"], description: 'Select the test type of tests case to run')
        choice(name: 'UI_LOCATION', choices: ["none", "local", "cloud"], description: 'Run UI tests locally or on cloud (Select \'none\' for API tests only)')
        choice(name: 'LOCAL_BROWSER', choices: ["chrome", "firefox", "edge"], description: 'Select the browser for local UI execution')
        booleanParam(name: 'HEADLESS_MODE', defaultValue: false, description: 'Run the local browser in headless mode?')
        choice(name: 'CLOUD_PROVIDER', choices: ["browserstack", "lambdatest"], description: 'Select the cloud testing provider')
        string(name: 'CLOUD_PLATFORM', defaultValue: 'Windows 10', description: 'Specify the OS platform for cloud testing')
        string(name: 'CLOUD_BROWSER', defaultValue: 'chrome', description: 'Specify the browser name for cloud testing')
        string(name: 'CLOUD_BROWSER_VERSION', defaultValue: 'latest', description: 'Specify the browser version for cloud testing')
    }
    // triggers {
    //     parameterizedCron('''
    //         // H/5 * * * * %ENVIRONMENT=staging;TEST_TYPE=api;TEST_CASE_TYPE=Positive
    //         //H/5 * * * * %ENVIRONMENT=staging;TEST_TYPE=ui;UI_LOCATION=local;LOCAL_BROWSER=chrome
    //         H/5 * * * * %ENVIRONMENT=staging;TEST_TYPE=ui;UI_LOCATION=cloud;CLOUD_PROVIDER=browserstack;CLOUD_BROWSER=firefox
    //     ''')
    // }
    
    
    stages {
        
        stage('Cleanup Workspace') {
            steps {
                // Clean workspace before build
                cleanWs()
                echo "Cleaned up workspace."
            }
        }
        stage('Checkout Code from GIT') {
            steps {
                script {
                    echo "Checking out code from ${params.GIT_REPO_URL} branch ${params.GIT_BRANCH}"
                }
                checkout scmGit(
                    branches: [[name: "*/${params.GIT_BRANCH}"]],
                    extensions: [],
                    userRemoteConfigs: [[url: "${params.GIT_REPO_URL}"]]
                )
                echo 'Check out git successfully!'
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    echo "Setting up Python ${env.PYTHON_VERSION} virtual environment"
                    bat "\"${python_location}\" -m venv ${env.VENV_DIR}"
                    echo "Installing dependencies from requirements.txt"
                    bat "${env.VENV_DIR}\\Scripts\\activate && python -m pip install --upgrade pip && pip install -r requirements.txt"
                    echo "Installed dependencies ...."
                }
            }
        }
        stage('Execute Pytest Tests') {
            steps {
                script {
                    echo "Constructing pytest command based on parameters..."
                    
                    // Base pytest command with environment activation
                    def pytestCommand = "${env.VENV_DIR}\\Scripts\\activate.bat && pytest tests"
                    
                    // Add common options
                    //pytestCommand += " --verbose"
                    pytestCommand += " --environment=${params.ENVIRONMENT}"
                    
                    if (params.TEST_TYPE = 'api') {
                        pytestCommand += " --test-type=${params.TEST_TYPE}"
                        pytestCommand += " -m=${params.TEST_CASE_TYPE}"
                        echo "Running only ${params.TEST_TYPE} tests."
                        
                    } else {
                        echo "Running all tests (API and UI)."
                    }
                    // Add test type filtering marker if not running 'all'
                    if (params.TEST_TYPE != 'all') {
                        pytestCommand += " --test-type=${params.TEST_TYPE}"
                        // pytestCommand += " -m=${params.TEST_CASE_TYPE}"

                        
                        echo "Running only ${params.TEST_TYPE} tests."
                    } else {
                        echo "Running all tests (API and UI)."
                    }
                    
                    // --- Handle UI Test Parameters ---
                    def runUiTests = (params.TEST_TYPE == 'ui' || params.TEST_TYPE == 'all')
                    def uiLocation = params.UI_LOCATION
                    def executedInWithCredentials = false // Flag to track if sh command ran inside withCredentials
                    
                    if (runUiTests) {
                        if (uiLocation == 'local') {
                            echo "Configuring for uiLocation in local platform"
                            echo "Configuring for Local UI tests on ${params.LOCAL_BROWSER}"
                            pytestCommand += " --browser=${params.LOCAL_BROWSER}"
                            if (params.HEADLESS_MODE) {
                                pytestCommand += " --headless"
                                echo "Headless mode enabled."
                            }
                        } else if (uiLocation == 'cloud') {
                            echo "Configuring for Cloud UI tests on ${params.CLOUD_PROVIDER}"
                            pytestCommand += " --remote" // Flag to indicate cloud execution
                            pytestCommand += " --browser=${params.CLOUD_BROWSER}" // Cloud browser name
                            pytestCommand += " --platform=\"${params.CLOUD_PLATFORM}\"" // Cloud platform (ensure quoted)
                            // pytestCommand += " --browser-version=${params.CLOUD_BROWSER_VERSION}"
                            
                            // Remote URL based on provider
                            def remoteUrl = (params.CLOUD_PROVIDER == 'browserstack') 
                                ? "https://hub-cloud.browserstack.com/wd/hub"
                                : "https://hub.lambdatest.com/wd/hub"
                            // pytestCommand += " --remote-url=\"${remoteUrl}\""
                            
                            // Determine which credentials to use
                            def cloudCredsId = (params.CLOUD_PROVIDER == 'browserstack') 
                                ? env.BS_CREDENTIALS_ID : env.LT_CREDENTIALS_ID
                                
                            // Use withCredentials block to securely inject credentials
                            withCredentials([usernamePassword(
                                credentialsId: cloudCredsId, 
                                usernameVariable: 'CLOUD_USERNAME', 
                                passwordVariable: 'CLOUD_ACCESS_KEY')]) {
                                
                                // Add the credentials as command line arguments
                                // These will be processed by your conftest.py
                                pytestCommand += " --bs-username=\"${CLOUD_USERNAME}\"" 
                                pytestCommand += " --bs-access-key=\"${CLOUD_ACCESS_KEY}\""
                                
                                echo "Executing tests on ${params.CLOUD_PROVIDER} with secure credentials..."
                                
                                try {
                                    bat "${pytestCommand}"
                                    
                                    executedInWithCredentials = true // Mark as executed
                                } catch (err) {
                                    echo "Pytest execution failed: ${err.getMessage()}"
                                    currentBuild.result = 'FAILURE'
                                }
                            }
                        } else if (uiLocation == 'none') {
                            // If UI tests were selected but location is 'none', log a warning.
                            // The framework's conftest.py might skip UI tests if --browser is not provided, or you might add specific logic.
                            echo "UI Location set to 'none' but Test Type is '${params.TEST_TYPE}'. UI tests might be skipped or fail if not configured correctly."
                        }
                    } else {
                        echo "Skipping UI specific configuration as Test Type is 'api'."
                    }
                    
                    // --- Execute Pytest Command ---
                    // Execute the command only if it wasn't already run inside withCredentials (for cloud tests)
                    if (!executedInWithCredentials) {
                        echo "Executing Pytest command: ${pytestCommand}"
                        // Use try-catch to ensure pipeline continues to post actions even if tests fail
                        try {
                            bat  "${pytestCommand}"
                        } catch (err) {
                            echo "Pytest execution failed: ${err.getMessage()}"
                            // Optionally re-throw the error if you want the pipeline stage to fail
                            // throw err 
                            currentBuild.result = 'FAILURE' // Mark build as failed but continue to post actions
                        }
                    }
                    
                    
                }
            }
        }
    }
    
        post {
        always {
            script {
                echo "Pipeline finished. Archiving reports and logs..."
            }
    
            // Archive HTML report (still useful for download)
            archiveArtifacts artifacts: 'reports/html_report/report.html', allowEmptyArchive: true
    
            // Publish HTML report (renders it properly in Jenkins UI)
            publishHTML([
                reportDir: 'reports/html_report',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report',
                reportTitles: 'Test Results Summary',
                keepAll: true,
                allowMissing: true,
                alwaysLinkToLastBuild: true
            ])
    
            // Archive log files
            archiveArtifacts artifacts: 'AutoLogs/*.log', allowEmptyArchive: true
    
            // Archive Allure results if needed (uncomment if configured)
            // allure([includeProperties: false, results: [[path: 'reports/allure-results']]])
        }
    
        success {
            script {
                echo "Pipeline completed successfully."
                // Add success notifications (e.g., Slack, Email)
            }
        }
    
        failure {
            script {
                echo "Pipeline failed."
                // Add failure notifications
            }
        }
    
        unstable {
            script {
                echo "Pipeline finished with unstable status (e.g., test failures)."
                // Add notifications for unstable builds if needed
            }
        }
    }

    
}