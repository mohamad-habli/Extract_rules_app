from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
from nltk.tokenize import sent_tokenize
import json


def ruleextract(doc):

    doc = doc.lower()
    #get the dataset from excel sheet
    df = pd.read_csv('/home/appbuilder555/Extract_rules_app/new_rules.csv', encoding= 'unicode_escape')

    #devide the doc to sentences and preprocessing each sentence
    part_list = []
    sentences = sent_tokenize(doc)
    for sentence in sentences:
        sent = re.sub("[^0-9a-zA-Z.:$%]", " ", sentence)
        sent = re.sub('\s+',' ',sent)
        sent = "."+sent
        part_list.append(sent)

    #for cleaning the result
    one = '1'
    two = '2'
    cleanres = ['herein']

    row_list = []
    # loop to extract all matches senteance by sentence
    i = 0
    for i in range(len(df)):
        before = re.sub("[^0-9a-zA-Z.:$]", " ", str(df.loc[i,"Before"]).lower())
        after = re.sub("[^0-9a-zA-Z.:$]", " ", str(df.loc[i,"After"]).lower())
        fn = str(df.loc[i,"FeatureName"]).lower()
        fn = re.sub("\s\s+" , " ", fn)
        fn = fn.strip()
        for sent in part_list:
            if after == "nan" or before == "nan":
                continue
            else:
                    regex = re.compile('{}(.*?){}'.format(re.escape(before), re.escape(after)))
                    res = regex.findall(sent)
                    if len(res) == 1:
                        res = res[0]
                        res.rstrip().lstrip()
                        if res == "" or len(res) < 4 or row_list.count(fn) > 0:
                            continue
                        elif len(res) > 100:
                                resu = res
                                regex = re.compile('{}(.*)'.format(re.escape(before)))
                                res = regex.findall(res)
                                if len(res) > 0:
                                    res = res[0]
                                else:
                                    res = resu
                                res.rstrip().lstrip()
                                if len(res) < 200:
                                    dict1 = {'FeatureName':fn,'Output':res}
                                    row_list.append(dict1)
                        elif cleanres[0] in res:
                            a = re.search(cleanres[0], res)
                            res = res[0:a.start()]
                            dict1 = {'FeatureName':fn,'Output':res}
                            row_list.append(dict1)
                        else:
                            dict1 = {'FeatureName':fn,'Output':res}
                            row_list.append(dict1)
                    elif len(res) == 2:
                        if one in fn and two in fn:
                            res = res[0] + " | " + res[1]
                            res.rstrip().lstrip()
                            if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                                continue
                            elif len(res) > 100:
                                resu = res
                                regex = re.compile('{}(.*)'.format(re.escape(before)))
                                res = regex.findall(res)
                                if len(res) > 0:
                                    res = res[0]
                                else:
                                    res = resu
                                res.rstrip().lstrip()
                                if len(res) < 200:
                                    dict1 = {'FeatureName':fn,'Output':res}
                                    row_list.append(dict1)
                            elif cleanres[0] in res:
                                a = re.search(cleanres[0], res)
                                res = res[0:a.start()]
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                            else:
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                        elif one in fn:
                            res = res[0]
                            res.rstrip().lstrip()
                            if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                                continue
                            elif len(res) > 100:
                                resu = res
                                regex = re.compile('{}(.*)'.format(re.escape(before)))
                                res = regex.findall(res)
                                if len(res) > 0:
                                    res = res[0]
                                else:
                                    res = resu
                                res.rstrip().lstrip()
                                if len(res) < 200:
                                    dict1 = {'FeatureName':fn,'Output':res}
                                    row_list.append(dict1)
                            elif cleanres[0] in res:
                                a = re.search(cleanres[0], res)
                                res = res[0:a.start()]
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                            else:
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                        elif two in fn:
                            res = res[1]
                            res.rstrip().lstrip()
                            if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                                continue
                            elif len(res) > 100:
                                resu = res
                                regex = re.compile('{}(.*)'.format(re.escape(before)))
                                res = regex.findall(res)
                                if len(res) > 0:
                                    res = res[0]
                                else:
                                    res = resu
                                res.rstrip().lstrip()
                                if len(res) < 200:
                                    dict1 = {'FeatureName':fn,'Output':res}
                                    row_list.append(dict1)
                            elif cleanres[0] in res:
                                a = re.search(cleanres[0], res)
                                res = res[0:a.start()]
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                            else:
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                    elif len(res) > 2:
                        res = min(res, key=len)
                        res.rstrip().lstrip()
                        if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                            continue
                        elif len(res) > 100:
                                resu = res
                                regex = re.compile('{}(.*)'.format(re.escape(before)))
                                res = regex.findall(res)
                                if len(res) > 0:
                                    res = res[0]
                                else:
                                    res = resu
                                res.rstrip().lstrip()
                                if len(res) < 200:
                                    dict1 = {'FeatureName':fn,'Output':res}
                                    row_list.append(dict1)
                        elif cleanres[0] in res:
                            a = re.search(cleanres[0], res)
                            res = res[0:a.start()]
                            dict1 = {'FeatureName':fn,'Output':res}
                            row_list.append(dict1)
                        else:
                            dict1 = {'FeatureName':fn,'Output':res}
                            row_list.append(dict1)

    if len(row_list) > 1 :
        df_res = pd.DataFrame(row_list)
        df_res['length'] = df_res['Output'].str.len()
        df_res.sort_values('length', ascending=False, inplace=True)
        df_res.drop_duplicates(subset =['FeatureName'], keep = "last", inplace = True)
        #df_res.drop_duplicates(subset =['Output'], keep = "last", inplace = True)
        df_res.sort_index(inplace=True)
    return df_res





app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def extrcat():
    # handle the POST request
    if request.method == 'POST':
        doc = request.form.get('document')
        df = ruleextract(doc)
        result = df.to_json(orient='records')
        parsed = json.loads(result)
        return jsonify(parsed)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><h1>Contract Extractor API</h1></div>
               <div><label for="document">Copy The Contract Below</label><br>
               <textarea name="document" rows="20" cols="230" placeholder="Copy The Contract here..."></textarea></label></div>
               <input type="submit" value="Submit">
           </form>'''

@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''

# driver function
if __name__ == '__main__':

    app.run(debug = True)
