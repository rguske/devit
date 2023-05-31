from flask import Flask, request, jsonify

app = Flask(__name__)

SINKBINDING_ENDPOINT = "http://rabbitmq-broker-broker-ingress.vmware-functions.svc.cluster.local"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Receive the JSON payload
    payload = request.json

    try:
        # Perform field mapping for CloudEvent.io compliance
        cloud_event = {
            "specversion": "1.0",
            "type": "asop.openc2.event."f"{payload['action']}.v0",
            "source": f"{payload['actuator']['veba']['hostname']}",
            "id": payload["command_id"],
            "time": "2023-05-30T12:00:00Z",
            "data": {
                "action": payload["action"],
                "target": {
                    "device": {
                        "hostname": payload["target"]["device"]["hostname"]
                    }
                },
                "actuator": {
                    "veba": {
                        "hostname": payload["actuator"]["veba"]["hostname"]
                    }
                },
                "args": {
                    "logical-switch-name": payload["args"]["logical-switch-name"]
                },
                "command_id": payload["command_id"]
            }
        }

        # Return the transformed payload
        return jsonify(cloud_event), 200

        # Send the CloudEvent payload to SinkBinding
        response = requests.post(SINKBINDING_ENDPOINT, json=cloud_event)

        if response.status_code == 200:
            return jsonify({"message": "CloudEvent payload sent to SinkBinding"}), 200
        else:
            return jsonify({"error": "Failed to send CloudEvent payload to SinkBinding"}), 500

    except KeyError as e:
        error_message = f"Missing required field: {str(e)}"
        return jsonify({"error": error_message}), 400

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run()
