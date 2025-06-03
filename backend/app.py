from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../frontend_code')
CORS(app)

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'my_thesis_db'),
        user=os.getenv('DB_USER', 'myuser'),
        password=os.getenv('DB_PASSWORD', 'Jeet@1999')
    )
    return conn

# Serve static files from frontend_code directory
@app.route('/')
def serve_dashboard():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Patient Management Routes
@app.route('/get_patients', methods=['GET'])
def get_patients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM patient_details ORDER BY name')
    patients = [{'id': row[0], 'name': row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO patient_details (id, name, created_at) VALUES (%s, %s, %s)',
            (data['id'], data['name'], datetime.now())
        )
        conn.commit()
        return jsonify({'message': 'Patient added successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/update_patient', methods=['PUT'])
def update_patient():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'UPDATE patient_details SET name = %s, updated_at = %s WHERE id = %s',
            (data['name'], datetime.now(), data['id'])
        )
        conn.commit()
        return jsonify({'message': 'Patient updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/delete_patient/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM patient_details WHERE id = %s', (patient_id,))
        conn.commit()
        return jsonify({'message': 'Patient deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Form Submission Routes
@app.route('/submit_patient_details', methods=['POST'])
def submit_patient_details():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO patient_details (
                id, name, date_of_birth, gender, age, height, weight, bmi,
                contact_info, medical_history, allergies, current_medications,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['hospitalId'], data['patientName'], data.get('dateOfBirth'),
            data.get('sex'), data.get('age'), data.get('height'),
            data.get('weight'), data.get('bmi'), data.get('contactNo'),
            data.get('historyOfIllness'), data.get('allergies'),
            data.get('asthmaMedicines'), datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'Patient details submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/submit_hrv', methods=['POST'])
def submit_hrv():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO hrv_data (
                patient_id, patient_name, mean_rr, sd_rr, rmssd, nn50, pnn50,
                sdnn, vlf, lf, hf, total_power, lf_hf_ratio, lf_nu, hf_nu,
                timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['patientId'], data['patientName'], data['meanRR'],
            data['sdRR'], data['rmssd'], data['nn50'], data['pnn50'],
            data['sdnn'], data['vlf'], data['lf'], data['hf'],
            data['totalPower'], data['lfHfRatio'], data['lfNu'],
            data['hfNu'], datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'HRV data submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/submit_aqlq', methods=['POST'])
def submit_aqlq():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO aqlq_data (
                patient_id, patient_name, activity_limitation, symptoms,
                emotional_function, environmental_stimuli, total_score,
                timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['patientId'], data['patientName'], data['activityLimitation'],
            data['symptoms'], data['emotionalFunction'],
            data['environmentalStimuli'], data['totalScore'],
            datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'AQLQ data submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/submit_p300', methods=['POST'])
def submit_p300():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO p300_data (
                patient_id, patient_name, latency_n1, latency_p2,
                latency_n2, latency_p300, amp_n1p2, amp_p2n2, amp_n2p3,
                timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['patientId'], data['patientName'], data['latencyN1'],
            data['latencyP2'], data['latencyN2'], data['latencyP300'],
            data['ampN1P2'], data['ampP2N2'], data['ampN2P3'],
            datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'P300 data submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/submit_caft', methods=['POST'])
def submit_caft():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO caft_data (
                patient_id, patient_name, max_rr_mean, min_rr_mean,
                ei_ratio_mean, basal_dbp, final_dbp, dbp_change,
                timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['patientId'], data['patientName'], data['maxRRMean'],
            data['minRRMean'], data['eiRatioMean'], data['basalDBP'],
            data['finalDBP'], data['dbpChange'], datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'CAFT data submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/submit_biomarkers', methods=['POST'])
def submit_biomarkers():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO biomarkers_data (
                patient_id, patient_name, serum_icam, serum_vcam,
                serum_eselectin, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            data['patientId'], data['patientName'], data['serumICAM'],
            data['serumVCAM'], data['serumESelectin'], datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'Biomarkers data submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)