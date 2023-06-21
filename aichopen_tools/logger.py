import logging
import os
import sys
from datetime import datetime


class LevelFilter(logging.Filter):
    def __init__(self, low=logging.DEBUG, high=logging.CRITICAL):
        '''
            Filters by logging level

        Args:
            low : Lowest passing level (** Included **)
            high : Highest passing level (** Included **)
        '''
        self._low = low
        self._high = high
        logging.Filter.__init__(self)

    def filter(self, record):
        return self._low <= record.levelno <= self._high


class LoggerFactory:
    output_files = []
    
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    CRITICAL = logging.CRITICAL
    
    min_stdout = logging.DEBUG
    max_stdout = logging.INFO
    min_stdoerr = logging.WARN
    max_stdoerr = logging.CRITICAL
    terminal_format_str = '%(asctime)s %(levelname)s - %(message)s [%(filename)s:%(lineno)s]'  # '%(levelname)-7s   %(message)s'
    file_format_str = '%(asctime)s %(levelname)s - %(message)s \t[%(filename)s:%(lineno)s]'
    replaced = []  # will hold a list of replaced files to prevent double erasing
    setup_loggers = []  # List of already setup loggers to prevent duplcate handlers

    @classmethod
    def add_output_file(cls, output_file, min_level=logging.INFO, max_level=logging.CRITICAL, mode='append'):
        '''
            Adds an additional output file. With a level filter (min and max_level INCLUDED)
            relative paths are relative to working directory

            Args:
                mode: 'append' or 'replace' (reset will delete the file if it exists)
        '''
        cls.output_files.append((output_file, min_level, max_level, mode))

    @classmethod
    def set_stdout_level_filter(cls, min_level=logging.DEBUG, max_level=logging.INFO):
        '''
            Set custom filter level for the stdout handler.
            Messages with min_level <= levels <= max_level will be displayed on stdout

        Args:
            min_level (_type_, optional): Minimal level to display on stdout (Included). Defaults to logging.DEBUG.
            max_level (_type_, optional): Maximal level to display on stdout (Included). Defaults to logging.INFO.
        '''
        cls.min_stdout = min_level
        cls.max_stdout = max_level

    @classmethod
    def set_stderr_level_filter(cls, min_level=logging.WARN, max_level=logging.CRITICAL):
        '''
            Set custom filter level for the stderr handler.
            Messages with min_level <= levels <= max_level will be displayed on stderr

        Args:
            min_level (_type_, optional): Minimal level to display on stderr (Included). Defaults to logging.WARN.
            max_level (_type_, optional): Maximal level to display on stderr (Included). Defaults to logging.CRITICAL.
        '''
        cls.min_stderr = min_level
        cls.max_stderr = max_level

    @classmethod
    def set_terminal_format_string(cls, terminal_format_string):
        cls.terminal_format_str = terminal_format_string

    @classmethod
    def set_file_format_string(cls, file_format_string):
        cls.file_format_str = file_format_string

    @classmethod
    def setup_logger(cls, logger: logging.Logger) -> logging.Logger:
        log_output_formatter = logging.Formatter(cls.file_format_str)
        log_std_formatter = logging.Formatter(cls.terminal_format_str)

        stdout_stream_handler = logging.StreamHandler(sys.stdout)
        stdout_stream_handler.setLevel(logging.DEBUG)
        stdout_stream_handler.addFilter(LevelFilter(logging.DEBUG, logging.INFO))
        stdout_stream_handler.setFormatter(log_std_formatter)
        logger.addHandler(stdout_stream_handler)

        stderr_stream_handler = logging.StreamHandler(sys.stderr)
        stderr_stream_handler.setLevel(logging.WARNING)
        stderr_stream_handler.addFilter(LevelFilter(logging.WARN, logging.CRITICAL))
        stderr_stream_handler.setFormatter(log_std_formatter)
        logger.addHandler(stderr_stream_handler)

        for (file, min_level, max_level, mode) in cls.output_files:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            if mode == 'replace' and file not in cls.replaced and os.path.exists(file):
                os.remove(file)
                cls.replaced.append(file)
            file_handler = logging.FileHandler(file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(log_output_formatter)
            file_handler.addFilter(LevelFilter(min_level, max_level))
            logger.addHandler(file_handler)

        return logger

    @classmethod
    def get_logger(cls, name='sagemaker_pipelines', level=logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)

        if name in cls.setup_loggers:
            logger.setLevel(level)
            return logger

        logger.propagate = False
        logger = cls.setup_logger(logger)
        logger.setLevel(level)
        cls.setup_loggers.append(name)
        return logger


# We add a timestamped log
log_folder = os.path.join(os.path.join(".logs", datetime.now().strftime("%Y%m%dT%H%M%S") + ".log"))
os.makedirs(log_folder, exist_ok=True)
LoggerFactory.add_output_file(output_file=os.path.join(log_folder, "Latest_ERRORS.log"), min_level=logging.WARN,
                              max_level=logging.CRITICAL, mode='replace')
LoggerFactory.add_output_file(output_file=os.path.join(log_folder, "Latest.log"), min_level=logging.DEBUG,
                              max_level=logging.CRITICAL, mode='replace')
LoggerFactory.add_output_file(output_file=os.path.join(log_folder, "Debug.log"), min_level=logging.DEBUG,
                              max_level=logging.CRITICAL, mode='append')
