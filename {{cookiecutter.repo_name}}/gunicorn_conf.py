import multiprocessing

bind = '0.0.0.0:5000'
if multiprocessing.cpu_count() * 4 + 1 < 25:
    workers = multiprocessing.cpu_count() * 4 + 1
else:
    workers = 25
pid = 'LOCATION_OF_SERVER/gunicorn.pid'
