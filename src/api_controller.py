"""Patient API Controller"""

from flask import Flask
from patient_db import PatientDB
from flask import jsonify
from flask import request
from patient import Patient
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL



class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the database.

    Every method in this class should return a JSON response with status code
    Status code should be 200 if the operation was successful,
    Status code should be 400 if there was a client error,
    """

    def create_patient(self):
        request_body = request.json
        try:
            # Create a new patient object
            patient = Patient(
                name=request_body.get("patient_name"),
                gender=request_body.get("patient_gender"),
                age=request_body.get("patient_age")
            )

            # Update room and ward if provided
            ward = request_body.get("patient_ward")
            room = request_body.get("patient_room")
            if ward is not None and room is not None:
                patient.update_room_and_ward(ward, room)

            # Commit patient to the database
            patient_id = self.patient_db.insert_patient(patient.__dict__)
            print(patient_id)
            if patient_id is not None:
                return jsonify({"patient_id": patient_id[0]}), 200
            else:
                return jsonify({"error": "Failed to insert patient into database"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def get_patients(self):
        patients = self.patient_db.select_all_patients()
        if patients:
            return jsonify(patients), 200
        else:
            return jsonify({"error": "Failed to retrieve patients from database"}), 400

    def get_patient(self, patient_id):
        patient = self.patient_db.select_patient(patient_id)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "Patient not found"}), 400

    def update_patient(self, patient_id):
        request_body = request.json
        try:
            update_dict = {}
            # Check if room and ward are provided
            if "patient_ward" in request_body and "patient_room" in request_body:
                ward = request_body["patient_ward"]
                room = request_body["patient_room"]
                if ward not in WARD_NUMBERS or room not in ROOM_NUMBERS[ward]:
                    return jsonify({"error": "Invalid ward or room number"}), 400
                update_dict["patient_ward"] = ward
                update_dict["patient_room"] = room

            # Update patient in the database
            rows_affected = self.patient_db.update_patient(patient_id, update_dict)
            if rows_affected is not None:
                return jsonify({"rows_affected": rows_affected}), 200
            else:
                return jsonify({"error": "Failed to update patient"}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def delete_patient(self, patient_id):
        rows_affected = self.patient_db.delete_patient(patient_id)
        if rows_affected is not None:
            return jsonify({"rows_affected": rows_affected}), 200
        else:
            return jsonify({"error": "Failed to delete patient"}), 400

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()
