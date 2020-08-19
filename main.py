import sys
import getopt
import time
from components.PacpowerAPI import PacpowerAPI


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:s:v:l:',
    ['user=', 'pass=', 'storage=', 'volt=', 'location='])

    parsed_argv = {
        'user': '', 'pass': '', 'storage_id': '', 'max_volt': '', 'location': ''
    }

    for key, val in opts:
        print(key, val)
        if key in ('-u', '--user'):
            parsed_argv['user'] = val
        if key in ('-p', '--pass'):
            parsed_argv['pass'] = val
        if key in ('-s', '--storage'):
            parsed_argv['storage_id'] = val
        if key in ('-v', '--volt'):
            parsed_argv['max_volt'] = int(val)
        if key in ('-l', '--location'):
            parsed_argv['location'] = val
    
    print(parsed_argv)
    pAPI = PacpowerAPI('pacpower', 'pacpower1234', 'DXE3A0305B', 54)
    # pAPI = PacpowerAPI(parsed_argv['user'], parsed_argv['pass'],
    # parsed_argv['storage_id'], parsed_argv['max_volt'])
    pAPI.initAPI()

    while True: 
        newData = pAPI.get_data_pack()
        print("NewData")
        print(newData)
        pAPI.send_to_cloud("pac0")

        # sleep for 15 mins
        time.sleep(60*15)
