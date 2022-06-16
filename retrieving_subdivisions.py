import requests
from datetime import date, datetime
import xmltodict

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
'      <DenNgay>12-06-2022</DenNgay>'
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
    Retrieve utf-8 decoded content of response from DanhMucHanhChinh api
    based on passed in body and header post.
    """

    try:
        response = requests.post(url,data=body,headers=headers)
    except Exception as e:
        print(f"error {e} in get_province()")
    else:
        return response.content.decode("utf-8")

def get_everything():
    province_content = get_danhmuchanhchinh_response(PROVINCE_BODY, PROVINCE_HEADERS)
    district_content = get_danhmuchanhchinh_response(DISTRICT_BODY, DISTRICT_HEADERS)
    ward_content = get_danhmuchanhchinh_response(WARD_BODY, WARD_HEADERS)


get_everything()