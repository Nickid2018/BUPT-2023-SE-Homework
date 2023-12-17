import sys
import time

import rsa

import ac_controller
import constants
from network_manager import NetworkManager

private_key_str = sys.argv[1]
constants.private_key = rsa.PrivateKey.load_pkcs1(("-----BEGIN RSA PRIVATE KEY-----\n" + private_key_str + "\n-----END RSA PRIVATE KEY-----").encode())

ac1 = ac_controller.ACController('2-233')
nm1 = NetworkManager(ac1)
ac1.set_network_manager(nm1)
ac1.initial_temperature = 32
ac2 = ac_controller.ACController('1-114')
nm2 = NetworkManager(ac2)
ac2.set_network_manager(nm2)
ac2.initial_temperature = 28
ac3 = ac_controller.ACController('1-514')
nm3 = NetworkManager(ac3)
ac3.set_network_manager(nm3)
ac3.initial_temperature = 30
ac4 = ac_controller.ACController('1-919')
nm4 = NetworkManager(ac4)
ac4.set_network_manager(nm4)
ac4.initial_temperature = 29
ac5 = ac_controller.ACController('1-111')
nm5 = NetworkManager(ac5)
ac5.set_network_manager(nm5)
ac5.initial_temperature = 35

# ---- Start! ----
ac1.toggle_power()
ac1.commit()
time.sleep(10)

ac2.toggle_power()
ac1.set_temperature(18)
ac5.toggle_power()
ac1.commit()
ac2.commit()
ac5.commit()
time.sleep(10)

ac3.toggle_power()
ac3.commit()
time.sleep(10)

ac2.set_temperature(19)
ac4.toggle_power()
ac2.commit()
ac4.commit()
time.sleep(10)

ac5.set_temperature(22)
ac5.commit()
time.sleep(10)

ac1.change_wind_speed()
ac1.commit()
time.sleep(10)

ac2.toggle_power()
ac2.commit()
time.sleep(10)

ac2.toggle_power()
ac5.change_wind_speed()
ac2.commit()
ac5.commit()
time.sleep(10)

time.sleep(10)

ac1.set_temperature(22)
ac4.change_wind_speed()
ac4.set_temperature(18)
ac1.commit()
ac4.commit()
time.sleep(10)

time.sleep(10)

ac2.set_temperature(22)
ac2.commit()
time.sleep(10)

ac5.change_wind_speed()
ac5.commit()
time.sleep(10)

time.sleep(10)

ac1.toggle_power()
ac3.change_wind_speed()
ac3.change_wind_speed()
ac3.set_temperature(24)
ac1.commit()
ac3.commit()
time.sleep(10)

ac5.change_wind_speed()
ac5.change_wind_speed()
ac5.set_temperature(20)
ac5.commit()
time.sleep(10)

ac2.toggle_power()
ac2.commit()
time.sleep(10)

ac3.change_wind_speed()
ac3.change_wind_speed()
ac3.commit()
time.sleep(10)

ac1.toggle_power()
ac4.set_temperature(20)
ac4.change_wind_speed()
ac4.change_wind_speed()
ac1.commit()
ac4.commit()
time.sleep(10)

ac2.toggle_power()
ac2.commit()
time.sleep(10)

ac5.set_temperature(25)
ac5.commit()
time.sleep(10)

time.sleep(10)

ac3.toggle_power()
ac3.commit()
time.sleep(10)

ac5.toggle_power()
ac5.commit()
time.sleep(10)

ac1.toggle_power()
ac1.commit()
time.sleep(10)

ac2.toggle_power()
ac4.toggle_power()
ac2.commit()
ac4.commit()