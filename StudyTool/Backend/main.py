from flask import Flask, request, jsonify, send_from_directory
from autogen import UserProxyAgent, AssistantAgent

app = Flask(__name__, static_folder="../Frontend", static_url_path="")

# Below is the config used to defined the model used for autogen
# I am running a local LLM on my device to there is not API key
# Replace the config paramaters if you wish to run a different model
llm_config = {
    "config_list": [
        {
            "model": "mistral",
            "base_url": "http://localhost:11434/v1",
            "api_key": "NULL"
        }
    ]
}

# Initialise the assistant and user agent.
# Assistant agent is used to process user input with the LLM along with proving a response from the LLM
# User agent handles the input from the user.
tutor_agent = AssistantAgent(
    name="LocalTutor",
    llm_config=llm_config,
    system_message="You are a helpful and concise study assistant. Answer questions clearly and thoroughly.",
)

user = UserProxyAgent(
    name="Student",
    code_execution_config=False
)

# Initialise the web app.
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    print(f"User said: {user_message}")

    try:
        latest_message = ""

        # Use the collect_reply function to capture the response
        def collect_reply(recipient, messages, sender, config):
            nonlocal latest_message
            latest_message = messages[-1]['content']  # Get the latest assistant response

        # Register the reply function
        user.register_reply(
            tutor_agent,
            reply_func=collect_reply,
            config={"callback": None},
        )
        # Initiate the chat with the user input
        try:
            user.initiate_chat(tutor_agent, message=user_message, clear_history=True)
        except Exception as e:
            print("Error during initiate_chat:", e)
        # Return the assistant's reply to frontend
        return jsonify({"response": latest_message})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "An error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
