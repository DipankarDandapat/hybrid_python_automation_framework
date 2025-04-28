// Jenkinsfile (Declarative Pipeline)

// This pipeline runs a Python pytest automation framework with parameterized options
// for environment, test type, and UI testing configurations (local/cloud).

pipeline {
    agent any // Use 'agent any' or specify a label for agents with Python/Git/Browsers installed

    environment {
        // Define environment variables
        PYTHON_VERSION = "3.10" // Specify desired Python version
        VENV_DIR = "venv"       // Virtual environment directory name
        
        // --- IMPORTANT: Replace these with your actual Jenkins Credential IDs ---
        BS_CREDENTIALS_ID = "browserstack-credentials" // Jenkins Credential ID for BrowserStack username/access key
        LT_CREDENTIALS_ID = "lambdatest-credentials"   // Jenkins Credential ID for LambdaTest username/access key
        GITHUB_CREDENTIALS_ID = "github-credentials"     // Jenkins Credential ID for GitHub (if repository is private)
    }

    parameters {
        // --- Git Repository Parameters ---
        string(name: 'GIT_REPO_URL', defaultValue: 'https://github.com/your-username/your-repo.git', description: 'Git repository URL for the automation framework')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to checkout')
        
        // --- Test Execution Parameters ---
        choice(name: 'ENVIRONMENT', choices: ["staging", "prod"], description: 'Select the target environment (e.g., staging, prod)')
        choice(name: 'TEST_TYPE', choices: ["api", "ui", "all"], description: 'Select the type of tests to run (api, ui, or all)')
        
        // --- UI Testing Parameters (Relevant only if TEST_TYPE is \'ui\' or \'all\') ---
        choice(name: 'UI_LOCATION', choices: ["none", "local", "cloud"], defaultValue: "none", description: 'Run UI tests locally on the agent or on a cloud provider? (Select \'none\') if running API tests only')
        
        // --- Local UI Options (Relevant only if UI_LOCATION is \'local\') ---
        choice(name: 'LOCAL_BROWSER', choices: ["chrome", "firefox", "edge"], defaultValue: "chrome", description: 'Select the browser for local UI execution')
        booleanParam(name: 'HEADLESS_MODE', defaultValue: false, description: 'Run the local browser in headless mode?')
        
        // --- Cloud UI Options (Relevant only if UI_LOCATION is \'cloud\') ---
        choice(name: 'CLOUD_PROVIDER', choices: ["browserstack", "lambdatest"], defaultValue: "browserstack", description: 'Select the cloud testing provider')
        string(name: 'CLOUD_PLATFORM', defaultValue: 'Windows 10', description: 'Specify the OS platform for cloud testing (e.g., \'Windows 10\', \'macOS Big Sur\')')
        string(name: 'CLOUD_BROWSER', defaultValue: 'chrome', description: 'Specify the browser name for cloud testing')
        string(name: 'CLOUD_BROWSER_VERSION', defaultValue: 'latest', description: 'Specify the browser version for cloud testing (e.g., \'latest\', \'100.0\')')
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    log.info("Checking out code from ${params.GIT_REPO_URL} branch ${params.GIT_BRANCH}")
                }
                // Checkout code from Git
                // Use credentialsId parameter if the repository is private
                // checkout([
                //     $class: 'GitSCM',
                //     branches: [[name: params.GIT_BRANCH]],
                //     userRemoteConfigs: [[url: params.GIT_REPO_URL, credentialsId: env.GITHUB_CREDENTIALS_ID]]
                // ])
                // For public repositories:
                 checkout([
                     $class: 'GitSCM',
                     branches: [[name: params.GIT_BRANCH]],
                     userRemoteConfigs: [[url: params.GIT_REPO_URL]]
                 ])
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    log.info("Setting up Python ${env.PYTHON_VERSION} virtual environment")
                    // Ensure the correct Python version is available on the agent
                    // You might need to configure Tool Installations in Jenkins (Manage Jenkins -> Global Tool Configuration)
                    // and potentially use the tool directive: tool name: "Python ${env.PYTHON_VERSION}", type: "python"
                    
                    // Create virtual environment
                    // Ensure the python command corresponds to the desired version (e.g., python3.10, python)
                    sh "python${env.PYTHON_VERSION} -m venv ${env.VENV_DIR}"
                    
                    log.info("Installing dependencies from requirements.txt")
                    // Activate venv and install dependencies
                    // This command works for Linux/macOS agents. Adjust for Windows if necessary.
                    sh ". ${env.VENV_DIR}/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
                    // Windows equivalent example: 
                    // bat "${env.VENV_DIR}\\Scripts\\activate && pip install -r requirements.txt"
                }
            }
        }

        stage('Execute Pytest Tests') {
            steps {
                script {
                    log.info("Constructing pytest command based on parameters...")
                    // Base pytest command, activating the virtual environment
                    // Adjust activation based on agent OS if needed
                    def pytestCommand = ". ${env.VENV_DIR}/bin/activate && pytest"
                    
                    // Add common options
                    pytestCommand += " --verbose"
                    pytestCommand += " --environment=${params.ENVIRONMENT}"
                    pytestCommand += " --alluredir=reports/allure-results" // Ensure Allure results are generated
                    pytestCommand += " --html=reports/html_report/report.html --self-contained-html" // Generate HTML report
                    
                    // Add test type filtering marker if not running 'all'
                    if (params.TEST_TYPE != 'all') {
                        // Assuming your conftest.py skips tests based on this marker
                        pytestCommand += " --test-type=${params.TEST_TYPE}"
                        log.info("Running only ${params.TEST_TYPE} tests.")
                    } else {
                        log.info("Running all tests (API and UI).")
                    }

                    // --- Handle UI Test Parameters ---
                    def runUiTests = (params.TEST_TYPE == 'ui' || params.TEST_TYPE == 'all')
                    def uiLocation = params.UI_LOCATION
                    def executedInWithCredentials = false // Flag to track if sh command ran inside withCredentials

                    if (runUiTests) {
                        if (uiLocation == 'local') {
                            log.info("Configuring for Local UI tests on ${params.LOCAL_BROWSER}")
                            pytestCommand += " --browser=${params.LOCAL_BROWSER}"
                            if (params.HEADLESS_MODE) {
                                pytestCommand += " --headless"
                                log.info("Headless mode enabled.")
                            }
                        } else if (uiLocation == 'cloud') {
                            log.info("Configuring for Cloud UI tests on ${params.CLOUD_PROVIDER}")
                            pytestCommand += " --remote" // Flag to indicate cloud execution
                            pytestCommand += " --browser=${params.CLOUD_BROWSER}" // Cloud browser name
                            pytestCommand += " --platform=\"${params.CLOUD_PLATFORM}\"" // Cloud platform (ensure quoted)
                            
                            // Determine which credentials to use
                            def cloudCredsId = (params.CLOUD_PROVIDER == 'browserstack') ? env.BS_CREDENTIALS_ID : env.LT_CREDENTIALS_ID
                            
                            // Inject cloud credentials securely as environment variables
                            withCredentials([usernamePassword(credentialsId: cloudCredsId, usernameVariable: 'CLOUD_USERNAME', passwordVariable: 'CLOUD_ACCESS_KEY')]) {
                                // Set environment variables required by the framework for cloud testing
                                // IMPORTANT: Ensure these variable names (e.g., BS_USERNAME, REMOTE_URL) match what your framework expects
                                env.BS_USERNAME = env.CLOUD_USERNAME 
                                env.BS_ACCESS_KEY = env.CLOUD_ACCESS_KEY
                                env.REMOTE_URL = (params.CLOUD_PROVIDER == 'browserstack') ? "https://hub-cloud.browserstack.com/wd/hub" : "https://hub.lambdatest.com/wd/hub"
                                env.BROWSER_VERSION = params.CLOUD_BROWSER_VERSION // Pass browser version
                                
                                log.info("Executing tests on ${params.CLOUD_PROVIDER} with injected credentials...")
                                // Execute the command within the credentials scope
                                sh "${pytestCommand}"
                                executedInWithCredentials = true // Mark as executed
                            }
                        } else if (uiLocation == 'none') {
                            // If UI tests were selected but location is 'none', log a warning.
                            // The framework's conftest.py might skip UI tests if --browser is not provided, or you might add specific logic.
                            log.warn("UI Location set to 'none' but Test Type is '${params.TEST_TYPE}'. UI tests might be skipped or fail if not configured correctly.")
                        }
                    } else {
                        log.info("Skipping UI specific configuration as Test Type is 'api'.")
                    }
                    
                    // --- Execute Pytest Command ---
                    // Execute the command only if it wasn't already run inside withCredentials (for cloud tests)
                    if (!executedInWithCredentials) {
                         log.info("Executing Pytest command: ${pytestCommand}")
                         // Use try-catch to ensure pipeline continues to post actions even if tests fail
                         try {
                             sh "${pytestCommand}"
                         } catch (err) {
                             log.error("Pytest execution failed: ${err.getMessage()}")
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
                log.info("Pipeline finished. Archiving reports and logs...")
            }
            // Archive HTML report
            archiveArtifacts artifacts: 'reports/html_report/report.html', allowEmptyArchive: true
            // Archive log files
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
            // Archive Allure results for the Allure Jenkins plugin
            // Ensure the Allure Jenkins plugin is installed and configured
            // allure([includeProperties: false, 
            //         results: [[path: 'reports/allure-results']]])
            
            // Clean up workspace
            cleanWs()
        }
        success {
            script {
                log.info("Pipeline completed successfully.")
                // Add success notifications (e.g., Slack, Email)
            }
        }
        failure {
            script {
                log.error("Pipeline failed.")
                // Add failure notifications
            }
        }
        unstable {
             script {
                log.warn("Pipeline finished with unstable status (e.g., test failures).")
                // Add notifications for unstable builds if needed
            }
        }
    }
}

