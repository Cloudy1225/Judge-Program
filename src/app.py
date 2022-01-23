from flask import Flask, render_template, request
import jiebaAnalysis
import wenshu_spider

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def jiebas():
    if request.method == 'GET':
        return render_template('司法大数据自动化标注与分析.html', text='')  # 返回模板
    else:
        text = request.form.get('textArea')
        result = jiebaAnalysis.out(text)
        jieba1s = result.get('不涉及地点名词')
        jieba2s = result.get('涉及地点名词')
        jieba3s = result.get('案由')
        jieba4s = result.get('形容词')
        return render_template('司法大数据自动化标注与分析.html', text=text, jieba1s=jieba1s,jieba2s=jieba2s,jieba3s=jieba3s,jieba4s=jieba4s)

@app.route('/文书爬取', methods = ['GET','POST'])
def crawl():
    if request.method == 'GET':
        return render_template('司法大数据自动化标注与分析.html', text='')  # 返回模板
    else:
        beginDate = request.form.get('beginDate')
        endDate = request.form.get('endDate')
        num = request.form.get('num')
        #设置参数默认值
        if beginDate == "":
            beginDate = "2002.12.25"
        if endDate == "":
            endDate = "2021.12.25"
        if num == "":
            num = "10"
        titleList = wenshu_spider.spider(beginDate,endDate,num)
        return render_template('文书爬取.html', titles=titleList)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port = 5000)
