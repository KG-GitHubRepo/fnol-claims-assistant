def parse_runs(data):
    rows = []

    for run in data.get("runs", []):
        run_name = run.get("name", "")
        run_id = run_name.split("/")[-1]

        state = run.get("state", {})

        if "completed" in state:
            status = "Completed"
            output = state["completed"].get("outputs", {})
        elif "awaiting_guidance" in state:
            status = "Awaiting Guidance"
            output = {}
        else:
            status = "Running"
            output = {}

        user_inputs = run.get("user_inputs", {})

        subject = (
            user_inputs
            .get("subject", {})
            .get("text", "")
        )

        attachments = user_inputs.get("attachments", {})

        attachment_count = 0

        if "list" in attachments:
            attachment_count = len(
                attachments["list"].get("items", [])
            )
        elif "file" in attachments:
            attachment_count = 1

        rows.append({
            "Run ID": run_id,
            "Created Time": run.get("create_time", ""),
            "Status": status,
            "Version": run.get("stage_version", ""),
            "Trigger": run.get("invocation_details", {}).get(
                "invocation_source", ""
            ),
            "Subject": subject,
            "Attachments": attachment_count,
            "Output": output
        })

    return rows



def get_run_details(token, run_id):
    import requests

    ORG_ID = "xdk36l7E1GbrEvfvYWgdq"
    WORKSPACE_ID = "wPQCXTbwgibi9E4HknJTZ"
    AUTOMATION_ID = "mYAw57j8GrQR0ixlWtkUz"

    url = (
        f"https://app.us-1.kognitos.com/api/v1/"
        f"organizations/{ORG_ID}/"
        f"workspaces/{WORKSPACE_ID}/"
        f"automations/{AUTOMATION_ID}/"
        f"runs/{run_id}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return response.json()



def extract_claim_data(run_data):
    import re

    trigger_input = (
        run_data["executable_steps"]
        ["inputs"]
        ["trigger_input"]
        ["dictionary"]
        ["entries"]
    )

    email_value = trigger_input[0]["value"]
    email_entries = email_value["dictionary"]["entries"]

    email_data = {}

    for entry in email_entries:
        key = entry["key"]["text"]
        value = entry["value"]

        if "text" in value:
            email_data[key] = value["text"]
        else:
            email_data[key] = value

    body = email_data.get("body", "")

    def extract(pattern):
        match = re.search(pattern, body)
        return match.group(1).strip() if match else ""

    return {
        "FNOL Number": extract(r"(?m)^FNOL Number\s+(.+)$"),
        "Claimant": extract(r"(?m)^Claimant\s+(.+)$"),
        "Date of Injury": extract(r"(?m)^Date of Injury\s+(.+)$"),
        "Employer": extract(r"(?m)^Employer\s+(.+)$"),
        "Injury": extract(r"(?m)^Injury\s+(.+)$")
    }



def get_claim_runs(token, page_size=100):
    import requests

    ORG_ID = "xdk36l7E1GbrEvfvYWgdq"
    WORKSPACE_ID = "wPQCXTbwgibi9E4HknJTZ"
    AUTOMATION_ID = "mYAw57j8GrQR0ixlWtkUz"

    url = (
        f"https://app.us-1.kognitos.com/api/v1/"
        f"organizations/{ORG_ID}/"
        f"workspaces/{WORKSPACE_ID}/"
        f"automations/{AUTOMATION_ID}/runs"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    filter_expression = (
        'archived = "false" AND '
        'stage = "Draft" AND '
        'invocation_source != "INVOCATION_SOURCE_TEST"'
    )

    all_runs = []
    page_token = ""

    while True:

        params = {
            "page_size": page_size,
            "filter": filter_expression,
            "order_by": "create_time desc"
        }

        if page_token:
            params["page_token"] = page_token

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        all_runs.extend(
            data.get("runs", [])
        )

        page_token = data.get(
            "next_page_token",
            ""
        )

        if not page_token:
            break

    return {
        "runs": all_runs
    }
