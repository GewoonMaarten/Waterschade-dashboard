from WifiService import WifiService

service = WifiService()
json = service.get_wifi_connection()

print(json)
