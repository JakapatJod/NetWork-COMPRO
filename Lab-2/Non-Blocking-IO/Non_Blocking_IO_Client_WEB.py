import logging
import socket
import select

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',datefmt = '%H:%M:%S',level=logging.DEBUG)

# Non Blocking
def create_nonblocking(host,port):
    logging.info('Non Blocking = creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    logging.info('Non Blocking - connecting')
    ret = s.connect_ex((host,port)) # Blocking
    
    print(ret)
    if ret != 0:
        logging.info('Non Blocking- failed to connect!')
        return
    
    logging.info('Non Blocking - Connected!')
    s.setblocking(False)

    inputs = [s]
    print(inputs)
    outputs = [s]
    print(outputs)

    while inputs:
        logging.info('Non Blocking - sending...')
        readable,writeble,exceptional = select.select(inputs,outputs,inputs,0.5)

        print(readable)
        print(writeble)
        print(exceptional)

        for s in writeble:
            logging.info('Non Blocking - sending...')
            data = s.send(b'hello\r\n')
            logging.info(f'Non Blocking - sent : {data}...')
            outputs.remove(s)
        for s in readable:
            logging.info(f'Non Blocking - sent : {data}...')
            data = s.recv(1024)
            logging.info(f'Non Blocking - data: {len(data)}')
            logging.info(f'Non Blocking - closing...')
            s.close()
            inputs.remove()
            break

        for s in exceptional:
            logging.info(f'Non Blocking - error')
            inputs.remove(s)
            break

        for s in exceptional:
            logging.info(f'Non Blocking - error')
            inputs.remove(s)
            outputs.remove(s)
            break

# Main
def main():
    create_nonblocking('voidrealms.com',80)

if __name__ == "__main__":
    main()