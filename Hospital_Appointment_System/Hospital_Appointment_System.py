import requests
from datetime import datetime
import smtplib
import dotenv
import os

dotenv.load_dotenv()

sheet_url = "https://api.sheety.co/468fa27b225c199db6181089b7355d81/hospitalAppointmentScheduler/hospital"

GMAIL = 'waleedkamal801@gmail.com'
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_API = 'smtp.gmail.com'
GMAIL_PORT = 587

# It will fetch all data from Google Spreadsheet.


def fetchAppointments():
    try:
        res = requests.get(url=sheet_url)
        res.raise_for_status()
        data = res.json().get('hospital', [])
        return data
    except Exception as e:
        print(f'Error: {e}')


def mail(GMAILTO, subject, message):
    '''It is used to send message through Gmail to the person given in the Google Spreadsheet.'''
    with smtplib.SMTP(GMAIL_API, GMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(GMAIL, GMAIL_PASSWORD)
        send = f"SUbject:{subject}\n\n{message}"
        smtp.sendmail(GMAIL, GMAILTO, send)
        smtp.quit()


# For Faisal Bhai
def update_sheet_for_Not_visiting(i_id):
    '''This function is used to Change status of Non Visited person to Last Reminder.'''

    try:
        hospitalAppointmentScheduler = {
            "hospital": {
                'status': "Last Reminder"
            }
        }

        upadate_res = requests.put(
            url=f"{sheet_url}/{i_id}", json=hospitalAppointmentScheduler)
        upadate_res.raise_for_status()
    except Exception as e:
        print(f'Error: {e}')


def update_sheet_for_Registered(i_id):
    '''This function is used to Change status of Registered person to Non Visited.'''

    try:
        hospitalAppointmentScheduler = {
            "hospital": {
                'status': "Not Visited"
            }
        }

        upadate_res = requests.put(
            url=f"{sheet_url}/{i_id}", json=hospitalAppointmentScheduler)
        upadate_res.raise_for_status()
    except Exception as e:
        print(f'Error: {e}')

# For Faisal Bhai


def delete_appointment(i_id):
    '''This function is used to delete data/appointment of a person from the Google Spreadsheet.'''

    try:
        del_data = requests.delete(url=f"{sheet_url}/{i_id}")
        del_data.raise_for_status()
    except Exception as e:
        print(f'Error: {e}')


fetchAppointments = fetchAppointments()
date = datetime.now()
date_now = date.strftime("%m/%d/%Y")
print(f'datetime, {date_now}')
for appointment in fetchAppointments:
    if appointment['dateOfAppointment'] <= date_now and appointment['status'] == "Registered":
        subject = f"Appointment Confirmation for {
            appointment['dateOfAppointment']}"
        message = f"""Assalamualaikum {appointment['patientsName']},

We have received your registration for the appointment on {appointment['dateOfAppointment']}. We are pleased to inform you that your appointment has been confirmed. We are looking forward to seeing you on the scheduled date and time.

However, should you be unable to visit us on the scheduled date and time, please inform us at least 24 hours before the scheduled appointment time. We will be more than happy to reschedule the appointment for you.

Thank you for your cooperation.

For any query please call:
03242923319

Regards,
Hospital Administration.
"""

        mail(appointment['email'], subject, message)

    elif appointment['dateOfAppointment'] == date_now and appointment['status'] == "Registered":
        subject = "Your Appointment on {appointment['dateOfAppointment']}"
        message = f"""Assalamualaikum {appointment['patientsName']},

We have received your registration for the appointment on {appointment['dateOfAppointment']}. We are pleased to inform you that your appointment date has been arrived. However, It seems that you have not visited us yet on the scheduled date and time.

Please visit us on the scheduled date and time. If you are unable to visit us on the scheduled date and time, please inform us at least 24 hours before the scheduled appointment time. We will be more than happy to reschedule the appointment for you.

Thank you for your cooperation.

For any query please call:
03242923319

Regards,
Hospital Administration.
"""

        mail(appointment['email'], subject, message)
        update_sheet_for_Registered(appointment['id'])

    # For Faisal Bhai
    elif appointment['status'] == "Visited":
        subject = "Confirmation of Appointment, Visit and Removal from List"
        message = f"""Assalamualaikum {appointment['patientsName']},
We see that you’ve already visited the department. We will now proceed to remove your appointment from our list. Thank you for attending your appointment. If you need further assistance or wish to reschedule.

Thank you.

For any query please call:
03242923319

Regards,
Hospital Administration.
"""

        delete_appointment(appointment['id'])

    # For Faisal Bhai
    elif appointment['status'] == "Not Visited":
        subject = "Final Reminder: Confirm Your Appointment or Visit Us"
        message = f"""Assalamualaikum {appointment['patientsName']},
You came in our hospital on {appointment['dateTakenOn']} and have taken appointment for {appointment['dateOfAppointment']} for the desease of {appointment['disease']} and the age  of patient is {appointment['age']} but you still not visited in the department. It is your last Reminder otherwise your registeration will be cancelled. If you want to cancel registration so please call in the given number. So please visit on the desired timing {appointment['timing']}.If you want to cancel your registration so please call on the given number.
Thank you.

Thank you.

For any query please call:
03242923319

Regards,
Hospital Administration.
"""
        update_sheet_for_Not_visiting(appointment['id'])
        mail(appointment['email'], subject, message)

    elif appointment['status'] == "Last Reminder":
        subject = "Final Reminder: Confirm Your Appointment or Visit Us"
        message = f"""Assalamualaikum {appointment['patientsName']},
We are sorry to inform you that your appointment for {appointment['dateOfAppointment']} for {appointment['disease']} is not attended yet. As per our record, you have received several reminders but you haven't visited us yet. So, we have cancelled your appointment.

Thank you.

For any query please call:
03242923319

Regards,
Hospital Administration.
"""
        delete_appointment(appointment['id'])
        mail(appointment['email'], subject, message)
