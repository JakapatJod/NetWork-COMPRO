from pysnmp.hlapi import *

def set_interface_status(community_string, target_ip, port, status):
    # OID สำหรับการเปลี่ยนสถานะของพอร์ต
    oid = ObjectIdentity('1.3.6.1.2.1.2.2.1.8.' + str(port))

    # ค่าที่ใช้เปลี่ยนสถานะ Up (1) หรือ Down (2)
    new_status = Integer(1 if status == 1 else 2)

    # สร้างคำขอ SNMP Set Request
    set_request = setCmd(
        SnmpEngine(),
        CommunityData(community_string),
        UdpTransportTarget((target_ip, 161)),
        ContextData(),
        ObjectType(oid, new_status))

    error_indication, error_status, error_index, var_binds = next(set_request)

    if error_indication:
        print(f"Error: {error_indication}")
    else:
        if error_status:
            print(f"Error: {error_status}")
        else:
            print(f"Success: Interface {port} changed state to {'Up' if status == 1 else 'Down'}")

# ตัวอย่างการใช้งาน
community_string = 'public'
target_ip_address = '192.168.1.20'
port = 3  # เปลี่ยนเป็นหมายเลขพอร์ตที่คุณต้องการควบคุม
status = 1  # ใส่ 1 หรือ 2 เพื่อเปิดหรือปิดพอร์ต

set_interface_status(community_string, target_ip_address, port, status)
