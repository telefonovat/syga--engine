import resource
from flask import Flask, request, jsonify
from multiprocess import Process, Manager
import traceback
from environment import DEBUG_MODE
from components import Loader, Runner, Sender, logger
from exceptions import AlgorithmException

app = Flask(__name__)

# Limits
MAX_MEMORY_MB = 1024
MAX_EXECUTION_TIME_SECOND = 4


def algorithm_worker(namespace, config):
    resource.setrlimit(
        resource.RLIMIT_AS, (MAX_MEMORY_MB * 1024 * 1024, MAX_MEMORY_MB * 1024 * 1024)
    )
    loader = Loader()
    runner = Runner(loader)

    try:
        loader.set_input(config)

        # Prepare the module
        loader.load()

        # Run the module
        runner.run()

        namespace.runner = runner
    except Exception as e:
        namespace.exception = e


@app.route("/v1/run", methods=["POST"])
def run_algorithm():
    if DEBUG_MODE:
        logger.info("Running in debug mode")

    sender = Sender(None)
    try:
        logger.info("start")

        config = request.get_json(force=True)

        runner = None
        with Manager() as manager:
            namespace = manager.Namespace()
            namespace.runner = Runner(None)
            namespace.exception = None

            p = Process(target=algorithm_worker, args=(namespace, config))
            p.start()
            p.join(timeout=MAX_EXECUTION_TIME_SECOND)

            if p.is_alive():
                p.terminate()
                raise Exception(
                    "Your code exceeded the allowed time limit to execute.\
                    You have probably have some infinite loop or similar."
                )
            elif p.exitcode < 0:
                raise Exception(
                    "Your code execution was terminated midway.\
                    You most likely exceeded the memory limit."
                )
            elif namespace.exception is not None:
                # Exception from loader and runner
                raise namespace.exception

            runner = namespace.runner
        if runner is None:
            raise Exception("Runner is None. Something horrible went wrong.")
        else:
            sender._runner = runner
        logger.info("result: OK")
        return sender.send_success()

    except AlgorithmException as e:
        logger.error(
            "result: AlgorithmException", {"exception": traceback.format_exc()}
        )
        return sender.send_error(e)

    except Exception as e:  # pylint: disable=broad-except
        logger.error("result: Exception", {"exception": traceback.format_exc()})
        return sender.send_error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
