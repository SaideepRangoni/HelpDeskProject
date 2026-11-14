# ☁️ Serverless Help Desk Ticketing System using Azure Functions

A cloud-based Help Desk Ticketing System developed using **Python, Azure Functions, and Azure Table Storage**. This project demonstrates serverless computing by automating ticket creation, cloud storage, daily report generation, and email notifications.

## 📌 Project Overview

The Serverless Help Desk Ticketing System allows employees to submit technical support requests through a web-based interface.

When an employee submits a ticket, an HTTP-triggered Azure Function processes the request, validates the information, generates a unique Ticket ID, and stores the ticket in Azure Table Storage.

Additionally, a timer-triggered Azure Function automatically generates a daily ticket report at **6:00 AM IST** and sends it through SendGrid email integration.

## 🎯 Project Objectives

- Implement serverless computing using Azure Functions.
- Develop an HTTP-triggered API using Python.
- Store ticket information in Azure Table Storage.
- Automate daily report generation using Timer Trigger.
- Integrate SendGrid for email notifications.
- Monitor application execution using Azure Application Insights.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Azure Functions | Serverless execution |
| Azure Table Storage | Ticket data storage |
| Azure Storage Account | Function storage and configuration |
| SendGrid | Email notifications |
| Application Insights | Monitoring and logging |
| HTML | Frontend development |
| CSS | User interface styling |
| JavaScript | Frontend-to-backend communication |
| VS Code | Development environment |
| Git & GitHub | Version control and project hosting |

## 🏗️ Project Architecture

```text
             Employee
                |
                |
          Help Desk Web Page
             (HTML/CSS)
                |
                |
          HTTP POST Request
                |
                v
         Azure Functions
                |
          CreateTicket
           (HTTP Trigger)
                |
                v
        Input Validation
                |
                v
         Generate Ticket ID
                |
                v
       Azure Table Storage
                |
                |
       Ticket Information
                |
                v
       Application Insights
        (Logs & Monitoring)


       Automated Reporting
                |
                v
        GenerateReport
         (Timer Trigger)
                |
                v
       Retrieve Ticket Data
                |
                v
        Generate Daily Report
                |
                v
             SendGrid
                |
                v
         Email Notification
```

## ⚙️ Key Features

### 1. HTTP Trigger – Create Ticket

- Accepts employee details through an HTTP POST request.
- Receives employee name, issue category, priority, and description.
- Validates all required fields.
- Generates a unique Ticket ID using UUID.
- Assigns the initial ticket status as `Open`.
- Stores ticket information in Azure Table Storage.
- Returns an HTTP 201 response after successful ticket creation.

### 2. Azure Table Storage Integration

- Creates the `Tickets` table if it does not already exist.
- Stores ticket information as table entities.
- Uses `Support` as the Partition Key.
- Uses the unique Ticket ID as the Row Key.

### 3. Timer Trigger – Daily Report Generation

- Executes automatically every day at 6:00 AM IST.
- Retrieves ticket records from Azure Table Storage.
- Calculates:
  - Total Tickets
  - Open Tickets
  - Closed Tickets
  - High-Priority Tickets
- Generates a formatted daily report.

### 4. SendGrid Email Integration

- Sends the generated daily report through SendGrid.
- Uses environment variables to configure email credentials.
- Logs successful email delivery and errors.

### 5. Application Insights Monitoring

- Monitors Azure Function execution.
- Captures application logs and exceptions.
- Helps troubleshoot application issues.
- Provides visibility into serverless application execution.

## 📂 Project Structure

```text
HelpDeskProject/
│
├── function_app.py
│
├── helpdesk.html
│
├── requirements.txt
│
├── host.json
│
├── .funcignore
│
├── .gitignore
│
├── local.settings.json
│
├── tickets.json
│
└── .vscode/
```

**File Description:**

| File | Description |
|---|---|
| `function_app.py` | Contains HTTP Trigger, Timer Trigger, storage integration and email functionality. |
| `helpdesk.html` | Frontend interface for submitting support tickets. |
| `requirements.txt` | Python dependencies required for the project. |
| `host.json` | Azure Functions host configuration. |
| `local.settings.json` | Local development settings and environment variables. |
| `.funcignore` | Specifies files excluded during Azure Functions publishing. |
| `.gitignore` | Specifies files excluded from Git tracking. |
| `tickets.json` | Additional project file. |

## 🚀 Installation and Setup

### Prerequisites

- Python
- Visual Studio Code
- Azure Functions Core Tools v4
- Azure CLI
- Azure Storage Account
- Azure Subscription
- SendGrid Account

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project directory:

```bash
cd HelpDeskProject
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Configure the required settings in your local `local.settings.json` file:

- `AzureWebJobsStorage`
- `FUNCTIONS_WORKER_RUNTIME`
- `FROM_EMAIL`
- `TO_EMAIL`
- `SENDGRID_API_KEY`

Use your own Azure Storage connection string and SendGrid credentials.

**Important:** Never upload actual connection strings, API keys, passwords, or other secrets to GitHub.

### Step 5: Run Azure Functions Locally

```bash
func start
```

The HTTP-triggered function will be available at:

```text
http://localhost:7071/api/CreateTicket
```

### Step 6: Run the Frontend

Open `helpdesk.html` using Visual Studio Code Live Server.

Submit a support ticket through the web interface and verify the response.

## 🧪 Testing and Validation

The following scenarios can be used to validate the application:

| Test Case | Expected Result |
|---|---|
| Submit a valid ticket | Ticket created successfully |
| Submit without required fields | HTTP 400 Bad Request |
| Successfully create a ticket | HTTP 201 Created |
| Store ticket information | Record appears in Azure Table Storage |
| Execute daily timer | Daily report is generated |
| Send report through SendGrid | Email delivery is attempted |
| Monitor application execution | Logs available through Application Insights |

## 🔐 Security Considerations

- Store sensitive configuration values in environment variables or Azure application settings.
- Do not commit `local.settings.json` containing secrets.
- Use secure authentication and authorization for production deployments.
- Protect Azure Storage credentials and SendGrid API keys.

**Note:** The current HTTP endpoint uses anonymous authorization for demonstration purposes. Production applications should implement appropriate access controls.

## 📊 Expected Outcome

The project demonstrates an end-to-end serverless workflow:

1. Employee submits a support ticket.
2. Azure Function receives and validates the request.
3. A unique Ticket ID is generated.
4. Ticket information is stored in Azure Table Storage.
5. Application execution is monitored through Application Insights.
6. A scheduled Azure Function generates the daily ticket report.
7. SendGrid is used to send the report through email.

## 🎓 Learning Outcomes

Through this project, I gained practical experience in:

- Azure Functions and serverless architecture.
- HTTP Trigger and Timer Trigger implementation.
- Python backend development.
- Azure Table Storage integration.
- Environment variable configuration.
- Automated scheduled tasks.
- SendGrid email integration.
- Application Insights monitoring.
- Git and GitHub version control.

## 👨‍💻 Author

**Developed as a hands-on Azure Serverless Computing project.**

**Project:** Serverless Functions with Azure Functions  
**Application:** Help Desk Ticketing System  
**Backend:** Python  
**Cloud Platform:** Microsoft Azure

---

⭐ If you find this project useful, feel free to explore the repository and learn more about Azure serverless computing.
