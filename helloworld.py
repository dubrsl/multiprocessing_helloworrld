import multiprocessing

from services import (
    database_service
)

from utils.configs import (
    DATABASE_EDIT_QUEUE,
    DATABASE_RESPONSE_QUEUE
)

multiprocessing.set_start_method("spawn", force=True)

database_writer_service = multiprocessing.Process(
    target=database_service.database_writer, args=(
        DATABASE_EDIT_QUEUE, DATABASE_RESPONSE_QUEUE)
)

print("Hello World")
