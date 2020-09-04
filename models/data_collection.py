import unidecode
from nltk.tokenize import word_tokenize
import re
import nltk
nltk.download('punkt')

host = 'http://iseek.herokuapp.com'

def collect_data():
    sql = ('SELECT post_post.content,post_post.title,post_post.salary_range'
        ' FROM post_post;')
    api_key = '1DyQ69AJGu6chA2B306VDQ5Qiy4mT4eH8'
    url = host + '/api/rawsql?api_key={}&sql={}'.format(api_key, sql)
    r = requests.get(url)
    data = json.loads(r.text)
    print(len(data))
    return data


def to_usd(val, vnd):
    val = float(val.replace('.', ''))
    if vnd:
        val *= 0.000043
    return val


def get_salary(val):
    val = val.replace(' triệu', '.000.000')
    is_vnd = not ('$' in val or 'USD' in val.upper())
    vals = re.findall(r'[0-9.]+', val)
    if len(vals) == 2:
        return [to_usd(vals[0], is_vnd), to_usd(vals[1], is_vnd)]
    return [to_usd(vals[0], is_vnd), to_usd(vals[0], is_vnd)]


def clean_text(text):
    text = unidecode.unidecode(text.lower())
    tokens = word_tokenize(text)
    return [t for t in tokens if re.match(r'[^\W\d]*$', t)]


def parse(data, parse_all=True):
    trainX = []
    trainY = []
    for d in data:
        salary = d[2]
        text = d[0] + ' ' + d[1]
        # vec = get_vector(text, False)
        if parse_all:
            trainX.append(clean_text(text))
        elif salary:
            trainX.append(clean_text(text))
            trainY.append(get_salary(salary))

    return trainX, trainY


# data = collect_data()
# train_text, _ = parse(data)

# with open("/content/job_desc.cor", "w") as f:
#     i = 0
#     for line in train_text:
#         i+=1
#         f.write(" ".join(line))
#         f.write("\n")
