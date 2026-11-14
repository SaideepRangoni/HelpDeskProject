import azure.functions as func
import json
import uuid
import os
import logging

from azure.data.tables import TableServiceClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = func.FunctionApp()


# COMMON FUNCTION TO CONNECT TO AZURE TABLE STORAGE

def get_table_client():

    connection_string = os.getenv("AzureWebJobsStorage")

    if not connection_string:
        raise ValueError("AzureWebJobsStorage connection string is missing")

    table_service = TableServiceClient.from_connection_string(
        conn_str=connection_string
    )

    table_service.create_table_if_not_exists("Tickets")

    table_client = table_service.get_table_client("Tickets")

    return table_client


# CREATE TICKET API

@app.route(route="CreateTicket", auth_level=func.AuthLevel.ANONYMOUS)
def CreateTicket(req: func.HttpRequest) -> func.HttpResponse:

    try:

        data = req.get_json()

        employee_name = data.get("employeeName")
        issue_type = data.get("issueType")
        priority = data.get("priority")
        description = data.get("description")

        if not employee_name or not issue_type or not priority or not description:

            return func.HttpResponse(
                json.dumps({"error": "All fields are required"}),
                mimetype="application/json",
                status_code=400
            )

        ticket_id = str(uuid.uuid4())[:8]

        ticket = {
            "ticketId": ticket_id,
            "employeeName": employee_name,
            "issueType": issue_type,
            "priority": priority,
            "description": description,
            "status": "Open"
        }

        table_client = get_table_client()

        entity = {
            "PartitionKey": "Support",
            "RowKey": ticket_id,
            "TicketId": ticket_id,
            "EmployeeName": employee_name,
            "IssueType": issue_type,
            "Priority": priority,
            "Description": description,
            "Status": "Open"
        }

        table_client.create_entity(entity=entity)

        logging.info("Ticket created successfully: %s", ticket_id)

        return func.HttpResponse(
            json.dumps({
                "message": "Ticket created successfully",
                "ticket": ticket
            }),
            mimetype="application/json",
            status_code=201
        )

    except Exception:

        logging.exception("Error while creating ticket")

        return func.HttpResponse(
            json.dumps({"error": "Unable to create ticket"}),
            mimetype="application/json",
            status_code=500
        )


# SEND EMAIL USING SENDGRID

def send_email(report):

    try:

        message = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=os.getenv("TO_EMAIL"),
            subject="Help Desk Daily Report",
            plain_text_content=report
        )

        sg = SendGridAPIClient(
            os.getenv("SENDGRID_API_KEY")
        )

        response = sg.send(message)

        logging.info(
            "Email sent successfully. Status: %s",
            response.status_code
        )

    except Exception:

        logging.exception("Email sending failed")


# GENERATE DAILY REPORT AT 6:00 AM IST

@app.timer_trigger(
    schedule="0 30 0 * * *",
    arg_name="mytimer",
    run_on_startup=False
)
def GenerateReport(mytimer: func.TimerRequest) -> None:

    try:

        logging.info("Daily Help Desk Report generation started.")

        table_client = get_table_client()

        tickets = list(table_client.list_entities())

        total_tickets = len(tickets)

        closed_tickets = sum(
            1 for ticket in tickets
            if ticket.get("Status") == "Closed"
        )

        open_tickets = sum(
            1 for ticket in tickets
            if ticket.get("Status") == "Open"
        )

        high_priority = sum(
            1 for ticket in tickets
            if ticket.get("Priority") == "High"
        )

        # Generate report

        report = f"""
========== HELP DESK DAILY REPORT ==========

Total Tickets  : {total_tickets}
Open Tickets   : {open_tickets}
Closed Tickets : {closed_tickets}
High Priority  : {high_priority}

============================================

TICKET DETAILS:
"""

        for ticket in tickets:

            report += f"""

------------------------
Ticket ID : {ticket.get('TicketId')}
Employee  : {ticket.get('EmployeeName')}
Issue     : {ticket.get('IssueType')}
Priority  : {ticket.get('Priority')}
Status    : {ticket.get('Status')}
------------------------

"""

        # Log report in Application Insights

        logging.info(report)

        # Send report through SendGrid

        send_email(report)

        logging.info("Daily Help Desk Report process completed.")

    except Exception:

        logging.exception("Error generating daily Help Desk report")