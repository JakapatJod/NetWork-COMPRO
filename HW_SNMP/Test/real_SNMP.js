const express = require('express');
const snmp = require('net-snmp');

const app = express();
const port = 8080;

app.get('/', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>เปิดหรือปิดพอร์ต SNMP</title>
      </head>
      <body>
        <h1>เปิดหรือปิดพอร์ต SNMP</h1>
        <a href="/enablePort" style="margin-right: 20px;">เปิดพอร์ต</a>
        <a href="/disablePort">ปิดพอร์ต</a>
      </body>
    </html>
  `);
});

app.get('/disablePort', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>ปิดพอร์ต SNMP</title>
      </head>
      <body>
        <h1>ปิดพอร์ต SNMP</h1>
        <form method="get" action="/disablePortResult">
          <label for="portNumber">หมายเลข Port: </label>
          <input type="text" id="portNumber" name="portNumber">
          <button type="submit">ปิดพอร์ต</button>
        </form>
        <p><a href="/">ย้อนกลับ</a></p>
      </body>
    </html>
  `);
});

app.get('/enablePort', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>เปิดพอร์ต SNMP</title>
      </head>
      <body>
        <h1>เปิดพอร์ต SNMP</h1>
        <form method="get" action="/enablePortResult">
          <label for="portNumber">หมายเลข Port: </label>
          <input type="text" id="portNumber" name="portNumber">
          <button type="submit">เปิดพอร์ต</button>
        </form>
        <p><a href="/">ย้อนกลับ</a></p>
      </body>
    </html>
  `);
});

app.get('/enablePortResult', (req, res) => {
  const target = '192.168.1.100';
  const community = 'private';
  const portToEnable = req.query.portNumber;

  const session = snmp.createSession(target, community);
  const oid = `1.3.6.1.2.1.2.2.1.7.${portToEnable}`;
  const value = 1; // Set to 1 to enable the port

  const varbinds = [
    { oid, type: snmp.ObjectType.Integer, value }
  ];

  session.set(varbinds, (error, varbinds) => {
    if (error) {
      res.status(500).json({ error: `เกิดข้อผิดพลาดในการเปิด port ${portToEnable}: ${error}` });
    } else {
      res.send(`
        <html>
          <head>
            <title>ผลการเปิดพอร์ต SNMP</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                text-align: center;
              }
              h1 {
                color: #333;
              }
              p {
                margin: 10px;
                font-size: 18px;
              }
              a {
                text-decoration: none;
                color: #007bff;
              }
            </style>
          </head>
          <body>
            <h1>ผลการเปิดพอร์ต SNMP</h1>
            <p>เปิดพอร์ต <span id="portNumberResult">${portToEnable}</span> สำเร็จ</p>
            <p><a href="/enablePort">ย้อนกลับ</a></p>
          </body>
        </html>
      `);
    }
    session.close();
  });
});

app.get('/disablePortResult', (req, res) => {
  const target = '192.168.1.100';
  const community = 'private';
  const portToDisable = req.query.portNumber;

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
      res.send(`
        <html>
          <head>
            <title>ผลการปิดพอร์ต SNMP</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                text-align: center;
              }
              h1 {
                color: #333;
              }
              p {
                margin: 10px;
                font-size: 18px;
              }
              a {
                text-decoration: none;
                color: #007bff;
              }
            </style>
          </head>
          <body>
            <h1>ผลการปิดพอร์ต SNMP</h1>
            <p>ปิดพอร์ต <span id="portNumberResult">${portToDisable}</span> สำเร็จ</p>
            <p><a href="/disablePort">ย้อนกลับ</a></p>
          </body>
        </html>
      `);
    }
    session.close();
  });
});
app.listen(port, () => {
  console.log(`เซิร์ฟเวอร์เริ่มทำงานที่พอร์ต ${port}`);
});
