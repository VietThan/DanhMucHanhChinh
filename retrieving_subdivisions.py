import requests
from datetime import date, datetime
import xmltodict

today = datetime.today()
today_string = datetime.strftime(today, '%d-%m-%Y')

URL = 'https://danhmuchanhchinh.gso.gov.vn/DMDVHC.asmx?wsdl'

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

def get_province() -> requests.Response:
    """

    """
    province_headers = {
        'Content-Type': 'text/xml',
        'SOAPAction': "http://tempuri.org/DanhMucTinh"
    } 

    province_body = (f''
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    '  <soap:Body>'
    '    <DanhMucTinh xmlns="http://tempuri.org/">'
    f'      <DenNgay>{today_string}</DenNgay>'
    '    </DanhMucTinh>'
    '  </soap:Body>'
    '</soap:Envelope>'
)
    try:
        province_response = requests.post(URL,data=province_body,headers=province_headers)
    except Exception as e:
        print(f"error {e} in get_province()")
    else:
        return province_response

def get_district() -> requests.Response:
    """

    """
    district_headers = {
        'Content-Type': 'text/xml',
        'SOAPAction': "http://tempuri.org/DanhMucQuanHuyen"
    } 

    district_body = (''
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    '  <soap:Body>'
    '    <DanhMucQuanHuyen xmlns="http://tempuri.org/">'
    '      <DenNgay>12-06-2022</DenNgay>'
    #'      <Tinh>27</Tinh>'
    #'      <TenTinh>Tỉnh Hải Dương</TenTinh>'
    '    </DanhMucQuanHuyen>'
    '  </soap:Body>'
    '</soap:Envelope>'
    )
    try:
        district_response = requests.post(URL,data=district_body,headers=district_headers)
    except Exception as e:
        print(f"error {e} in get_district()")
    else:
        return district_response

def get_ward() -> requests.Response:
    """

    """
    ward_headers = {
        'Content-Type': 'text/xml',
        'SOAPAction': "http://tempuri.org/DanhMucPhuongXa"
    } 

    ward_body = (f''
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
    try:
        ward_response = requests.post(URL,data=ward_body,headers=ward_headers)
    except Exception as e:
        print(f"error {e} in get_province()")
    else:
        return ward_response

def get_everything():
    province_content = get_province().content.decode("utf-8")
    district_content = get_district().content.decode("utf-8")
    ward_content = get_ward().content.decode("utf-8")


get_everything()