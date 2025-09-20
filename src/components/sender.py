"""
The sender component
"""

import datetime
import traceback
import json
from src.environment import DEBUG_MODE
from src.engine.color import Color
from src.engine.node_shape import NodeShape
from src.engine.edge_shape import EdgeShape
from src.engine.stopwatch import Stopwatch
from .logger import logger
from .runner import Runner


class Sender:
    """
    Sender is used to send the result of the algorithm run. Provided frames are
    parsed before to make sure they can be JSON encoded
    """

    def _parse_custom_types(self, obj):
        """
        Recursively turns all instances of Color into RGB tuples
        """
        if isinstance(obj, NodeShape):
            return obj.shape

        if isinstance(obj, EdgeShape):
            return obj.shape

        if isinstance(obj, Color):
            return obj.to_hex()

        if isinstance(obj, list):
            for i in range(len(obj)):  # pylint: disable=consider-using-enumerate
                obj[i] = self._parse_custom_types(obj[i])

        elif isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._parse_custom_types(value)

        return obj

    def _send_response(self, res, err=None):
        """
        Sends the response to stdout

        parameters:
         - res (bool): Whether the run was successful
         - err (Exception): The exception thrown during preparation or execution
         - frames (list<Frame>): The list of generated frames (or an empty list)
        """
        try:
            stopwatch = Stopwatch().start()

            # Get ticks only in debug mode
            ticks = None
            if DEBUG_MODE:
                ticks = [dict(tick) for tick in self._runner.get_ticks()]

            # Get all frames as dicts
            frames = [dict(frame) for frame in self._runner.make_frames()]

            # Get engine logs only in debug mode
            # engine_logs = None
            # if DEBUG_MODE:
            #   engine_logs = self._runner.get_logs()

            self._parse_custom_types(frames)

            # Get elapsed times
            alg_time = self._runner.get_elapsed_time()
            parse_time = stopwatch.stop().elapsed
            elapsed = alg_time + parse_time

            logger.info("Sending {} response".format(res), {"res": res})
            logger.info(
                "Algorithm run in {:.6f} seconds".format(alg_time), {"time": alg_time}
            )
            logger.info(
                "Response prepared in {:.6f} seconds".format(parse_time),
                {"time": parse_time},
            )
            logger.info(
                "Everything took {:.6f} seconds".format(elapsed), {"time": elapsed}
            )

            return json.dumps(
                {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "res": res,
                    "err": None if err is None else str(err),
                    "alg_time": alg_time,
                    "parse_time": parse_time,
                    "elapsed": elapsed,
                    "frames": frames,
                    "ticks": ticks,
                    "engine_logs": None,  # temporarily disabled
                }
            )

        except Exception as sender_exception:  # pylint: disable=broad-except
            logger.error("Error in sender", {"error": traceback.format_exc()})

            return json.dumps(
                {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "res": "error",
                    "err": str(sender_exception),
                }
            )

    def send_error(self, err):
        """
        Sends an error response

        parameters:
          - err (Exception): The exception raised during preparation or execution
        """
        return self._send_response("error", err)

    def send_mixed(self, err):
        """
        Sends a mixed response

        parameters:
          - err (Exception): The exception raised during preparation or execution
        """
        return self._send_response("mixed", err)

    def send_success(self):
        """
        Sends a success response
        """
        return self._send_response("success")

    def __init__(self, runner: Runner):
        """
        Creates a new instance of Sender
        """
        self._runner = runner
