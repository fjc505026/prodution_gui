#!/usr/bin/python3
import argparse
import csv
import os
import subprocess
import sys
import json
from scanner.ecia import Scanner
from devices import device_list
import database as db
from devices import def1119

import serial.tools.list_ports
from CAN import *
from uart import *
from PDF import *
from command import *
from ISP import *

from rich.console import Console
from tests.LTE import get_ids

console = Console()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Definium Technologies device test tool"
    )
    parser.add_argument(
        "--no_print", help="Don't print passed test results", action="store_true"
    )
    parser.add_argument("--no_test", help="Don't test device", action="store_true")
    parser.add_argument(
        "--test_mode",
        help="Put device into test mode instead of enable",
        action="store_true",
    )
    parser.add_argument(
        "--can", help="Enable CAN Echo (for Sensor Gateways)", action="store_true"
    )
    parser.add_argument("--port", help="Override serial port selection", default=None)

    parser.add_argument("-b","--board", help="The number of board type", default=None)

    parser.add_argument("-m","--manual", help="manual input board eui",  action="store_true")

    parser.add_argument("-e","--exmod", nargs="*", type=list, help="add extra module to test",default=None)


    args = parser.parse_args()

    keys = {}
    boards = {}
    batch_ids = {}
    bootldr_keys = {}
    board_ids = {}
    uart_port=None

    if not args.manual:
        s = Scanner()

    if args.port is not None:
        serial_device = args.port
    else:
        serial_ports = []
        for p in serial.tools.list_ports.comports():
            if p.manufacturer == "FTDI" or p.manufacturer == "DTI":
                serial_ports.append(p)

        if len(serial_ports) == 0:
            print("No valid serial devices found")
            sys.exit(os.EX_UNAVAILABLE)
        elif len(serial_ports) == 1:
            print(f"Selecting serial port {serial_ports[0]}")
            serial_device = serial_ports[0]
        else:
            for i, p in enumerate(serial_ports):
                print("{}: {}".format(i, p.name))
            device_port = int(input("Select device number: "))
            if device_port >= len(serial_ports):
                print("Invalid serial device")
                sys.exit(os.EX_DATAERR)
            if args.exmod and "uart" in args.exmod: 
                uart_port = int(input("Select UART number: "))
                if uart_port >= len(serial_ports):
                    print("Invalid UART port")
                    sys.exit(os.EX_DATAERR)    
                test_uart = serial_ports[uart_port]
            serial_device = serial_ports[device_port]    

    if args.can:
        can_echo = CAN_Echo("can0")
        can_echo.start()
    
    if uart_port:
        uart_echo=Uart_echo(test_uart,"echo uart")
        uart_echo.start()    

    while True:
        if not args.manual:
            s.drain()
            print("Please scan device barcode(plug in battery and switch on the board)")
            bc = s.scan()

            if "S" not in bc:
                print("Could not decode barcode")
                continue
            eui = bc["S"]
        else:
            while True:
                user_inpput = input("Please type in board eui: ")

                if len(user_inpput)==16:
                    eui=user_inpput
                    break
                else:
                    print("the eui should be 16 digit")
                    continue
        

        db.connect()
        dev = db.get_device_by_eui(eui)
        if dev is None:
            print("Invaild database object returned")
            continue

        print(dev)
        # lwn = db.get_or_create_lorawan_details_by_eui(eui)
        lwn = None
        if lwn is None:
            print("Device does not have LoRa radio")

        # db.commit()

        res = reboot_device(serial_device)
        if not res:
            print("Could not reboot device")
            continue

        if lwn is not None:
            print(lwn["region"])
            if lwn["region"] == "NA":
                region = "US915"
            elif lwn["region"] == "EU":
                region = "EU868"
            elif lwn["region"] == "AS":
                region = "AS923"
            elif lwn["region"] == "AU":
                region = "AU915"
            else:
                print("Invalid region found")
                continue
            print(lwn)
        else:
            region = None

        # reboot_device(serial_device)
        _, version = exec_command(serial_device, "version")
        print(version)
        if len(version) == 0:
            print("\033[91m", end="")
            print("No reply from device")
            print("\033[0m", end="")
            continue

        if lwn is not None:
            region_valid = False
            for v in version:
                if region in v:
                    region_valid = True

            if not region_valid:
                print("\033[91m", end="")
                print("Device region differs from database")
                print("\033[0m", end="")
                continue
            # success, msg = exec_command(serial_device, 'board_id')
            # if not success:
            #    print("Failed to retrieve board identifier")
            #    continue
            # try:
            #    board_id = int(msg[0][6:])
            # except (ValueError, IndexError):
            #    print("Failed to parse board identifier - {}".format(msg))
            #    continue

            if not configure_device(serial_device, eui, lwn["app_eui"], lwn["app_key"]):
                print("Device configuration failed")
                break

            time.sleep(2)
            print("Verifying Config")
            success, msg = exec_command(serial_device, "lora eui dev")
            print(msg)
            new_eui = parse_struct_syntax(msg[0])
            print(new_eui)
            if new_eui is None or new_eui != eui:
                print("EUI Verification failed - reconfigure device")
                continue
            else:
                print("Device EUI verified")

            success, msg = exec_command(serial_device, "lora eui app")
            new_eui = parse_struct_syntax(msg[0])
            print(new_eui)
            if new_eui is None or new_eui != lwn["app_eui"]:
                print("Application EUI Verification failed - reconfigure device")
                continue
            else:
                print("Application EUI verified")
            success, msg = exec_command(serial_device, "lora key app")
            key = parse_struct_syntax(msg[0])
            if key is None or key != lwn["app_key"]:
                print("Application Key Verification failed - reconfigure device")
                continue
            else:
                print("Application Key verified")

        print("Settings verified")

        if args.no_test:
            print("Skipping testing")
            passed = True
        else:
            print("Beginning test")
            test_output: List[str] = []

            if lwn is not None:
                print("Verifying key for device {}".format(eui))
                success, msg = exec_command(serial_device, "lora key app")
                print(msg)
                if not success:
                    print("Failed to retrieve application key")
                    test_output += ["APP KEY NOT VERIFIED"]
                else:
                    key = parse_struct_syntax(msg[0])
                    test_output += [
                        "APP KEY "
                        + (
                            "MATCHES"
                            if lwn["app_key"].lower() == key.lower()
                            else "DOES NOT MATCH"
                        )
                    ]

            def1119.Def1119Device.init_device("", serial_device)
            if uart_port:
                from tests import UART
                def1119.Def1119Device.add_periphs(UART)
            reboot_device(serial_device)
            test_output += [""]
            test_output.extend(def1119.Def1119Device.test_periphs(serial_device))
            print("test_output")
            print(test_output)
            passed, test_data= def1119.Def1119Device.parse_tests(test_output)
            print("test_data")
            print(test_data)
            # generate_report_pdf(eui, test_output, test_data, passed)
            client_data={}
            if get_ids()[0]:
                print(eui,list(get_ids()[1:]))
                iccid=str(get_ids()[1])
                imsi=str(get_ids()[2])
                imei=str(get_ids()[3])
                client_data={'iccid':iccid,'imsi':imsi,'imei':imei}
                client_json=json.dumps(client_data)
                print(client_json)
            try:    
                with open('dt1119.csv','a', newline='') as test_file:
	                test_writer=csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	                test_writer.writerow([eui,get_ids()[1],get_ids()[2],get_ids()[3]])
            except OSError:
                print("open the CSV file fail")
                sys.exit(os.EX_NOINPUT)        

            db.connect()
            if client_data:
                db.set_device_client_data(eui,client_json)
            db.add_test_to_device_by_eui(eui, test_data)
            db.commit()

            for r in test_data["Details"]:
                if "RESULT" in r.keys() and "FAIL" in r["RESULT"]:
                    console.print(f'[bold red]{r["TEST"]} FAIL[bold red]')
                else:
                    console.print(f'[bold green]{r["TEST"]} PASS[bold green]')
                print(r)

        if passed:
            # exec_password(serial_device, dev["default_password"])
            # exec_command(serial_device, "dormant 1")
            # exec_command(serial_device, "")
            # print(enable_device(serial_device))
            console.print(f"[bold green]PASS[bold green]")
        else:
            console.print(f"[bold red]FAIL[bold red]")
        print("Test Procedure Complete")
