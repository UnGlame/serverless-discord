import json
import os

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

public_key = os.getenv("PUBLIC_KEY")
region = os.getenv("REGION")
instance_id = os.getenv("INSTANCE_ID")

region = "ap-southeast-1"
instances = [instance_id]
ec2_client = boto3.client("ec2", region_name=region)
ec2_resource = boto3.resource("ec2", region_name=region)


def lambda_handler(event, context):
    try:
        # Get event data
        body = json.loads(event["body"])
        signature = event["headers"]["x-signature-ed25519"]
        timestamp = event["headers"]["x-signature-timestamp"]

        # Validate the interaction
        verify_key = VerifyKey(bytes.fromhex(public_key))

        message = timestamp + event["body"]

        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {"statusCode": 401, "body": json.dumps("invalid request signature")}

        # Handle the interaction
        t = body["type"]

        if t == 1:
            return {"statusCode": 200, "body": json.dumps({"type": 1})}
        elif t == 2:
            return command_handler(body)
        else:
            return {"statusCode": 400, "body": json.dumps("unhandled request type")}
    except:
        raise


def command_handler(body):
    command = body["data"]["name"]

    if command == "dststart":
        if not is_instance_stopped():
            return write_response("DST server instance is still running!")

        ec2_client.start_instances(InstanceIds=instances)
        print("Start instances: " + str(instances))

        return write_response("Started DST server instance!")

    if command == "dststop":
        if not is_instance_running():
            return write_response("DST server instance is not running!")

        ec2_client.stop_instances(InstanceIds=instances)
        print("Stopped instances: " + str(instances))

        return write_response("Stopped DST server instance!")

    if command == "dstsave":
        if not is_instance_running():
            return write_response("DST server instance is not running!")

        ssm_client = boto3.client("ssm")
        command = "bash -c /home/steam/steamapps/DST/save_dedicated_servers.sh"
        commands = [command]

        response = ssm_client.send_command(
            InstanceIds=instances,
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": commands},
        )

        command_id = response["Command"]["CommandId"]
        print(f"Command {command_id} called successfully: '{command}'")

        return write_response("Saving DST server.")

    return write_response(400, f"unhandled command: {command}")


def is_instance_running() -> bool:
    instance = ec2_resource.Instance(instance_id)
    return instance.state["Name"] == "running"


def is_instance_stopped() -> bool:
    instance = ec2_resource.Instance(instance_id)
    return instance.state["Name"] == "stopped"


def write_response(content: str, status_code: int = 200):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "type": 4,
                "data": {
                    "content": content,
                },
            }
        ),
    }
