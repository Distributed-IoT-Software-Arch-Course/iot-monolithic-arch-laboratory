from communication.dto.telemetry_message import TelemetryMessage
from data.data_manager import DataManager

class CoreManager:
    """
    Core Manager class that handles the core functionality of the application
    Main methods re-call the data manager methods to decouple the core functionality from the data management
    Additional dedicated methods are used to handle telemetry data from devices with a specific application logic
    """

    def __init__(self, data_manager: DataManager):
        """Initialize the CoreManager with a Data Manager"""
        self.data_manager = data_manager

    def handle_mqtt_device_telemetry_data(self, device_id: str, device_telemetry_data: TelemetryMessage):
        """ Handle telemetry data from device """

        # Check request not None and instance of TelemetryMessage
        if device_telemetry_data is None or not isinstance(device_telemetry_data, TelemetryMessage):
            raise ValueError("Invalid TelemetryMessage")
        else:
            self.data_manager.add_device_telemetry_data(device_id, device_telemetry_data)
            print(f'Telemetry data received from device {device_id}')

    def get_telemetry_data_by_device_id(self, device_id: str):
        """
        Get telemetry data by device id from data manager
        :param device_id: Device id associated with telemetry data
        :return: List of telemetry data
        """
        return self.data_manager.get_telemetry_data_by_device_id(device_id)
