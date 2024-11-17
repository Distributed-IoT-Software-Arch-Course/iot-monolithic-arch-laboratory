from flask import Flask, request
from flask_restful import Api
from application.core_manager import CoreManager
from communication.api.resources.telemetry_data_resource import TelemetryDataResource
import threading
import yaml
import os

class RestApiServer:
    """
    RESTful API Server designed to manage the Inventory of IoT Devices
    """

    # Default Endpoint Prefix
    DEFAULT_ENDPOINT_PREFIX = "/api/iot/inventory"

    def __init__(self, config_file: str, core_manager: CoreManager):

        # Initialize REST API Server and Flask Application to None
        # They will be initialized in the init_rest_api method
        self.api = None
        self.app = None

        # Server Thread
        self.server_thread = None

        # Configuration File Path
        self.config_file = config_file

        # Data Manager
        self.core_manager = core_manager

        # Set a default configuration
        self.configuration_dict = {
            "rest":{
                "api_prefix": self.DEFAULT_ENDPOINT_PREFIX,
                "host": "0.0.0.0",
                "port": 7070
            }
        }

        # Read Configuration from target Configuration File Path
        self.read_configuration_file()

        # Initialize REST API
        self.init_rest_api()

    def read_configuration_file(self):
        """ Read Configuration File for the REST API Server
         :return:
        """

        # Get the main communication directory
        main_app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construct the file path
        file_path = os.path.join(main_app_path, self.config_file)

        with open(file_path, 'r') as file:
            self.configuration_dict = yaml.safe_load(file)

        print("Read Configuration from file ({}): {}".format(self.config_file, self.configuration_dict))

    def init_rest_api(self):
        """ Initialize REST API with resources and endpoints
        :return:
        """

        # Create a new Flask Application and the REST API from Flask Restful
        self.app = Flask(__name__)
        self.api = Api(self.app)

        # Add Resources and Endpoints
        self.api.add_resource(TelemetryDataResource, self.configuration_dict['rest']['api_prefix'] + '/device/<string:device_id>/telemetry',
                              resource_class_kwargs={'core_manager': self.core_manager},
                              endpoint="device_telemetry_data",
                              methods=['GET'])

    def run_server(self):
        """ Start the REST API Server """
        self.app.run(host=self.configuration_dict['rest']['host'], port=self.configuration_dict['rest']['port'])

    def start(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def stop(self):
        """ Stop the REST API Server (Flask Method)
        In this code, request.environ.get('werkzeug.server.shutdown')
        retrieves the shutdown function from the environment.
        If the function is not found, it raises a RuntimeError,
        indicating that the server is not running with Werkzeug.
        If the function is found, it is called to shut down the server."""

        # Shutdown the server
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        # Call the shutdown function
        func()

        # Wait for the server thread to join
        self.server_thread.join()