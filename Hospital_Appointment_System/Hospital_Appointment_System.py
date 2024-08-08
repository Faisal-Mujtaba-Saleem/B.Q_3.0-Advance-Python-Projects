import requests
from datetime import datetime
import smtplib
import dotenv
import os

dotenv.load_dotenv()

sheet_url = "https://api.sheety.co/0f1220c277b74c4f1e9beebad404884a/hospitalAppointmentScheduler/hospital1"

GMAIL = 'waleedkamal801@gmail.com'
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_API = 'smtp.gmail.com'
GMAIL_PORT = 587


def fetch_appointments():
    try:
        res = requests.get(url=sheet_url)
        res.raise_for_status()
        # print(res.text)
        data = res.json().get('hospital1', [])
        return data
    except Exception as e:
        print(f'Error: {e}')
        return []


def send_mail(mail_to, subject, message):
    '''It is used to send message through Gmail to the person given in the Google Spreadsheet.'''
    with smtplib.SMTP(GMAIL_API, GMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(GMAIL, GMAIL_PASSWORD)
        send = f"Subject:{subject}\n\n{message}"
        smtp.sendmail(GMAIL, mail_to, send)


def update_sheet_status(i_id, status):
    try:
        hospitalAppointmentScheduler = {
            "hospital1": {
                'status': status
            }
        }
        update_res = requests.put(
            url=f"{sheet_url}/{i_id}", json=hospitalAppointmentScheduler)
        update_res.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'Response content: {http_err.response.content}')
    except Exception as e:
        print(f'Error: {e}')


def delete_appointment(i_id):
    '''This function is used to delete data/appointment of a person from the Google Spreadsheet.'''
    try:
        del_data = requests.delete(url=f"{sheet_url}/{i_id}")
        del_data.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'Response content: {http_err.response.content}')
    except Exception as e:
        print(f'Error: {e}')


date_now = datetime.now().strftime("%m/%d/%Y")


def iterate_sheet_update_status_and_send_mail():
    appointments_fetched_to_update_status = fetch_appointments()

    for appointment in appointments_fetched_to_update_status:
        if appointment['dateOfAppointment'] < date_now and appointment['status'] == "Registered":
            subject = f"Appointment Notification for {
                appointment['dateOfAppointment']}"
            message = f"""Assalamualaikum {appointment['patientsName']},
                        <Your message content>
                        Regards,
                        Hospital Administration.
                        """
            send_mail(appointment['email'], subject, message)

        elif appointment['dateOfAppointment'] == date_now and appointment['status'] == "Registered":
            subject = f"Your Appointment on {appointment['dateOfAppointment']}"
            message = f"""Assalamualaikum {appointment['patientsName']},
                        <Your message content>
                        Regards,
                        Hospital Administration.
                        """
            send_mail(appointment['email'], subject, message)
            update_sheet_status(appointment['id'], "Not Visited")

        elif appointment['status'] == "Visited":
            subject = "Confirmation of Appointment, Visit and Removal from List"
            message = f"""Assalamualaikum {appointment['patientsName']},
                        <Your message content>
                        Regards,
                        Hospital Administration.
                        """
            send_mail(appointment['email'], subject, message)

        elif appointment['status'] == "Not Visited":
            subject = "Final Reminder: Confirm Your Appointment or Visit Us"
            message = f"""Assalamualaikum {appointment['patientsName']},
                        <Your message content>
                        Regards,
                        Hospital Administration.
                        """
            send_mail(appointment['email'], subject, message)
            update_sheet_status(appointment['id'], "Last Reminder")

        elif appointment['status'] == "Last Reminder":
            subject = "Cancellation of Appointment"
            message = f"""Assalamualaikum {appointment['patientsName']},
                        <Your message content>
                        Regards,
                        Hospital Administration.
                        """
            send_mail(appointment['email'], subject, message)


def iterate_sheet_and_delete_appointments():
    while True:
        appointments_fetched_to_delete = fetch_appointments()
        # print(appointments_fetched_to_delete)
        for appointment in appointments_fetched_to_delete:
            if appointment['status'] == "Visited" or appointment['status'] == "Last Reminder":
                delete_appointment(appointment['id'])
        if not any(appointment['status'] == "Visited" or appointment['status'] == "Last Reminder" for appointment in appointments_fetched_to_delete):
            break


iterate_sheet_and_delete_appointments()
iterate_sheet_update_status_and_send_mail()
