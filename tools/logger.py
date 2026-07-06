import logging
import sys

def setup_logger(name: str = "job_matcher") -> logging.Logger:
    """
    Setup logger dengan format yang rapi: timestamp, level, pesan.
    
    Args:
        name: nama logger (biasanya nama module)
    
    Returns:
        instance logger yang siap dipakai
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:  # hindari duplikat handler kalau dipanggil berkali-kali
        return logger
    
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger