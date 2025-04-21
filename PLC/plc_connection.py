from pymodbus.client import ModbusTcpClient as mbc
from pymodbus.exceptions import ConnectionException

connect_status = False

class PLCConnection:
    global connect_status
    def __init__(self, host='192.168.0.1', port=502):
        self.host = host
        self.port = port
        self.client = mbc(host = self.host, port = self.port)
        self.UNIT = 0x1
    def connectPLC(self):
        try:
            connect_status = self.client.connect()
            print(connect_status)
            print(f"Connected to PLC at {self.host}:{self.port}")
        except ConnectionException as e:
            print(f"Failed to connect to PLC: {e}")
    def write(self, address, value):
        if connect_status:
            self.client.write_register(address, value, unit=self.UNIT)
    def read(self, address, count=1):
        if connect_status:
            result = self.client.read_holding_registers(address, count, unit=self.UNIT)
            return result.registers if result.isError() == False else None
    def disconnectPLC(self):
        self.client.close()

PLCConnection().connectPLC()