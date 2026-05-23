import json
import websocket 
import ssl

SERVER_URL = "ws://127.0.0.1:9001" #ikut IP Zia
# ws = websocket.create_connection(SERVER_URL, sslopt={"cert_reqs": ssl.CERT_NONE})

def sendSocket(actionName, payloadData):
    reqData = {
        "action": actionName,
        "payload": payloadData
    }
    try:
        ws = websocket.create_connection(SERVER_URL)
        ws.send(json.dumps(reqData))
        respStr = ws.recv()
        respJson = json.loads(respStr)
        ws.close()
        return respJson
        
    except Exception as e:
        return {"status": "error", "message": f"Gagal terhubung via WSS {str(e)}"}