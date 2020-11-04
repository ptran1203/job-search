import unidecode
import re
import nltk
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from word2vec import embedding
from nltk.tokenize import word_tokenize

API_KEY = "1DyQ69AJGu6chA2B306VDQ5Qiy4mT4eH8"
SALARY_UNITS = ["$", "USD", "TRIỆU", "TRIEU"]
SALARY_DETECT_TERM = ["SALARY", "LƯƠNG", "LUONG"]
# nltk.download("punkt")

host = "http://iseek.herokuapp.com"


def collect_data():
    sql = (
        "SELECT post_post.content,post_post.title,post_post.salary_range"
        " FROM post_post;"
    )
    url = host + "/api/rawsql?api_key={}&sql={}".format(API_KEY, sql)
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.text)
        print("Get {} records".format(len(data)))
    else:
        data = []
        print("Request failed with status code {}, {}".format(r.status_code, r.text))
    return data


def to_float(val):
    try:
        return float(val)
    except ValueError:
        return False


def _cleaned_num(val):
    return val.replace(".", "").replace(",", "")


def to_usd(val, vnd, scale):
    val = to_float(_cleaned_num(val))
    if val >= 1000000:
        return val * 0.000043
        scale = 1

    if val is False:
        return False

    if vnd:
        return val * 0.000043 * scale

    elif val < 100:
        return False

    return val


def get_scale_factor(val):
    if "TRIỆU" in val.upper() or "TRIEU" in val.upper():
        return 1e6

    if re.search(r"[0-9]+K", val) or re.search(r"[0-9]+M", val):
        return 1e3

    return 1


def get_salary(val):
    if not val or type(val) is not str:
        return []

    scale = get_scale_factor(val)
    is_vnd = not ("$" in val or "USD" in val.upper()) and any(
        [c in val.upper() for c in {"VND", "VNĐ", "TRIỆU", "TRIEU"}]
    )

    if not is_vnd and scale == 1e3:
        """
        UPTO 20M/tháng.
        Lương thỏa thuận. Từ 20M – 30M/tháng.
        """
        is_vnd = True

    vals = re.findall(r"[0-9.,]+", val)

    vals = list(filter(lambda x: _cleaned_num(x) != "", vals))

    if not vals:
        return []

    if len(vals) == 2:
        max_val, min_val = [
            to_usd(vals[0], is_vnd, scale),
            to_usd(vals[1], is_vnd, scale),
        ]
    else:
        max_val, min_val = [
            to_usd(vals[0], is_vnd, scale),
            to_usd(vals[0], is_vnd, scale),
        ]

    # print(max_val, min_val)

    if max_val is False:
        max_val = min_val
    elif min_val is False:
        min_val = max_val

    if max_val is False:
        return []

    return max_val, min_val


def clean_text(text):
    text = unidecode.unidecode(text.lower())
    tokens = word_tokenize(text)
    return [t for t in tokens if re.match(r"[^\W\d]*$", t)]


def _get_salaty_from_content(content):
    idx = -1
    for term in SALARY_DETECT_TERM:
        idx = content.upper().find(term)
        if idx != -1:
            salary = get_salary(content[idx : idx + 50])
            if not salary:
                pass
                # with open("content.txt", "a") as f:
                #     f.write(
                #         content[idx : idx + 50] + "\n{}\n---------\n".format(salary)
                #     )
            else:
                # with open("have_salary.txt", "a") as f:
                #     f.write(
                #         content[idx : idx + 50] + "\n{}\n---------\n".format(salary)
                #     )
                return salary

    return False


def parse(data, parse_all=True):
    trainX = []
    trainY = []
    for d in data:
        salary = d[2] or ""
        text = d[0] + " " + d[1]
        # vec = get_vector(text, False)
        salary = get_salary(salary)
        if not salary:
            if any(c in d[1].upper() for c in SALARY_UNITS):
                salary = get_salary(d[1])

        if not salary:
            salary = _get_salaty_from_content(d[0])

        if salary:
            trainX.append(clean_text(text))
            trainY.append(salary)

        if salary and salary[1] > 400000.0:
            print(d[1], salary)

    return trainX, trainY


def to_embedding(texts):
    r = []
    for txt in texts:
        r.append(embedding.text2vec(txt))

    return np.array(r)


if __name__ == "__main__":
    # data = collect_data()
    # with open("./temp.json", "w") as f:
    #     json.dump(data, f)

    with open("./temp.json", "r") as f:
        data = json.load(f)
    train_x, train_y = parse(data)

    train_x = to_embedding(train_x)
    train_y = np.array(train_y)
    # np.save("./temp_y.npy", train_y)
    # train_y = np.load("./temp_y.npy")
    print(train_y.shape)
    print(train_x.shape)
    max_salary = np.max(train_y)
    print("max_salary", max_salary)
    train_y = train_y / max_salary
    # sns.displot(train_y[:, 0], kind="kde")
    # sns.displot(train_y[:, 1], kind="kde")
    # plt.show()

    from sklearn.ensemble import RandomForestRegressor

    model = RandomForestRegressor(max_depth=2)
    model.fit(train_x, train_y)
    score = model.score(train_x, train_y)
    print(score)

    test_txt = """
    Top 3 Reasons To Join Us
Building super-app for e-businesses globally
Attractive incentive program
Performance review any time
Job Description
Design and build data pipeline that consume large dimensional structured, unstructured data.
Writes ETL processes, designs database systems and deploys/develops tools for real-time and offline analytic processing.
Collaborate and understand the requirements from Data Analyst/ Business Users and turn into technical insight.
Research new technologies/ methodologies which can be applied to improve business performance.
Your Skills and Experience
At least 2 years of experience in building ETL pipeline, Data Warehouse
Experience in processing data in DBMS (Mongo, MySQL, SQL Server)
Experience with SQL, Python, bash shell scripts
Experience with Spark and its features: Spark SQL, Spark streaming, structured streaming.
Experience with Linux servers
Nice - to - have: Experience in PHP (Laravel Framework)
E-commerce experience is a plus
Why You'll Love Working Here
Life at Epsilo

Health care (Aon Insurance), health check, full social, health & employment insurances
Activities: Happy hour, sport content, company trip, team building, year-end party
Award: the best employee
Training: on the job training, coaching
Allowance: parking, phone card, business expense
Others: Laptop, T-Shirts, handbook, door gifts
14 annual leaves per year
Competitive salary range
Working hour at Epsilo

Venue: District 1, HCMC
Mon - Fri
9h00 - 18h30, and break time 1h30
    """
    pred = model.predict(np.expand_dims(embedding.text2vec(test_txt), axis=0))
    print(pred * max_salary)

