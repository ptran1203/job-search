import unidecode
import re
import nltk
import requests
import json
import numpy as np
import pickle
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestRegressor

try:
    from salary_estimation.word2vec import embedding
except ImportError:
    from word2vec import embedding

# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd

API_KEY = "1DyQ69AJGu6chA2B306VDQ5Qiy4mT4eH8"
SALARY_UNITS = ["$", "USD", "TRIỆU", "TRIEU"]
SALARY_DETECT_TERM = ["SALARY", "LƯƠNG", "LUONG"]
nltk.download("punkt")

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
    if "%" in val:
        return ""

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
    if "TRIỆU" in val.upper() or "TRIEU" in val.upper() or re.search(r"[0-9]+M", val):
        return 1e6

    if re.search(r"[0-9]+K", val):
        return 1e3

    return 1


def get_salary(val):
    if not val or type(val) is not str:
        return []

    scale = get_scale_factor(val)
    is_vnd = not ("$" in val or "USD" in val.upper()) and any(
        [c in val.upper() for c in {"VND", "VNĐ", "TRIỆU", "TRIEU"}]
    )

    if not is_vnd and scale == 1e6:
        """
        UPTO 20M/tháng.
        Lương thỏa thuận. Từ 20M – 30M/tháng.
        """
        is_vnd = True

    vals = re.findall(r"[0-9.,]+%?", val)

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
                with open("have_salary.txt", "a") as f:
                    f.write(
                        content[idx : idx + 50]
                        + "\n{} {}\n---------\n".format(
                            salary, get_scale_factor(content[idx : idx + 50])
                        )
                    )
                return salary

    return False


def get_year_exp(description):
    keywords = [
        "years of experience",
        "year of experience",
        "years experience",
        "year experience",
        "năm kinh nghiệm",
        "kinh nghiệm yêu cầu",
    ]
    for k in keywords:
        idx = description.find(k)
        if idx != -1:
            truncated = description[idx - 15 : idx + len(k) + 15].replace("\n", " ")
            rex = r"[0-9]+-?[0-9]+\+? {}".format(k.split(" ")[0])
            numbers = re.findall(rex, truncated)
            if numbers:
                # print(truncated, numbers)
                return numbers


def parse(data, parse_all=True):
    trainX = []
    trainY = []
    for d in data:
        desc, title, salary = d
        text = title + " " + desc
        salary = get_salary(salary)
        if not salary:
            if any(c in title.upper() for c in SALARY_UNITS):
                salary = get_salary(title)

        if not salary:
            salary = _get_salaty_from_content(desc)

        if salary:
            trainX.append(clean_text(text))
            trainY.append(salary)

        exp = get_year_exp(desc)
        if exp and salary:
            print(exp, salary, title)

    return trainX, trainY


def to_embedding(texts):
    r = []
    for txt in texts:
        r.append(embedding.text2vec(txt))

    return np.array(r)


def load_data(get_new=True):
    new_data = []
    if get_new:
        print("Fetch new data...")
        new_data = collect_data()

    with open("./salary_estimation/storage/temp.json", "r") as f:
        data = json.load(f)

    descriptions = set([d[0][:100] for d in data])
    count = 0
    for d in new_data:
        if d[0][:100] not in descriptions:
            data.append(d)
            count += 1

    print("Total: {}, {} new".format(len(data), count))

    if count:
        with open("./salary_estimation/storage/temp.json", "w") as f:
            json.dump(data, f)

    return data


if __name__ == "__main__":
    data = load_data(False)
    train_x, train_y = parse(data)

    train_x = to_embedding(train_x)
    train_y = np.array(train_y)

    max_salary = np.max(train_y)
    print("max_salary", max_salary)
    train_y = train_y / max_salary

    model = RandomForestRegressor(max_depth=3)
    model.fit(train_x, train_y)
    score = model.score(train_x, train_y)
    print(score)

    # pred = model.predict(np.expand_dims(embedding.text2vec(test_txt), axis=0))
    # print(pred * max_salary)

    # filename = "./salary_estimation/storage/model.pkl"
    # pickle.dump(model, open(filename, "wb"))
    # pickle.dump(max_salary, open("./salary_estimation/storage/maxval.pkl", "wb"))
