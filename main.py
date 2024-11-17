from communication.api.rest_api_server import RestApiServer
from communication.web.web_server import WebServer
from communication.mqtt.mqtt_data_fetcher import MqttDataFetcher
from application.core_manager import CoreManager
from data.data_manager import DataManager

API_CONFIG_FILE = "config/api_conf.yaml"
WEB_CONFIG_FILE = "config/web_conf.yaml"
MQTT_CONFIG_FILE = "config/mqtt_fetcher_conf.yaml"

if __name__ == '__main__':

    # Data Manager initialization
    data_manager = DataManager()

    # Create the Core Manager with the Data Manager reference
    core_manager = CoreManager(data_manager)

    # Create RESTful API Server
    rest_api_server = RestApiServer(API_CONFIG_FILE, core_manager)

    # Run RESTful API Server
    rest_api_server.start()

    # Create Web Server
    web_server = WebServer(WEB_CONFIG_FILE, core_manager)

    # Run Web Server
    web_server.start()

    # Create MQTT Data Fetcher
    mqtt_data_fetcher = MqttDataFetcher(MQTT_CONFIG_FILE, core_manager)

    # Run MQTT Data Fetcher
    mqtt_data_fetcher.start()