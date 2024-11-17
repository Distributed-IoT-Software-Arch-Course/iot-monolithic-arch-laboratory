from flask_restful import Resource, reqparse
from application.core_manager import CoreManager

class TelemetryDataResource(Resource):
    """Resource to handle the Telemetry Data of a specific Device"""

    def __init__(self, **kwargs):
        # Inject the CoreManager instance
        self.core_manager: CoreManager = kwargs['core_manager']

    def get(self, device_id):
        """GET Request to retrieve the Telemetry Data of a target device"""

        device_telemetry_data = self.core_manager.get_telemetry_data_by_device_id(device_id)

        if device_telemetry_data is not None:
            result_location_list = []

            # Iterate over the telemetry data to build a serializable telemetry data list
            # transforming the telemetry data into a dictionary. Then it will be Flask to serialize it into JSON
            for telemetry_data in device_telemetry_data:
                result_location_list.append(telemetry_data.__dict__)

            return result_location_list, 200  # return data and 200 OK code
        else:
            return {'error': "Device Not Found !"}, 404
