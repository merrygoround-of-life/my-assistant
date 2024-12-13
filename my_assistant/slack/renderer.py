def create_block_section(text: str, accessory: dict=None):
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }
    if accessory:
        block = { **block, "accessory": accessory }
    return block

def create_block_action(elements: list[dict]):
    return {
        "type": "actions",
        "elements": elements
    }

def create_element_button(text: str, action_id: str, value: str):
    return {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": text
        },
        "action_id": action_id,
        "value": value
    }

def create_block_input(label: str, action_id: str, placeholder: str):
    return {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": action_id,
            "placeholder": {
                "type": "plain_text",
                "text": placeholder
            }
        },
        "block_id": action_id,
        "label": {
            "type": "plain_text",
            "text": label
        }
    }