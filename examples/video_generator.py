# add base path to sys.path
import os, sys
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from framework.service.generator import Generator
import cv2
from .video_task import VideoTask
from framework.message_queue.mqtt import MqttPublisher
import json
import base64
import time

class VideoGenerator(Generator):
    def __init__(self, data_source, id, mq_topic, priority, tuned_parameters,
                 mqtt_host='localhost', mqtt_port=1883, mqtt_username='admin', 
                 mqtt_password='admin'):
        super().__init__(data_source, id, mq_topic, priority, tuned_parameters)
        mqtt_client_id=str(id)
        self.publisher = MqttPublisher(mqtt_host, mqtt_port, mqtt_username, mqtt_password, mqtt_client_id)
        self._data_source = cv2.VideoCapture(data_source)

    @classmethod
    def generator_type(cls) -> str:
        return 'video'

    @classmethod
    def generator_description(cls) -> str:
        return 'Video generator'

    def get_data_source(self) -> object:
        return self._data_source

    def get_id(self) -> str:
        return self._id
    
    def get_mq_topic(self) -> str:
        return self._mq_topic

    def get_priority(self) -> int:
        return self._priority
    
    def set_priority(self, priority: int):
        self._priority = priority

    def get_tuned_parameters(self) -> dict:
        return self._tuned_parameters
    
    def set_tuned_parameters(self, tuned_parameters: dict):
        self._tuned_parameters = tuned_parameters

    def send_task_to_mq(self, task: VideoTask):
        self.publisher.publish(self._mq_topic, json.dumps(task.serialize()))

    def run(self):
        # import random
        # while True:
        #     random_num = random.randint(0, 100)
        #     yield random_num
        self.publisher.client.loop_start()
        id = 0
        while True:
            # ret, frame = self._data_source.read()
            # if not ret:
            #     break
            # base64_frame = base64.b64encode(frame).decode('utf-8')
            # task = VideoTask(base64_frame, id, self._id, self._priority)
            import random
            random_num = random.randint(0, 100)
            task = VideoTask(random_num, id, self._id, self._priority)
            self.send_task_to_mq(task)
            id += 1
            time.sleep(5)


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Video generator')
    parser.add_argument('--id', type=str, help='generator id')
    id = parser.parse_args().id
    generator = VideoGenerator(0, f'generator_{id}',
                                'testapp/generator', 0, {})
    generator.run()

