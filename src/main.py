from flask import Flask, request, jsonify
import traceback
from environment import DEBUG_MODE
from components import Loader, Runner, Sender, logger
from exceptions import AlgorithmException

app = Flask(__name__)


@app.route("/v1/run", methods=["POST"])
def run_algorithm():
    if DEBUG_MODE:
        logger.info("Running in debug mode")

    try:
        logger.info("start")

        # Initiate components
        loader = Loader()
        runner = Runner(loader)
        sender = Sender(runner)

        # Read config JSON from POST body
        config = request.get_json(force=True)
        loader.set_input(config)

        # Prepare the module
        loader.load()

        # Run the module
        runner.run()

        logger.info("result: OK")
        return sender.send_success()

    except AlgorithmException as e:
        logger.error(
            "result: AlgorithmException", {"exception": traceback.format_exc()}
        )
        return sender.send_mixed(e)

    except Exception as e:  # pylint: disable=broad-except
        logger.error("result: Exception", {"exception": traceback.format_exc()})
        return sender.send_error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
