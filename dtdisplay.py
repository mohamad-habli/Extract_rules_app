import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import re
from nltk.tokenize import sent_tokenize



def ruleextract(doc):
    
    doc = doc.lower()
    #get the dataset from excel sheet
    df = pd.read_excel (r'Rules_enhanced.xlsx')
    
    #devide the doc to sentences and preprocessing each sentence
    part_list = []
    sentences = sent_tokenize(doc)
    for sentence in sentences:
        sent = re.sub("[^0-9a-zA-Z.:$]", " ", sentence)
        sent = re.sub('\s+',' ',sent)
        part_list.append(sent)
    
    #for cleaning the result
    one = '1'
    two = '2'
    cleanres = ['herein']
    
    row_list = []
    # loop to extract all matches senteance by sentence
    i = 0
    for i in range(93):    
        before = str(df.loc[i,"Before"]).lower()
        after = str(df.loc[i,"After"]).lower()
        fn = str(df.loc[i,"FeatureName"]).lower()
        fn = fn.strip()
        for sent in part_list:   
            if after == "nan":      
                continue
            else:  
                    regex = re.compile('{}(.*?){}'.format(re.escape(before), re.escape(after)))
                    res = regex.findall(sent)
                    if len(res) == 1:
                        res = res[0]
                        if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                            continue
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
                            if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                                continue
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
                            if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                                continue
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
                            if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                                continue
                            elif cleanres[0] in res:
                                a = re.search(cleanres[0], res)
                                res = res[0:a.start()]
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                            else:
                                dict1 = {'FeatureName':fn,'Output':res}
                                row_list.append(dict1)
                    elif len(res) > 2:
                        res = res[0]
                        if res == "" or len(res) > 200 or len(res) < 4 or row_list.count(fn) > 0:
                            continue
                        elif cleanres[0] in res:
                            a = re.search(cleanres[0], res)
                            res = res[0:a.start()]
                            dict1 = {'FeatureName':fn,'Output':res}
                            row_list.append(dict1)
                        else:
                            dict1 = {'FeatureName':fn,'Output':res}
                            row_list.append(dict1)
    
                    
    df_res = pd.DataFrame(row_list)    
    df_res['length'] = df_res['Output'].str.len()
    df_res.sort_values('length', ascending=False, inplace=True)       
    df_res.drop_duplicates(subset =['FeatureName'], keep = "last", inplace = True)
    df_res.sort_index(inplace=True)  
    return df_res

app = dash.Dash()
application = app.server

app.layout = html.Div([
    html.Div([
        dcc.Textarea(
            id='textarea-state-example',
            value='Textarea content initialized\nwith multiple lines of text',
            style={'width': '100%', 'height': 200},
        ),
        html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
        html.Div(id='textarea-state-example-output', style={'whiteSpace': 'normal'}),
    ]), html.Div([
    html.Div(id="table1", 
             style={'width': '75%', 'textAlign': 'left'})


    ]),    

])

@app.callback(Output('table1','children'),
              [Input('textarea-state-example-button', 'n_clicks')],
              [State('textarea-state-example', 'value')])

def update_datatable(n_clicks,value):            
    if n_clicks:                            
        df = ruleextract(value)
        data = df.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns,                style_header={'backgroundColor': "#FFD700",
                              'fontWeight': 'bold',
                              'textAlign': 'center',},
                style_table={'overflowX': 'scroll'},  
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[
                    {
                        'width': '30%',
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px',
                    }])


if __name__ == '__main__':
    application.run(debug=False, port=8080)

