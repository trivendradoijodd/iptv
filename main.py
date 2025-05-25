from utils.serve import run_server
from utils.driver import driver


m3u_link = driver();

if m3u_link:
    run_server(8123, 'outputs/output.m3u')
