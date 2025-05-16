from pymodbus.client.tcp import ModbusTcpClient as mbc
from pymodbus.exceptions import ConnectionException

class PLCConnection:
    def __init__(self, host='192.168.0.1', port=502):
        self.host = host
        self.port = port
        self.client = mbc(host=self.host, port=self.port)
        self.connect_status = False

    def connectPLC(self):
        try:
            self.connect_status = self.client.connect()
            print(self.connect_status)
            print(f"Connection to {self.host}:{self.port} is {'successful' if self.connect_status else 'failed'}")
            return self.connect_status
        except ConnectionException as e:
            print(f"Failed to connect to PLC: {e}")

    def write(self, address, value):
        if self.connect_status:
            # Không sử dụng 'unit' trong pymodbus 3.x
            self.client.write_registers(address, [value])  # Dùng write_registers thay vì write_register
        else:
            print("Not connected. Cannot write.")

    def read(self, address, count=1):
        if self.connect_status:
            # Không sử dụng 'unit' trong pymodbus 3.x
            result = self.client.read_holding_registers(address, count)
            return result.registers[0] if not result.isError() else None
        else:
            print("Not connected. Cannot read.")
            return None

    def disconnectPLC(self):
        self.client.close()
        self.connect_status = False
