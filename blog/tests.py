import requests
url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=b70d59041b71455ab753c78956f6a8b8&ip_address='
ip = '103.10.29.126'
final_url = url + ip
response = requests.get(final_url)
print(response.status_code)
print(response.content)

# 200
# b'{"ip_address":"103.10.29.126","city":"Patan","city_geoname_id":1282931,"region":"Province 3","region_iso_code":"P3","region_geoname_id":12095449,"postal_code":null,"country":"Nepal","country_code":"NP","country_geoname_id":1282988,"country_is_eu":false,"continent":"Asia","continent_code":"AS","continent_geoname_id":6255147,"longitude":85.3142,"latitude":27.6766,"security":{"is_vpn":false},"timezone":{"name":"Asia/Kathmandu","abbreviation":"+0545","gmt_offset":5,"current_time":"19:47:12","is_dst":false},"flag":{"emoji":"\xf0\x9f\x87\xb3\xf0\x9f\x87\xb5","unicode":"U+1F1F3 U+1F1F5","png":"https://static.abstractapi.com/country-flags/NP_flag.png","svg":"https://static.abstractapi.com/country-flags/NP_flag.svg"},"currency":{"currency_name":"Nepalese Rupee","currency_code":"NPR"},"connection":{"autonomous_system_number":45650,"autonomous_system_organization":"Vianet Communications Pvt. Ltd","connection_type":"Corporate","isp_name":"Vianet Communications Pvt. Ltd","organization_name":"Vianet"}}'
# [Finished in 3.4s]

# import requests

# response = requests.get("https	://ipgeolocation.abstractapi.com/v1/?api_key=b70d59041b71455ab753c78956f6a8b8&ip_address=103.10.29.126")
# print(response.status_code)
# print(response.conten)