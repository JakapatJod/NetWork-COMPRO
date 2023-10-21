const snmp = require('snmp-native');

// สร้างตัวจัดการ SNMP
const session = new snmp.Session({});

// กำหนดค่าการรับ SNMP traps
session.trap(1, (error, trap) => {
  if (!error) {
    // ประมวลผลข้อมูลจาก trap ที่ได้รับ
    console.log('Received SNMP trap:', trap);
  } else {
    console.error('Error receiving SNMP trap:', error);
  }
});

// เริ่มต้นการรับ SNMP traps
session.bind({ family: 'udp4', port: 162, address: '192.168.1.100' }, () => {
  console.log('Listening for SNMP traps on UDP port 162');
});
