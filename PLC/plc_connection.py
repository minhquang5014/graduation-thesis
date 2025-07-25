from pymodbus.client.tcp import ModbusTcpClient as mbc
from pymodbus.exceptions import ConnectionException

# This script defines PLC connection but the Python script is running as a client. This means that the PLC will be the server. 
# Every single time when you wanna run it, you would have a PLC, connect it to the server first.
# Then you can run this script to connect to the PLC and read/write data from/to it.
# Now we will code another class to connect to ip address and port as a server, no need for the real PLC hardware. 

class PLCServer:
    pass

class PLCConnection:
    def __init__(self, host='192.168.0.1', port=502):
        self.host = host
        self.port = port
        self.client = mbc(host=self.host, port=self.port)
        self.connect_status = False

    def connectPLC(self):
        try:
            self.connect_status = self.client.connect()
            print(self.connect_status) # False or True
            print(f"Connection to {self.host}:{self.port} is {'successful' if self.connect_status else 'failed'}")
            return self.connect_status
        except ConnectionException as e:
            print(f"Failed to connect to PLC: {e}")

    def write(self, address, value):
        if self.connect_status:
            # Không sử dụng 'unit' trong pymodbus 3.x
            self.client.write_registers(address, [value])  # Dùng write_registers thay vì write_register
            # Thread(target = self.write(address, value), daemon=True).start()
        else:
            print(f"Not connected. Cannot write to holding register {address}, {value}.")

    def read(self, address, count=1):
        if self.connect_status:
            # Không sử dụng 'unit' trong pymodbus 3.x
            try:
                result = self.client.read_holding_registers(address=address, count=count)
                # Thread(target = self.read(address), daemon=True).start()
                return result.registers[0] if not result.isError() else None
            except Exception as e:
                print(f"PLC connected but cannot read {address}")
                return 0  
        else:
            return 0
                

    def disconnectPLC(self):
        self.client.close()
        self.connect_status = False
