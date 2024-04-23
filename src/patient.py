"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""


# Import necessary modules
from uuid import uuid4
from datetime import datetime
import requests
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL
from patient_db_config import PATIENTS_TABLE_NAME

class Patient:
    def __init__(self, name, gender, age):
        # Validate inputs
        if gender not in GENDERS:
            raise ValueError("Invalid gender")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")

        self.patient_id = str(uuid4())
        self.patient_name = name
        self.patient_age = age
        self.patient_gender = gender
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None

    def update_room_and_ward(self, ward, room):
        # Validate ward and room
        if ward not in WARD_NUMBERS:
            raise ValueError("Invalid ward number")
        if str(room) not in ROOM_NUMBERS[ward]:
            raise ValueError(f"Invalid room number: {ROOM_NUMBERS[ward]}, {ward}, {room}")

        self.patient_ward = ward
        self.patient_room = room

    def commit_to_database(self):
        # Prepare request body
        request_body = {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "patient_age": self.patient_age,
            "patient_gender": self.patient_gender,
            "patient_checkin": self.patient_checkin,
            "patient_ward": self.patient_ward,
            "patient_room": self.patient_room
        }

        # Make POST request to API controller
        try:
            response = requests.post(f"{API_CONTROLLER_URL}/patients", json=request_body)
            if response.status_code == 200:
                print("Patient successfully committed to the database.")
            else:
                print("Error committing patient to the database:", response.text)
        except requests.RequestException as e:
            print("Error:", e)

