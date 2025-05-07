from plc_connection import PLCConnection
import time

connect_plc = PLCConnection(host='192.168.0.1')
connect_plc.connectPLC()

i = 0
try:
    while True:
        print(i)
        connect_plc.write(1, i)
        time.sleep(1)
        i += 1
except KeyboardInterrupt:
    print("\nInterrupted by user. Disconnecting...")
    connect_plc.disconnectPLC()


