from flask import Flask, request, jsonify

app = Flask(__name__)

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

#       REORDERING DOES NOT WORK!
#        # Rearrange the fields to match the desired order
#        ordered_cloud_event = {
#            "specversion": cloud_event["specversion"],
#            "type": cloud_event["type"],
#            "source": cloud_event["source"],
#            "id": cloud_event["id"],
#            "time": cloud_event["time"],
#            "data": cloud_event["data"]
#        }

        # Return the transformed payload
        return jsonify(cloud_event), 200

    except KeyError as e:
        error_message = f"Missing required field: {str(e)}"
        return jsonify({"error": error_message}), 400

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run()
