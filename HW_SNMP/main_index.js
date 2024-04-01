const express = require('express'); // http://localhost:3000/ run code
const snmp = require('net-snmp');   // C:\Users\User\Desktop\NetWork-COMPRO\REAL_HW_SNMP>node snmp_trap_index.js run ใน cmd
const cors = require('cors');   

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
    res.send(`
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Port Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .main_wrapper {
            background-color: white;
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            display: flex;
        }

        .wrapper1, .wrapper2 {
            flex: 1;
            margin: 10px;
            padding: 10px;
        }

        .wrapper1 {
            background-color: #e0e0e0;
        }

        .wrapper2 {
            background-color: #f0f0f0;
        }

        h4 {
            text-align: center;
        }

        p, .wrapper_o_tag {
            text-align: center;
        }

        .btn_main, .btn_goole {
            display: flex;
            justify-content: center;
        }

        

        .btn_change {
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .button_on {
            background-color: #4caf50;
            color: white;
        }

        .button_on:hover {
            background-color: #45a049;
        }

        .button_off {
            background-color: #f44336;
            color: white;
        }

        .button_off:hover {
            background-color: #d32f2f;
        }

        .button_submit {
            background-color: #008CBA;
            color: white;
        }

        .button_submit:hover {
            background-color: #0077A3;
        }

        .button_link {
            background-color: #333;
            color: white;
        }

        .button_link:hover {
            background-color: #222;
        }
    </style>
</head>
<body>
    <div class="main_wrapper">
        <div class="wrapper1">
            <h4>Port Manager</h4>
            <input type="number" id="port" placeholder="port">
            <p id="output"></p>
            <div class="btn_main">
                <button onclick="javascript:on()" class="button_on btn_change">On</button>
                <button onclick="javascript:off()" class="button_off btn_change">Off</button>
            </div>
        </div>
        <div class="wrapper2">
            <h4>Display Port</h4>
            <input type="number" id="port_bulk" placeholder="port_bulk">
            <p class="wrapper_o_tag" id="output_bluk"></p>
            <button onclick="javascript:bluk()" class="button_submit btn_change">Submit</button>
            <div class="btn_goole">
                <button onclick="redirectTosnmp_trap()" class="button_link btn_change">Check Status Port</button>
            </div>
        </div>
    </div>
        <script>
            function on() {
                const port = parseInt(document.getElementById("port").value);
                fetch("http://localhost:3000/set/" + port + "/1")
                .then(res => res.text()) // Parse the response as text
                .then(responseText => {
                    document.getElementById("output").innerText = responseText; // Update the output element with the response text
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
    
            function off() {
                const port = parseInt(document.getElementById("port").value);
                fetch("http://localhost:3000/set/" + port + "/2")
                .then(res => res.text()) // Parse the response as text
                .then(responseText => {
                    document.getElementById("output").innerText = responseText; // Update the output element with the response text
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }

            function bluk() {
                const port_bulk = parseInt(document.getElementById("port_bulk").value);
                fetch("http://localhost:3000/set/" + port_bulk)
                .then(res => res.text()) // Parse the response as text
                .then(responseText => {
                    document.getElementById("output_bluk").innerText = responseText; // Update the output element with the response text
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }

            function redirectTosnmp_trap() {
                window.open("http://127.0.0.1:8000/", "_blank", 'width=600,height=400');
            }
        </script>
    </body>
    </html>
    `)
})

app.get('/set/:port/:status', (req, res) => {
    const target = '192.168.119.80';
    const community = 'private';

    const oid = `1.3.6.1.2.1.2.2.1.7.${req.params.port}`;  // '1.3.6.1.2.1.2.2.1.7.1'; เปิด port 

    const ciscoContactInfoOid = `1.3.6.1.2.1.2.2.1.2.${req.params.port}`;

    const value = parseInt(req.params.status);

    const session = snmp.createSession(target, community, { timeout: 5000 });

    const varbinds = [
        { oid, type: snmp.ObjectType.Integer, value }
    ];

    session.set(varbinds, (error, varbinds) => {
        if (error) {
            console.error('Error setting SNMP values:', error);
        } else {
            console.log('SNMP set request successful');
            varbinds.forEach((vb) => {
                console.log(`${ vb.oid } = ${ vb.value }`);

            });
        }

    });

    const oids = [ciscoContactInfoOid];

    session.get(oids, (error, varbinds) => {
        if (error) {
            console.error(error);
        } else {
            varbinds.forEach((vb) => {
                if (value == 1){
                    res.send(`${vb.value} ON !!`);
                }else{
                    res.send(`${vb.value} OFF !!`);
                }
            });
        }
        session.close();
    });
    })

app.get('/set/:port_bulk', (req, res) => {
    const target = '192.168.119.80';
    const community = 'public';
    const interfaceInfoOid = '1.3.6.1.2.1.2.2.1.2.';
    const numInterfaces = parseInt(req.params.port_bulk);
    const session = snmp.createSession(target, community);

    const getInterfaceInfo = (index) => {
        const interfaceOid = interfaceInfoOid + index;

        return new Promise((resolve, reject) => {
            session.get([interfaceOid], (error, varbinds) => {
                if (error) {
                    reject(`Error querying interface ${index}: ${error}`);
                } else {
                    const interfaceName = varbinds[0].value.toString();
                    console.log(`Interface ${index}: ${interfaceName}`);
                    resolve({ index, name: interfaceName });
                }
            });
        });
    };

    const interfaceInfoPromises = Array.from({ length: numInterfaces }, (_, index) =>
        getInterfaceInfo(index + 1)
    );

    Promise.all(interfaceInfoPromises)
        .then((interfaceInfoList) => {
            const interfaceNames = interfaceInfoList.map(info => `Interface ${info.index}: ${info.name}`);
            console.log('All interfaces queried successfully.');
            res.send(interfaceNames.join('\n')); // Send all interface names in a single response
        })
        .catch((error) => {
            console.error(`Error querying interfaces: ${error}`);
            res.status(500).send('Error querying interfaces');
        })
        .finally(() => {
            session.close();
        });
});




app.listen(3000, () => {
    console.log('Server is running on port 3000');
});