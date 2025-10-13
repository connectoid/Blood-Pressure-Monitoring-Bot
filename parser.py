import requests
from pprint import pprint


cookies = {
    'at_check': 'true',
    'affinity': '"0be9ad402a683356"',
    'TOYOTANATIONAL_PCO_PRIVACY_BannerSeen': '1',
    'TOYOTANATIONAL_PCO_PRIVACY_MODAL_VIEWED': '1',
    'tda': 'TRI10',
    'AMCVS_8F8B67C25245B30D0A490D4C%40AdobeOrg': '1',
    'cif.cartID': '7uICUyDbp4Fnd5kcBwCqxcVVYXUEAI2j',
    'cif.userToken': '',
    'AMCV_8F8B67C25245B30D0A490D4C%40AdobeOrg': '359503849%7CMCIDTS%7C20365%7CMCMID%7C37606111471573851892764764055902175924%7CMCAAMLH-1760064240%7C6%7CMCAAMB-1760064240%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1759466644s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1',
    'private_content_version': 'c9c6acfddcf4778b283414ed28e9730e',
    'user_email_id': '',
    'user_id': '',
    'user_logged_in_status': '0',
    'user_account_type': '',
    'tms_vi': '8312488202061496_6567974989139986',
    'tms_firstVisitEver': '1759459462147',
    'tms_isNew': 'true',
    'tms_c': 'test',
    'tms_kmd': '%7B%7D',
    'tms_kmv': '%7B%7D',
    'tms_visitList': '%7B%7D',
    'tms_visitReferrer': 'https%3A%2F%2Fkwork.ru%2F',
    's_cc': 'true',
    '_fbp': 'fb.1.1759459474870.963454701817911446',
    'TOYOTANATIONAL_PCO_PRIVACY_TargetingCookies': '1',
    'TOYOTANATIONAL_PCO_PRIVACY_FunctionalCookies': '1',
    'mbox': 'session#8bf5d02c151749b6be75c8bc50876a5f#1759461468',
    'tms_firstReferrer': '',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'content-type': 'application/json',
    'magento-customer-group': 'dealer_37172',
    'magento-store-code': 'main_website_store',
    'magento-store-view-code': 'default',
    'magento-website-code': 'base',
    'priority': 'u=1, i',
    'referer': 'https://autoparts.conicellitoyotaofspringfield.com/search?search_query=35678-33270',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'store': 'website_37172_en',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-request-id': '6b94b032-f586-4f1b-a8ef-9c7f971ec956',
    # 'cookie': 'at_check=true; affinity="0be9ad402a683356"; TOYOTANATIONAL_PCO_PRIVACY_BannerSeen=1; TOYOTANATIONAL_PCO_PRIVACY_MODAL_VIEWED=1; tda=TRI10; AMCVS_8F8B67C25245B30D0A490D4C%40AdobeOrg=1; cif.cartID=7uICUyDbp4Fnd5kcBwCqxcVVYXUEAI2j; cif.userToken=; AMCV_8F8B67C25245B30D0A490D4C%40AdobeOrg=359503849%7CMCIDTS%7C20365%7CMCMID%7C37606111471573851892764764055902175924%7CMCAAMLH-1760064240%7C6%7CMCAAMB-1760064240%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1759466644s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1; private_content_version=c9c6acfddcf4778b283414ed28e9730e; user_email_id=; user_id=; user_logged_in_status=0; user_account_type=; tms_vi=8312488202061496_6567974989139986; tms_firstVisitEver=1759459462147; tms_isNew=true; tms_c=test; tms_kmd=%7B%7D; tms_kmv=%7B%7D; tms_visitList=%7B%7D; tms_visitReferrer=https%3A%2F%2Fkwork.ru%2F; s_cc=true; _fbp=fb.1.1759459474870.963454701817911446; TOYOTANATIONAL_PCO_PRIVACY_TargetingCookies=1; TOYOTANATIONAL_PCO_PRIVACY_FunctionalCookies=1; mbox=session#8bf5d02c151749b6be75c8bc50876a5f#1759461468; tms_firstReferrer=',
}

params = {
    'query': '\n    query Products($sku: [String!]!) {\n        products(\n            filter: {\n                sku: { in: $sku }\n            }\n        ) {\n            items {\n                sku\n                id\n                name\n                uid\n                special_price\n                part_number\n                substitution_part_number\n                custom_attributes {\n                    attribute_code\n                    attribute_value\n                }\n            }\n        }\n    }\n',
    'variables': '{"sku":["3567833270"]}',
}

response = requests.get(
    'https://autoparts.conicellitoyotaofspringfield.com/api/graphql',
    params=params,
    cookies=cookies,
    headers=headers,
)

pprint(response.json()['data']['products']['items'][0]['id'])
pprint(response.json()['data']['products']['items'][0]['name'])
pprint(response.json()['data']['products']['items'][0]['part_number'])
pprint(response.json()['data']['products']['items'][0]['special_price'])
pprint(response.json()['data']['products']['items'][0]['substitution_part_number'])
pprint(response.json()['data']['products']['items'][0]['uid'])