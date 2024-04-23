"""patient_db module"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import operators
from sqlalchemy import select
from patient_db_config import PATIENTS_TABLE, ENGINE


class PatientDB:
    """
    A class representing a patient database.

    This class provides methods to interact with the patient database, including
    inserting, selecting, updating, and deleting patient records.

    Attributes:
        None

    Methods:
        insert_patient: Inserts a new patient record into the database.
        row_to_dict: Converts a database row to a dictionary.
        select_all_patients: Retrieves all patient records from the database.
        select_patient: Retrieves a specific patient record from the database.
        update_patient: Updates a specific patient record in the database.
        delete_patient: Deletes a specific patient record from the database.
    """

    def __init__(self):
        pass

    def insert_patient(self, request_body):
        """
        Inserts a new patient record into the database.

        Args:
            request_body (dict): The request body containing the patient information.

        Returns:
            str: The primary key of the inserted patient record, or None if an error occurred.
        """
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.insert().values(**request_body)
            result = conn.execute(stmt)
            conn.commit()
            return result.inserted_primary_key
        except SQLAlchemyError as e:
            print("Error occurred while inserting the patient", e)
            return None
        finally:
            conn.close()

    def row_to_dict(self, row_keys, row_values):
        """
        Converts a database row to a dictionary.

        Args:
            row_keys (list): The list of column names.
            row_values (tuple): The tuple of row values.

        Returns:
            dict: The dictionary representation of the row.
        """
        return dict(zip(row_keys, row_values))

    def select_all_patients(self):
        """
        Retrieves all patient records from the database.

        Returns:
            list: A list of dictionaries representing the patient records,
            or None if an error occurred.
        """
        try:
            conn = ENGINE.connect()
            stmt = select(PATIENTS_TABLE)
            result = conn.execute(stmt)
            keys = result.keys()
            rows = result.fetchall()
            patients = [dict(zip(keys, row)) for row in rows]
            return patients
        except SQLAlchemyError as e:
            print("Error occurred while selecting all patients", e)
            return None
        finally:
            conn.close()

    def fetch_patient_id_by_name(self, patient_name):
        """
        Retrieves the patient ID by patient name.

        Args:
            patient_name (str): The name of the patient.

        Returns:
            int: The patient ID, or None if an error occurred.
        """
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.select().where(
                operators.like_op(
                    PATIENTS_TABLE.c.patient_name,
                    "%"+patient_name+"%"
                )
            )
            result = conn.execute(stmt)
            keys = result.keys()
            rows = result.fetchall()
            patients = [dict(zip(keys, row)) for row in rows]
            return patients
        except SQLAlchemyError as e:
            print("Error occurred while fetching patient ID by name", e)
            return None
        finally:
            conn.close()

    def select_patient(self, patient_id):
        """
        Retrieves a specific patient record from the database.

        Args:
            patient_id (int): The ID of the patient.

        Returns:
            dict: A dictionary representing the patient record, or None if an error occurred.
        """
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.select().where(
                PATIENTS_TABLE.c.patient_id == patient_id
            )
            result = conn.execute(stmt)
            keys = result.keys()
            values = result.fetchone()
            patient = self.row_to_dict(keys, values)
            print(patient)
            return patient
        except SQLAlchemyError as e:
            print("Error occurred while selecting the patient", e)
            return None
        finally:
            conn.close()

    def update_patient(self, patient_id, update_dict):
        """
        Updates a specific patient record in the database.

        Args:
            patient_id (int): The ID of the patient.
            update_dict (dict): The dictionary containing the updated patient information.

        Returns:
            int: The number of affected rows, or None if an error occurred.
        """
        try:
            conn = ENGINE.connect()
            stmt = (
                PATIENTS_TABLE.update()
                .where(PATIENTS_TABLE.c.patient_id == patient_id)
                .values(**update_dict)
            )
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            print("Error occurred while updating the patient", e)
            return None
        finally:
            conn.close()

    def delete_patient(self, patient_id):
        """
        Deletes a specific patient record from the database.

        Args:
            patient_id (int): The ID of the patient.

        Returns:
            int: The number of affected rows, or None if an error occurred.
        """
        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.delete().where(
                PATIENTS_TABLE.c.patient_id == patient_id
            )
            result = conn.execute(stmt)

            conn.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            print("Error occurred while deleting the patient", e)
            return None
        finally:
            conn.close()
