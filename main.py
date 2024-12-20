import dotenv
import os
import warnings
import logging
from src.yolov5_inference import VehicleDetector

warnings.simplefilter("ignore", category=FutureWarning)
dotenv.load_dotenv()

# Set up logging configuration
def setup_logging(level=logging.INFO):
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    return logger

logger = setup_logging()  # Default to INFO level 

MODEL = str(os.getenv("MODEL", "models/yolov5m.torchscript")) 
CONF = float(os.getenv("CONF", 0.5))
IOU = float(os.getenv("IOU", 0.45))
QSIZE = int(os.getenv("QSIZE", 500))
DEVICE = str(os.getenv("DEVICE", "cpu"))
SHOW = bool(int(os.getenv("SHOW", 1)))
TRACKING = bool(int(os.getenv("TRACKING", 0)))
DEBUG = bool(int(os.getenv("DEBUG", 0)))
RTSP_URLS = os.getenv("RTSP_URLS", "data/video/Khao-Chi-On_CCTV34R.mp4").split(",")
CLASSES = os.getenv("CLASSES", "car").split(",")

if __name__ == "__main__":
    detector = VehicleDetector(
        rtsp_urls=RTSP_URLS, model_path=MODEL, conf=CONF, iou_thres=IOU,
        queue_size=QSIZE, device=DEVICE, yaml_path="yolov5/data/coco.yaml"
    )
    detector.define_classes(classes=CLASSES)
    detector.init_parked_detector(dist_sencitivity=5, time_limit_sec=0.25)
    detector.run(show=SHOW, tracking=TRACKING, debug=DEBUG)  # Set debug=True to show detailed logs