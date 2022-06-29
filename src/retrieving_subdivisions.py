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

        province["province_name"] = item["TenTinh"]
        province["type"] = item["LoaiHinh"]
        province["province_service_key"] = item["MaTinh"]
        province["province_service_order"] = item["@msdata:rowOrder"]
    
        provinces.append(province)

    return provinces

def parse_district_content(district_content):
    district_content_dict = xmltodict.parse(district_content)
    district_dict = return_value_with_key(root=district_content_dict, key='TABLE')

    districts = []
    for item in district_dict:
        district = {}

        keys = ("MaTinh", "TenTinh", "MaQuanHuyen", "TenQuanHuyen", "LoaiHinh", "@msdata:rowOrder", "@diffgr:id")
        for key in item:
            if key not in keys:
                print(f"found weird key: {key}")
                print(f"    with values: {item[key]}")

        district["province_service_key"] = item["MaTinh"]
        district["province_name"] = item["TenTinh"]
        district["district_service_key"] = item["MaQuanHuyen"]
        district["district_name"] = item["TenQuanHuyen"]
        district["type"] = item["LoaiHinh"]
        district["province_service_order"] = item["@msdata:rowOrder"]
    
        districts.append(district)
        
    return districts

def parse_ward_content(ward_content):
    ward_content_dict = xmltodict.parse(ward_content)
    ward_dict = return_value_with_key(root=ward_content_dict, key='TABLE')

    wards = []
    for item in ward_dict:
        ward = {}

        keys = ("MaTinh", "TenTinh", "MaQuanHuyen", "TenQuanHuyen", "MaPhuongXa", "TenPhuongXa", "LoaiHinh", "@msdata:rowOrder", "@diffgr:id")
        for key in item:
            if key not in keys:
                print(f"found weird key: {key}")
                print(f"    with values: {item[key]}")

        ward["province_service_key"] = item["MaTinh"]
        ward["province_name"] = item["TenTinh"]
        ward["district_service_key"] = item["MaQuanHuyen"]
        ward["district_name"] = item["TenQuanHuyen"]
        ward["ward_service_key"] = item["MaPhuongXa"]
        ward["ward_name"] = item["TenPhuongXa"]
        ward["type"] = item["LoaiHinh"]
        ward["ward_service_order"] = item["@msdata:rowOrder"]
    
        wards.append(ward)
        
    return wards

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

    
    # get district
    district_content = get_danhmuchanhchinh_response(DISTRICT_BODY, DISTRICT_HEADERS)
    districts = parse_district_content(district_content)
    with open('districts.json', 'w', encoding='utf8') as district_json_name:
        json.dump(districts, district_json_name, ensure_ascii=False, indent=4)
    
    # get wards
    ward_content = get_danhmuchanhchinh_response(WARD_BODY, WARD_HEADERS)
    wards = parse_ward_content(ward_content)
    with open('wards.json', 'w', encoding='utf8') as ward_json_name:
        json.dump(wards, ward_json_name, ensure_ascii=False, indent=4)


get_everything()