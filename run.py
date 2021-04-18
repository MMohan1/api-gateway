from optparse import OptionParser
from typing import NoReturn

import click

from rgate_app.api import rgate_app
from rgate_app.configmanager import YMLconfigReader

global REQUEST_STATE

REQUEST_STATE = {
    "request_count": {"success": 0, "error": 0},
    "latency_ms": {"average": 0, "p95": 0, "p99": 0},
    "requests_time": [],
}

rgate_app.REQUEST_STATE = REQUEST_STATE


def run_with_builtin(port: int, debug_mode: bool, config_file: str) -> NoReturn:
    """
    Run with default builtin flask/klein/bottle app
    """
    print(f"Built-in development server on port {port} ...")
    rgate_config = YMLconfigReader(config_file).read()
    rgate_app.config["RGATE_CONFIG"] = rgate_config
    rgate_app.run(host="0.0.0.0", port=port, debug=debug_mode)


def main() -> NoReturn:
    """
    Parse the options to get port and config file path"
    """
    parser = OptionParser(usage="%prog [options]  or type %prog -h (--help)")
    parser.add_option(
        "-c",
        "--config",
        dest="config_filename",
        default="config.yml",
        help="config file name",
        metavar="FILE",
    )
    parser.add_option(
        "--debug",
        help="When passed, sets app in debug mode",
        dest="debug_mode",
        action="store_true",
        default=False,
    )
    parser.add_option(
        "-p",
        "--port",
        dest="app_port",
        type="int",
        default=5000,
        help="Port on which to run service, default to 5000",
    )

    options, args = parser.parse_args()
    port = options.app_port
    config_file = options.config_filename
    debug_mode = options.debug_mode
    run_with_builtin(port, debug_mode, config_file)


if __name__ == "__main__":
    main()
