import requests
from datetime import date, datetime
import xmltodict
import json

today = datetime.today()
today_string = datetime.strftime(today, '%d-%m-%Y')

URL = 'https://danhmuchanhchinh.gso.gov.vn/DMDVHC.asmx?wsdl'

PROVINCE_HEADERS = {
    'Content-Type': 'text/xml',
    'SOAPAction': "http://tempuri.org/DanhMucTinh"
} 
PROVINCE_BODY = (f''
'<?xml version="1.0" encoding="utf-8"?>'
'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
'  <soap:Body>'
'    <DanhMucTinh xmlns="http://tempuri.org/">'
f'      <DenNgay>{today_string}</DenNgay>'
'    </DanhMucTinh>'
'  </soap:Body>'
'</soap:Envelope>'
)

DISTRICT_HEADERS = {
    'Content-Type': 'text/xml',
    'SOAPAction': "http://tempuri.org/DanhMucQuanHuyen"
} 

DISTRICT_BODY = (''
'<?xml version="1.0" encoding="utf-8"?>'
'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
'  <soap:Body>'
'    <DanhMucQuanHuyen xmlns="http://tempuri.org/">'
f'      <DenNgay>{today_string}</DenNgay>'
#'      <Tinh>27</Tinh>'
#'      <TenTinh>Tỉnh Hải Dương</TenTinh>'
'    </DanhMucQuanHuyen>'
'  </soap:Body>'
'</soap:Envelope>'
)

WARD_HEADERS = {
    'Content-Type': 'text/xml',
    'SOAPAction': "http://tempuri.org/DanhMucPhuongXa"
} 

WARD_BODY = (f''
'<?xml version="1.0" encoding="utf-8"?>'
'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
'  <soap:Body>'
'    <DanhMucPhuongXa xmlns="http://tempuri.org/">'
f'      <DenNgay>{today_string}</DenNgay>'
#'      <Tinh>string</Tinh>'
#'      <TenTinh>string</TenTinh>'
#'      <QuanHuyen>string</QuanHuyen>'
#'      <TenQuanHuyen>string</TenQuanHuyen>'
'    </DanhMucPhuongXa>'
'  </soap:Body>'
'</soap:Envelope>'
)

def return_value_with_key(root : dict, key: str):
    result = None
    
    if type(root) is not dict:
        return result
    
    for k, v in root.items():
        if k == key:
            return v
        else:
            result = return_value_with_key(v, key=key)
            if result is not None:
                return result
    return result


def get_danhmuchanhchinh_response(
    body : str,
    headers : str,
    url : str = URL
) -> requests.Response:
    """
    Retrieve utf-8 decoded content of response from DanhMucHanhChinh API
    based on passed-in body and header post.
    """

    try:
        response = requests.post(url,data=body,headers=headers)
    except Exception as e:
        print(f"error {e} in get_province()")
    else:
        return response.content.decode("utf-8")

def parse_province_content(province_content):
    province_content_dict = xmltodict.parse(province_content)
    province_dict = return_value_with_key(root=province_content_dict, key='TABLE')

    provinces = []
    for item in province_dict:
        province = {}

        keys = ("TenTinh", "LoaiHinh", "MaTinh", "@msdata:rowOrder", "@diffgr:id")
        for key in item:
            if key not in keys:
                print(f"found weird key: {key}")
                print(f"    with values: {item[key]}")

        province["name"] = item["TenTinh"]
        province["type"] = item["LoaiHinh"]
        province["service_key"] = item["MaTinh"]
        province["service_order"] = item["@msdata:rowOrder"]
    
        provinces.append(province)

    return provinces

def get_everything():
    """
    Get the most complete responses from DanhMucHanhChinh API for 
    all administrative subdivisions. parse response and save content
    into json format.
    """
    # get province
    province_content = get_danhmuchanhchinh_response(PROVINCE_BODY, PROVINCE_HEADERS)
    provinces = parse_province_content(province_content)
    with open('provinces.json', 'w', encoding='utf8') as provinces_json_name:
        json.dump(provinces, provinces_json_name, ensure_ascii=False, indent=4)

    
    # # get district
    # district_content = get_danhmuchanhchinh_response(DISTRICT_BODY, DISTRICT_HEADERS)
    # districts = parse_district_content(province_content)
    
    # # get wards
    # ward_content = get_danhmuchanhchinh_response(WARD_BODY, WARD_HEADERS)
    # wards = parse_ward_content(province_content)


get_everything()