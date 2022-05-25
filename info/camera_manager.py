import requests

import flags


class CameraManager:
    def __init__(self, camera_url):
        self.camera_url = camera_url
        requests.post(self.camera_url + "/api/initialize", json={"device_id": "0"})

    def update_position(self):
        response = requests.get(self.camera_url + "/api/position")
        print(response.json()['message'])
        if flags.SIDE == "PURPLE":
            for number in response.json()['message']:
                if response.json()['message'][number]['id'] in range(1, 5):
                    print("Youhou")
        elif flags.SIDE == "YELLOW":
            for number in response.json()['message']:
                if response.json()['message'][number]['id'] in range(6, 10):
                    print(number)

    # def update_flags(self):



if __name__ == "__main__":
    cm = CameraManager("http://192.168.169.178:5000")
    print(cm.update_position())
