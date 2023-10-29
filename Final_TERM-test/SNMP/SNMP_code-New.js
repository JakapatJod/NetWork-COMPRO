const express = require('express');
const { Session } = require('snmp-native');     // http://localhost:2000

const app = express();
const port = 2000;
const ip_add = '192.168.1.100';
const community = 'private';

function createSession() {
  return new Session({ host: ip_add, community: community });
}

function closeSessionAndCallback(session, callback, error) {
  session.close();
  callback(error);
}

function managePort(portNumber, action, callback) {
  const session = createSession();
  const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 7, portNumber];
  const type = 2;

  session.set({ oid, value: action, type }, (error) => {
    closeSessionAndCallback(session, callback, error);
  });
}

function getPortInfo(oid, callback) {
  const session = createSession();

  session.getSubtree({ oid }, (error, varbinds) => {
    const portData = {};

    for (const varbind of varbinds) {
      const portNumber = varbind.oid[varbind.oid.length - 1];
      portData[portNumber] = varbind.value;
    }

    closeSessionAndCallback(session, () => {
      if (error) {
        callback(error, null);
      } else {
        callback(null, portData);
      }
    }, null);
  });
}

function getSessionData(oid, callback) {
  const session = createSession();

  session.get({ oid }, (error, varbinds) => {
    closeSessionAndCallback(session, () => {
      if (error) {
        callback(error, null);
      } else {
        if (varbinds.length > 0) {
          const data = varbinds[0].value;
          callback(null, data);
        } else {
          callback(new Error('No data found for the specified OID'), null);
        }
      }
    }, null);
  });
}

app.get('/open/:portNumber', (req, res) => {
  const portNumber = req.params.portNumber;
  managePort(portNumber, 1, (error) => {
    if (error) {
      res.status(500).send(`Error opening port: ${error.message}`);
    } else {
      res.redirect('/');
    }
  });
});

app.get('/close/:portNumber', (req, res) => {
  const portNumber = req.params.portNumber;
  managePort(portNumber, 2, (error) => {
    if (error) {
      res.status(500).send(`Error closing port: ${error.message}`);
    } else {
      res.redirect('/');
    }
  });
});



// -------------------------------------------------------- Get เวลา

app.get('/gettime', (req, res) => {
  const oid = [1, 3, 6, 1, 2, 1, 1, 3, 0];
  getSessionData(oid, (error, sysUpTime) => {
    if (error) {
      res.status(500).send(`Error fetching system uptime: ${error.message}`);
    } else {
        const totalSeconds = sysUpTime;
        const hours = Math.floor(totalSeconds / 3600);
        const remainingSeconds = totalSeconds % 3600;
        const minutes = Math.floor(remainingSeconds / 60);
        const seconds = remainingSeconds % 60;
      const html = `
        <html>
          <head>
            <title>System Uptime</title>
          </head>
          <body>
            <h1>System Uptime</h1>
            <p>System Uptime: ${hours} Hours ${minutes} Min ${seconds} Sec</p>
            </body>
        </html>
      `;
      res.send(html);
    }
  });
});
// --------------------------------------------------------


// -------------------------------------------------------- Get ต่างๆ


app.get('/getany', (req, res) => {
    const oid = [1,3,6,1,4,1,9,2,1,61,0];
    getSessionData(oid, (error, getany) => {
      if (error) {
        res.status(500).send(`Error  ${error.message}`);
      } else {

        const html = `
          <html>
            <head>
              <title>Get</title>
            </head>
            <body>
              <h1>Get</h1>
              <p>GET Output : ${getany} </p>
            </body>
          </html>
        `;
        res.send(html);
      }
    });
  });
// --------------------------------------------------------



// -------------------------------------------------------- Set


app.get('/setDeviceName', (req, res) => {
    const newDeviceName = req.query.newDeviceName; 
    const oid = [1, 3, 6, 1, 2, 1, 1, 5, 0];
  
    const session = createSession();
    session.set({ oid, value: newDeviceName, type: 4 }, (error) => {
      closeSessionAndCallback(session, (setError) => {
        if (setError) {
          res.status(500).send(`Error setting device name: ${setError.message}`);
        } else {
          res.redirect('/');
        }
      });
    });
  });
  

// --------------------------------------------------------




app.get('/', (req, res) => {
    getPortInfo([1, 3, 6, 1, 2, 1, 2, 2, 1, 7], (error, portStatus) => {
      if (error) {
        res.status(500).send(`Error fetching port data: ${error.message}`);
      } else {
        getPortInfo([1, 3, 6, 1, 2, 1, 2, 2, 1, 2], (nameError, portName) => {
          if (nameError) {
            res.status(500).send(`Error fetching port names: ${nameError.message}`);
          } else {
            const html = `
            <html>
              <head>
                <title>SNMP Port Status</title>
                <style>
                  .status-up { color: green; }
                  .status-down { color: red; }
                </style>
              </head>
              <body>
                <h1>SNMP Port Status</h1>
                <table>
                  <tr>
                    <th>Port Name</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                  ${Object.entries(portStatus)
                    .map(([portNumber, status]) => `
                      <tr>
                        <td>${portName[portNumber] || 'Port ' + portNumber}</td>
                        <td class="status-${status === 1 ? 'up' : 'down'}">${status === 1 ? 'Up' : 'Down'}</td>
                        <td>
                          <a href="/open/${portNumber}">เปิด</a> |
                          <a href="/close/${portNumber}">ปิด</a>
                        </td>
                      </tr>
                    `).join('')}
                </table>
                <div>
                  <h3>Get</h3>
                  <a href="/gettime">Get Uptime</a>
                </div>
                <div>
                  <a href="/getany"> Get Test </a>
                </div>
                <div>
                <h3>Config</h3>
                <form action="/setDeviceName" method="get">
                    <label for="newDeviceName">New Device Name:</label>
                    <input type="text" name="newDeviceName" id="newDeviceName" required>
                    <button type="submit">Set Device Name</button>
                </form>
                </div>
              </body>
            </html>
          `;
          res.send(html);
          }
        });
      }
    });
  });
  

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
