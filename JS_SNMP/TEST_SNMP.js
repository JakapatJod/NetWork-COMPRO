const express = require('express');
const snmp = require('net-snmp');

const app = express();
const port = 8080;

app.get('/disablePort/:portNumber', (req, res) => {     // http://localhost:8080/disablePort/4
  const target = '192.168.1.100';
  const community = 'private';
  const portToDisable = req.params.portNumber;

  const session = snmp.createSession(target, community);
  const oid = `1.3.6.1.2.1.2.2.1.7.${portToDisable}`;
  const value = 2;

  const varbinds = [
    { oid, type: snmp.ObjectType.Integer, value }
  ];

  session.set(varbinds, (error, varbinds) => {
    if (error) {
      res.status(500).json({ error: `เกิดข้อผิดพลาดในการปิด port ${portToDisable}: ${error}` });
    } else {
      res.json({ message: `ปิด port ${portToDisable} สำเร็จ` });
    }
    session.close();
  });
});

app.listen(port, () => {
  console.log(`เซิร์ฟเวอร์เริ่มทำงานที่พอร์ต ${port}`);
});
