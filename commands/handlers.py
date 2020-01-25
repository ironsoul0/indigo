from commands.start import *
from commands.help import *
from commands.notify_lectures import *
from commands.unknown import *

handlers = [
  start_handler,
  help_handler,
  notify_lectures_handler,
  unknown_handler
]