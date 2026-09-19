import logging

FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure_logging(level: str) -> None:
    # force=True: Granian успевает поставить свои хендлеры до старта приложения
    logging.basicConfig(format=FORMAT, level=level.upper(), force=True)
