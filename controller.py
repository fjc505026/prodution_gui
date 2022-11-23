
import serial.tools.list_ports
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.debug_port=''
        self.uart_test_port=''


    def get_device_port(self):
        res=self.update_device_port()
        if(res[0]):
            self.debug_port=res[1]
        return self.debug_port

    def update_device_port(self):
        serial_ports = []
        for p in serial.tools.list_ports.comports():
            if p.manufacturer == "FTDI" or p.manufacturer == "DTI":
                serial_ports.append(p)

        if len(serial_ports) == 0:
            print("No valid serial devices found")
            return False
        elif len(serial_ports) == 1:
            print(f"Selecting serial port {serial_ports[0]}")
            serial_device = serial_ports[0]
        else:
            for i, p in enumerate(serial_ports):
                print("{}: {}".format(i, p.name))
            device_port = int(input("Select device number: "))
            if device_port >= len(serial_ports):
                print("Invalid serial device")
                return False
            serial_device = serial_ports[device_port]
        return True, serial_device

    def get_uart_test_port(self):
        res=self.update_uart_test_port()
        if(res[0]):
            self.uart_test_port=res[1]
        return self.uart_test_port

    def update_uart_test_port(self):
        serial_ports = []
        # for p in serial.tools.list_ports.comports():
        #     if p.manufacturer == "FTDI" or p.manufacturer == "DTI":
        #         serial_ports.append(p)

        # if len(serial_ports) == 0:
        #     print("No valid serial devices found")
        #     return
        # elif len(serial_ports) == 1:
        #     print(f"Selecting serial port {serial_ports[0]}")
        #     serial_device = serial_ports[0]
        # else:
        #     for i, p in enumerate(serial_ports):
        #         print("{}: {}".format(i, p.name))
        #     device_port = int(input("Select device number: "))
        #     if device_port >= len(serial_ports):
        #         print("Invalid serial device")
        #         return
        #     if args.exmod and "uart" in args.exmod: 
        #         uart_port = int(input("Select UART number: "))
        #         if uart_port >= len(serial_ports):
        #             print("Invalid UART port")
        #             sys.exit(os.EX_DATAERR)    
        #         test_uart = serial_ports[uart_port]
        #     serial_device = serial_ports[device_port]
        return serial_ports;          
