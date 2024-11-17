from application.core_manager import CoreManager
from communication.dto.telemetry_message import TelemetryMessage
import json
import paho.mqtt.client as mqtt
import yaml
import os
import threading

class MqttDataFetcher:
    """ MQTT Data Fetcher Class in charge of fetching data from the MQTT Broker
    The fetcher is executed in a separate thread in order to avoid blocking the main thread.
    Uses a configuration file to read the MQTT Broker configuration and username/password information."""

    def __init__(self, config_file: str, core_manager: CoreManager):

        # Fetcher Thread
        self.fetcher_thread = None

        # MQTT Client Initialization to None
        self.client = None

        # Configuration File Path
        self.config_file = config_file

        # Data Manager
        self.core_manager = core_manager

        # Default Configuration Dictionary
        self.configuration_dict = {
            "broker_ip": "127.0.0.1",
            "broker_port": 1883,
            "target_telemetry_topic": "device/+/temperature",
            "username": None,
            "password": None
        }

        # Read Configuration from target Configuration File Path
        self.read_configuration_file()

        # MQTT Broker Configuration
        self.mqtt_broker_host = self.configuration_dict["broker_ip"]
        self.mqtt_broker_port = self.configuration_dict["broker_port"]
        self.mqtt_topic = self.configuration_dict["target_telemetry_topic"]
        self.mqtt_username = self.configuration_dict["username"]
        self.mqtt_password = self.configuration_dict["password"]

        # Initialize MQTT Client
        self.init_mqtt_client()

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

    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server."""
        print("Connected to MQTT Broker with result code " + str(rc))
        self.client.subscribe(self.mqtt_topic)
        print(f"Subscribed to topic: {self.mqtt_topic}")

    def on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server."""

        if mqtt.topic_matches_sub(self.mqtt_topic, msg.topic):
            try:

                # Decode the payload
                payload = msg.payload.decode()

                # Get JSON data from the message payload
                json_data = json.loads(payload)

                # Extract the device ID from the topic
                device_id = msg.topic.split('/')[1]

                # Deserialize the payload into a TelemetryMessge object
                telemetry_message = TelemetryMessage(**json_data)

                # Update the data manager with the new data
                print(f"Received message from device {device_id}: {payload}")

                # Handle the telemetry message
                self.core_manager.handle_mqtt_device_telemetry_data(device_id, telemetry_message)

            except Exception as e:
                print(f"Error processing MQTT message: {str(e)}")

    def init_mqtt_client(self):
        """ Initialize the MQTT Client
        :return:
        """

        # Create MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        """ Connect to the MQTT Broker and start the loop """

        # Check if username and password are provided
        if self.mqtt_username and self.mqtt_password:
            print("Setting username and password ...")
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)

        # Connect to MQTT Broker
        print("Connecting to MQTT Broker ...")
        self.client.connect(self.mqtt_broker_host, self.mqtt_broker_port, 60)

        # Start the MQTT loop
        print("Starting MQTT Loop ...")
        self.client.loop_forever()

    def start(self):
        # Define a new thread for the fetcher associated to the execution of the connect method
        self.fetcher_thread = threading.Thread(target=self.connect)

        # Start the fetcher thread
        self.fetcher_thread.start()
