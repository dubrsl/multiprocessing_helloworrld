import asyncio
import asyncio.tasks
import multiprocessing
from datetime import datetime, timedelta

multiprocessing.set_start_method("spawn", force=True)

DATABASE_EDIT_QUEUE: multiprocessing.Queue = multiprocessing.Queue()
DATABASE_RESPONSE_QUEUE: multiprocessing.Queue = multiprocessing.Queue()

DATE_TIME_ANALYTICS_FORMAT = "%Y-%m-%dT%H:%M:%S"
RECORDS_PER_PAGE_LIMIT = 25
SELECTION_START_DATE = datetime(2022, 1, 1)

DEFAULT_UPDATE_TIME_SECONDS = 0.5
NEAR_ZERO = 1e-7

MAX_INTERSECTION_TO_RECEIVER_DISTANCE = 100000  # meters
MAX_AGE = 5000

SINGLE_RECEIVER_INTERSECT_INTERVAL = 120000  # milliseconds

MINIMUM_DISTANCE_FOR_SELF_INTERSECTION = 500.0  # meters
MINIMUM_RELATIVE_ANGLE_FOR_INTERSECTION = 5.0  # degrees

NUM_LOBS_FOR_STATISTICS = 5

STABLE_BEARING_STD_THRESHOLD = 5  # degrees

# Use this variable in case of invalid snr was gotten
REALLY_SMALL_SNR = -1000
MIN_SNR_FOR_LOGGING = -2.0  # dB
MIN_SNR_FOR_INTERSECTION = 0.0  # dB
DEFAULT_SNR_FOR_COMPATIBILITY = 0.0  # dB

SEC_TO_MSEC = 1000.0

TWO_DAYS_MILLISECONDS = timedelta(days=1).total_seconds() * SEC_TO_MSEC
R_TWO_DAYS_MILLISECONDS = 1.0 / TWO_DAYS_MILLISECONDS

MAX_REQUEST_TRIES = 150
RETRY_SLEEP_TIME_S = 10e-3

CLUSTERING_MAX_RUNTIME_S = 20.0
CLUSTERING_INTERVAL_S = 30

# TODO(Микола): в ідеалі, це значення повинно приходити з сенсору, а не бути фікосваним в агрегаторі
KRAKENSDR_FREQUENCY_STABILITY_PPM = 1.0
KRAKENSDR_FREQUENCY_STABILITY_RELATIVE = KRAKENSDR_FREQUENCY_STABILITY_PPM * 1e-6

DEFAULT_SETTINGS = {
    "eps": 1500.0,
    "min_samp": 10,
    "max_cluster_dimension": 25000.0,
    "min_conf": 3,
    "min_snr": 0.0,
    # start_time in milliseconds (3 days back from current time)
    "start_time": int((datetime.now() - timedelta(days=3)).timestamp() * SEC_TO_MSEC),
    "is_clustering": True,
    "is_hq_rendering": False,
    "is_receiving": True,
    "is_plot_intersects": True,
    "is_intersects_clusterization": False,
    "is_pins_clusterization": False,
    "intersects_pixel_range": 10,
    "intersects_minimum_cluster_size": 3,
}
SENSOR_DATA_REQUEST_TIMEOUT = 2  # seconds
RECEIVER_SETTINGS_REQUEST_TIMEOUT = 2  # seconds

GROUP_DEFAULT_ID = "3d4e5d91507847cfa7286900001b4e36"
GROUP_DEFAULT_NAME = "Default"
GROUP_DEFAULT_COLOR = "#99c1f1"
GROUP_ID_COLUMN_VALUE = f"VARCHAR(32) DEFAULT '{GROUP_DEFAULT_ID}'"

SDR_ONLINE_VIEW_BANDWIDTH_MHZ = 2.4
SDR_HEADROOM_BANDWIDTH = 0.9

sensors_loggers: set[asyncio.tasks.Task] = set()

rotator_mqtt_tasks_map: dict[str, asyncio.tasks.Task] = {}
tsukorok_mqtt_tasks_map: dict[str, asyncio.tasks.Task] = {}
control_panel_mqtt_tasks_map: dict[str, asyncio.tasks.Task] = {}

HZ_TO_MHZ = 1.0e-6
MHZ_TO_HZ = 1 / HZ_TO_MHZ

DOA_MAX_REQUESTS_FOR_STATUS_ERROR = 2  # times
STATUS_MAX_REQUESTS_FOR_STATUS_ERROR = 5  # times

DATABASE_CACHE_SIZE_KB = 10000

GLOBAL_SETTINGS_DEFAULT_UUID = "de795742d6d94691af43a6aa1173315c"
CLUSTER_NUM_STD_DIMENSION_FACTOR = 3.0

DEFAULT_RECEIVER_ANTENNA_HEIGHT_AGL_M = 5
SPLAT_DEFAULT_CALCULATION_RADIUS_KM = MAX_INTERSECTION_TO_RECEIVER_DISTANCE // 1000
SPLAT_DEFAULT_TARGET_ANTENNA_HEIGHT_AGL_M = 10

PROXY_DATA_REQUEST_TIMEOUT = 5  # seconds
