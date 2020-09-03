import requests


r = requests.get("https://www.topcv.vn/tim-viec-lam-thi%E1%BA%BFt-k%E1%BA%BF-%C4%91%E1%BB%93-ho%E1%BA%A1-designer?salary=0&exp=0&company_field=0&page=1")

with open("zhtml.html", 'w') as f:
    f.write(r.text)