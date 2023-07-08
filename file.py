import socket
from machine import Pin
import network
from time import sleep

ssid = 'Duba 3 DIICOT'
password = '123xxx123'


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    wlan.connect(ssid, password)
    
    #Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -=1
        print('Waiting for connection...')
        sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('Connected!')
    print(wlan.ifconfig())


try:
    connect()
except KeyboardInterrupt:
    machine.reset()


# creeaza ledurile
red = Pin(15, mode=Pin.OUT)
green = Pin(14, mode=Pin.OUT)
blue = Pin(13, mode=Pin.OUT)

red.value(1)
green.value(1)
blue.value(1)

# creeaza un server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# specifica ca serverul va rula pe portul 5678, accesibil de pe orice ip al serverului
serversocket.bind(('', 80))
# serverul poate accepta conexiuni; specifica cati clienti pot astepta la coada
serversocket.listen(5)

while True:
    print('#############################')
    print('Serverul asculta potentiali client')
    # asteapta conectarea uni client la server
    (clientsocket, address) = serversocket.accept()
    print('S-a conectat un client')

    # se proceseaza cererea
    cerere = ''
    linieDeStart = ''
    while True:
        data = clientsocket.recv(1024)
        if len(data) < 1:
            break
        cerere = cerere + data.decode()
        print('S-a citit mesajul: \n---------------------------\n' +
              cerere + '\n---------------------------')
        pozitie = cerere.find('\r\n')
        if pozitie > -1:
            linieDeStart = cerere[0:pozitie]
            print('S-a citit linia de start din cerere: ##### ' +
                  linieDeStart + '##### ')
            break
    print('S-a terminat citirea')

    if linieDeStart == '':
        clientsocket.close()
        print('S-a terminat comunicarea cu clientul - nu s-a primit niciun mesaj.')
        continue

    path = linieDeStart.split(" ")[1]
    startLine = 'HTTP/1.1 200 OK\r\n'

    if red.value() == 0:
        red_value = 'on'
    else:
        red_value = 'off'
    if green.value() == 0:
        green_value = 'on'
    else:
        green_value = 'off'
    if blue.value() == 0:
        blue_value = 'on'
    else:
        blue_value = 'off'

    text = '''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMpixel</title>
</head>

<style>

    body {
        background-color: black;
        text-align: center;
        color: white;

    }
    div {       
        margin-top: 30%;
    }
    h1 {
        font-size: 40px;
    }

    button {
        border-radius: 50%;
        font-size: 20px;
        padding: 20px;
        cursor: pointer;
    }

    #redLed {

        background-color: white;
        color: red;
    }

    #greenLed {

        background-color: white;
        color: green;
    }

    #blueLed {

        background-color: white;
        color: blue;
    }
</style>
<script>
    var redLed, greenLed, blueLed;
    function checkLoaded(){
        redLed="''' + red_value + '''", greenLed="''' + green_value +'''", blueLed="''' + blue_value + '''";
        if (redLed == "on") {
            document.getElementById('redLed').style.backgroundColor = 'red';
            document.getElementById('redLed').style.color = 'white';
        }


        if (greenLed == "on") {
            document.getElementById('greenLed').style.backgroundColor = 'green';
            document.getElementById('greenLed').style.color = 'white';
        }

        console.log("blueLed: " + blueLed)
        if (blueLed == "on") {
            document.getElementById('blueLed').style.backgroundColor = 'blue';
            document.getElementById('blueLed').style.color = 'white';
        }
    }



    function redButton() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                redLed = this.responseText;
                console.log('redLed: ' + redLed)
                if (redLed == 'off')
                    redLed = 'on';
                else
                    redLed = 'off'
                console.log('redLed: ' + redLed)
                if (redLed == 'off') {
                    document.getElementById('redLed').style.backgroundColor = 'black';
                    document.getElementById('redLed').style.color = 'red';

                }
                else {
                    document.getElementById('redLed').style.backgroundColor = 'red';
                    document.getElementById('redLed').style.color = 'white';
                    document.getElementById('greenLed').style.backgroundColor = 'white';
                    document.getElementById('greenLed').style.color = 'green';
                    document.getElementById('blueLed').style.backgroundColor = 'white';
                    document.getElementById('blueLed').style.color = 'blue';
                }

                http = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                    }
                }
                xhttp.open('GET', '/?led=red', true);
                xhttp.send();

            }
        }
        xhttp.open('GET', '/getRedLedValue', true);
        xhttp.send();


    }
    function greenButton() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                greenLed = this.responseText;
                console.log('greenLed: ' + greenLed)
                if (greenLed == 'off')
                    greenLed = 'on';
                else
                    greenLed = 'off'

                if (greenLed == 'off') {
                    document.getElementById('greenLed').style.backgroundColor = 'white';
                    document.getElementById('greenLed').style.color = 'green';
                }
                else {
                    document.getElementById('greenLed').style.backgroundColor = 'green';
                    document.getElementById('greenLed').style.color = 'black';
                    document.getElementById('redLed').style.backgroundColor = 'white';
                    document.getElementById('redLed').style.color = 'red';
                    document.getElementById('blueLed').style.backgroundColor = 'white';
                    document.getElementById('blueLed').style.color = 'blue';
                }

                http = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                    }
                }
                xhttp.open('GET', '/?led=green', true);
                xhttp.send();

            }
        }
        xhttp.open('GET', '/getGreenLedValue', true);
        xhttp.send();


    }
    function blueButton() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                blueLed = this.responseText;
                if (blueLed == 'off')
                    blueLed = 'on';
                else
                    blueLed = 'off'
                console.log('blueLed: ' + blueLed)
                if (blueLed == 'off') {
                    document.getElementById('blueLed').style.backgroundColor = 'white';
                    document.getElementById('blueLed').style.color = 'blue';
                }
                else {
                    document.getElementById('blueLed').style.backgroundColor = 'blue';
                    document.getElementById('blueLed').style.color = 'white';
                    document.getElementById('greenLed').style.backgroundColor = 'white';
                    document.getElementById('greenLed').style.color = 'green';
                    document.getElementById('redLed').style.backgroundColor = 'white';
                    document.getElementById('redLed').style.color = 'red';
                }

                http = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                    }
                }
                xhttp.open('GET', '/?led=blue', true);
                xhttp.send();




            }
        }
        xhttp.open('GET', '/getBlueLedValue', true);
        xhttp.send();



    }
</script>

<body onload="checkLoaded()">
    <div>
        <h1>SMpixel</h1>
        <button id="redLed" onclick="redButton()">RED</button><br><br>
        <button id="greenLed" onclick="greenButton()">GREEN</button><br><br>
        <button id="blueLed" onclick="blueButton()">BLUE</button><br><br>
    </div>
</body>

</html>'''
    
    header = ('Server: SMpixelServer\r\nConnection: close\r\nContent-Length: ' +
              str(len(text)) + '\r\n' + 'Content-Type: text/html' + '\r\n\r\n')

    if path == '/?led=red':
        green.value(1)
        blue.value(1)
        red.toggle()

    elif path == '/?led=green':
        red.value(1)
        blue.value(1)
        green.toggle()
        
    elif path == '/?led=blue':
        red.value(1)
        green.value(1)
        blue.toggle()

    elif path == '/getRedLedValue':
        if red.value() == 0:
            text = 'on'
        else:
            text = 'off'
        header = ('Server: SMpixelServer\r\nConnection: close\r\nContent-Length: ' +
                  str(len(text)) + '\r\n' + 'Content-Type: text/plain' + '\r\n\r\n')

    elif path == '/getGreenLedValue':
        if green.value() == 0:
            text = 'on'
        else:
            text = 'off'
        header = ('Server: SMpixelServer\r\nConnection: close\r\nContent-Length: ' +
                  str(len(text)) + '\r\n' + 'Content-Type: text/plain' + '\r\n\r\n')

    elif path == '/getBlueLedValue':
        if blue.value() == 0:
            text = 'on'
        else:
            text = 'off'
        header = ('Server: SMpixelServer\r\nConnection: close\r\nContent-Length: ' +
                  str(len(text)) + '\r\n' + 'Content-Type: text/plain' + '\r\n\r\n')

    response = startLine.encode(
        'utf-8') + header.encode('utf-8') + text.encode('utf-8')

    clientsocket.sendall(response)
    clientsocket.close()
    print('S-a terminat comunicarea cu clientul: ' +
          address[0] + ':' + str(address[1]))
