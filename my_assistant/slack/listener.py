import os

from slack_bolt.async_app import AsyncApp as SlackApp

from my_assistant.slack.renderer import create_block_action, create_element_button, create_block_input

slack_app = SlackApp(token=os.environ.get("SLACK_BOT_TOKEN"))


@slack_app.event("app_mention")
async def get_user_id(body, say, logger):
    blocks = [
        create_block_input(":smiley: How can I help you?", "input", "Type here"),
        create_block_action([create_element_button("Chat", "chat", "chat")]),
        create_block_action([create_element_button("Translation", "translation", "translation")]),
        create_block_action([create_element_button("Git Commit Message", "gitlog", "gitlog")]),
        create_block_action([create_element_button("Paraphrase", "paraphrase", "paraphrase")]),
        create_block_action([create_element_button("Grammar", "grammar", "grammar")])
    ]
    await say(blocks=blocks)

@slack_app.action("chat")
async def chat(body, ack, say):
    await ack()
    user_input = body["state"]["values"]["input"]["input"]["value"]
    await say(f"Chat: {user_input}")

@slack_app.action("translation")
async def chat(body, ack, say):
    await ack()
    user_input = body["state"]["values"]["input"]["input"]["value"]
    await say(f"Translation: {user_input}")

@slack_app.action("gitlog")
async def chat(body, ack, say):
    await ack()
    user_input = body["state"]["values"]["input"]["input"]["value"]
    await say(f"Git Commit Message: {user_input}")

@slack_app.action("paraphrase")
async def chat(body, ack, say):
    await ack()
    user_input = body["state"]["values"]["input"]["input"]["value"]
    await say(f"Paraphrase: {user_input}")

@slack_app.action("grammar")
async def chat(body, ack, say):
    await ack()
    user_input = body["state"]["values"]["input"]["input"]["value"]
    await say(f"Grammar: {user_input}")