import json
import random
import re
import time

import requests


def spider(beginDate, endDate, num):
    """

    :param beginDate: "2020.01.20"
    :param endDate: "2021.12.25"
    :param num:
    :return:
    """
    dateList = []
    date = "judgmentDate:["+beginDate+' TO '+endDate+']'
    dateList.append(date)


   # "filterDates": ["judgmentDate:[2020.02.05 TO 2022.01.06]"]
    Cookies = ['autologin=true; username=2034885420@qq.com; userConfig={"moduleList":[],"userStaffType":0,"isIpUser":0,"parentId":0,"sourceSiteUrl":null,"sourceSiteName":null,"clientSource":"自主注册","trial":true,"expire":false,"caseView":false,"advancedlSearchExpires":"2","proximateLatestExpires":"48","proximateSearch":false}; check=valid; TY_SESSION_ID=827ba7ea-6794-4eaf-abf1-8f66eb227b74; connect.sid=s:ZXBCNi-URL3-e59bSiqzeRJNCckhEXEX.zuDa4MclAW4qWi4yAyCr88dNkXS19xsGOxBGpudIEYk; userInfo={"id":"1000290499","username":"2034885420@qq.com","password":"0x02000000511ec6b5b749cd46de1cf27e985d76cd0b5f608d2d7f8172158330542a1718a781d215aaee94b1de4b5377df41109118","userType":"normal","email":"2034885420@qq.com","userLang":"cn","userPageSize":25,"isSend":true,"sendLang":"cn","recieveEmails":[],"groupName":"law","libraryCode":"law,taa,hr,HKBold","licences":1,"telephone":"18355442634","conf":""}; loginin=true; loginId=e6029baaa3b9484eb96ecf84287938f6; acw_tc=78e2b62616426938197051079e9f34ff3064942aaf94eb0cf973020c11; Hm_lpvt_fecce484974a74c6d10f421b6d3bd395=',
               'check=valid; TY_SESSION_ID=346b2eee-b5d7-4e77-8e10-fd5498f42ede; autologin=true; username=632101734@qq.com; acw_tc=78cebd9816427533357544001e2808a8cd92fc1f6388c9ef189f60038f; connect.sid=s:Z3qGUVaiBnAsqnk40KZY5ELvtrB3GHCv.L4+emsCG+duBmRk5BwwAH0M2VyyE5yjj+/7BXr5flHg; userInfo={"id":"1000290723","username":"632101734@qq.com","password":"0x020000003092368a749aa28c92e2afa813943ebb1d1d136f1baa5e9a3533b889a410991b300166b336538414650dec260dcf5280","userType":"normal","email":"632101734@qq.com","userLang":"cn","userPageSize":25,"isSend":true,"sendLang":"cn","recieveEmails":[],"groupName":"law","libraryCode":"law,taa,hr,HKBold","licences":1,"telephone":"18169538061","conf":""}; loginin=true; loginId=298901ca248749449df3198c9dba1df4; userConfig={"moduleList":[],"userStaffType":0,"isIpUser":0,"parentId":0,"sourceSiteUrl":null,"sourceSiteName":null,"clientSource":"自主注册","trial":true,"expire":false,"caseView":false,"advancedlSearchExpires":"2","proximateLatestExpires":"48","proximateSearch":false}; Hm_lvt_fecce484974a74c6d10f421b6d3bd395=1642745554,1642747324,1642753336,1642753375; Hm_lpvt_fecce484974a74c6d10f421b6d3bd395='
            ]

    cookie = random.choice(Cookies)

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Appversion': '2021.03.17.1',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=utf-8',
        'Cookie': (cookie+str(int(time.time()))).encode('utf-8'),
        'Host': 'law.wkinfo.com.cn',
        'Identification': '_2a66579079e311ecbc3ba7fea9a4723d',
        'Referer': 'https://law.wkinfo.com.cn/judgment-documents/list?mode=advanced',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'X-Tingyun-Id': 'tN6Win9ZeY4;r=96286256',
    }

    params = {
        "indexId": "law.case",
        "query": {
            "queryString": "typeOfCase:刑事 AND typeOfDecision:((001))",
            "filterQueries": [],
            "filterDates": dateList
        },
        "searchScope": {"treeNodeIds": []},
        "relatedIndexQueries": [],
        "sortOrderList": [{"sortKey": "judgmentDate", "sortDirection": "DESC"}],
        "pageInfo": {"limit": int(num), "offset": 0},
        "otherOptions": {
            "requireLanguage": "cn",
            "relatedIndexEnabled": False,
            "groupEnabled": False,
            "smartEnabled": True,
            "buy": False,
            "summaryLengthLimit": 100,
            "advanced": True,
            "synonymEnabled": True,
            "isHideBigLib": 0,
            "relatedIndexFetchRows": 5,
            "proximateCourtID": "",
            "module": ""
        },
        "chargingInfo": {"useBalance": True}}

    url = 'https://law.wkinfo.com.cn/csi/search'
    result = requests.session().post(url, headers=headers, json=params)

    if result.status_code == 200:
        content = result.content
        print(content)
        return htmlParser(content)
    else:
        print(result.content.decode('utf-8'))
        return []


def htmlParser(content):
    titleList = []
    contentDict = json.loads(content,strict=False)
    documentList = contentDict['documentList']
    for i in range(len(documentList)):
        titleList.append(wenshuDownload(documentList[i]))
    return titleList

def wenshuDownload(document):
    title = document['title']
    additionalFields = document['additionalFields']
    res = title + '\r'
    for key,value in additionalFields.items():
        if key == "judgmentDate":
            continue
        if key == "instancecode":
            continue
        if key == "referenceLevel":
            continue
        if key == "updateContentStatus":
            continue
        if key == "product":
            continue
        if value == None:
            continue
        if value=='':
            continue

        r = re.compile(r'\s+')
        value = r.sub("\r", value)
        res+=value
    path = r'static/Downloads/'+title+'.txt'
    with open(path,'w',encoding='utf-8') as file:
        file.write(res)
    return title

if __name__ == '__main__':
    beginDate = "2020.01.01"
    endDate = "2022.01.21"
    num = "5"
    print(spider(beginDate,endDate,num))
    #content='{"searchMetadata":{"searchId":"3d195bd52c634eef8a340e29988ea463","docCount":1182708,"costs":[{"title":"PREPARE","cost":48},{"title":"SOLR_Q_1","cost":286},{"title":"SOLR_E_1","cost":391},{"title":"SOLR_R_1","cost":452},{"title":"SEARCH","cost":1890},{"title":"RELATE_SEARCH","cost":1890},{"title":"DOC_AUTH","cost":1978},{"title":"TOTAL","cost":2018}],"filterTrees":null,"relatedTerms":null,"searchField":null,"isAccurate":null,"limitCount":5000,"isCache":false,"expire":false},"documentList":[{"docId":"MjAzNTc1NTI0NDU=","title":"刘国扬故意伤害刑事一审刑事判决书","subTitle":null,"summary":"沈阳市沈河区人民法院\r刑事判决书\r（2021）辽0103刑初821号\r公诉机关沈阳市沈河区人民检察院。\r被告人刘国扬，男，1995年3月4日出生于河南省濮阳市，汉族，中专文化，无职业，现住河南省濮阳市...","docType":"case","docOrdinal":1,"createTime":null,"modifiedTime":null,"lang":"cn","author":null,"count":null,"permit":true,"score":1.4142135,"attention":false,"translations":[],"additionalFields":{"judgmentDate":"2022.01.04","caseClaim1":"","caseDetail":"书\r（2021）辽0103刑初821号\r公诉机关沈阳市沈河区人民检察院。\r被告人刘国扬，男，1995年3月4日出生于河南省濮阳市，汉族，中专文化，无职业，现住河南省濮阳市清丰县。因涉嫌故意伤害罪于2021年9月13日被刑事拘留，同年9月23日被依法逮捕。现羁押于沈阳市沈河区看守所。\r沈阳市沈河区人民检察院以沈河检公诉刑诉[2021]110号起诉书指控被告人刘国扬犯故意伤害罪，于2021年12月1日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。沈阳市沈河区人民检察院指派检察员高嵩出庭支持公诉。被告人刘国扬到庭参加诉讼。现已审理终结。\r经审理查明，2021年7月18日11时许，在沈阳市沈河区，被告人刘国扬与被害人史某均为在御景中心售楼处的装修工人，刘国扬与史某因琐事发生纠纷，史某被刘国扬推倒致伤。经鉴定，被害人史某的损伤程度为轻伤二级。\r上述事实，被告人刘国扬在开庭审理过程中均无异议，且有案件来源、抓捕经过、电话查询记录、常住人口信息表、辨认笔录，被害人史某的陈述，证人刘某1、祝某、刘某2的证言，被告人刘国扬的供述及司法鉴定意见书等证据材\r料，经庭审举证、质证，足以证明。\r","caseOverview":"","caseClaim3":"","judgmentResult":"：\r被告人刘国扬犯故意伤害罪，判处有期徒刑六个月，缓刑一年。\r（缓刑考验期从判决确定之日起计算。）\r如不服本判决，可在接到判决书的第二日起十日内，通过本院或者直接向沈阳市中级人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本二份。\r审　判　长　　刘　洋\r人民陪审员　　张宗瑞\r人民陪审员　　郑秀丽\r二〇二二年一月四日\r\n","caseClaim2":"","documentNumber":"(2021)辽0103刑初821号","instancecode":"001","judgedResultDatabase":"被告人刘国扬犯故意伤害罪，判处有期徒刑六个月，缓刑一年。\r\n（缓刑考验期从判决确定之日起计算。）","court2Judgement":"","trialProcess":"沈阳市沈河区人民检察院以沈河检公诉刑诉[2021]110号起诉书指控被告人刘国扬犯故意伤害罪，于2021年12月1日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。沈阳市沈河区人民检察院指派检察员高嵩出庭支持公诉。被告人刘国扬到庭参加诉讼。现已审理终结。","referenceLevel":"99","court1Judgement":"","updateContentStatus":"00000001","product":"BLNCETCA,BLNCETCB,BLPB,BLPN,BLPNA,BLPNB,BLPNC,BLPNCA,BLPNCB,BLPNCC,BLPNCCA,BLPNCCB,BLPNCE,BLPNCEA,BLPNCEB,BLPNCEC,BLPNCECA,BLPNCECB,BLPNCET,BLPNCETA,BLPNCETB,BLPNCETC,BLPNCZ,BLPNCZA,BLPNCZB,BLPNCZE,BLPNCZEA,BLPNCZEB,BLPNEC,BLPNECA,BLPNECB,BOLD,SCNCASE","courtFoundOut1":"","courtFoundOut2":"","focusOfDispute":"","courtFoundOut3":"经审理查明，2021年7月18日11时许，在沈阳市沈河区，被告人刘国扬与被害人史某均为在御景中心售楼处的装修工人，刘国扬与史某因琐事发生纠纷，史某被刘国扬推倒致伤。经鉴定，被害人史某的损伤程度为轻伤二级。\r\n上述事实，被告人刘国扬在开庭审理过程中均无异议，且有案件来源、抓捕经过、电话查询记录、常住人口信息表、辨认笔录，被害人史某的陈述，证人刘某1、祝某、刘某2的证言，被告人刘国扬的供述及司法鉴定意见书等证据材\r\n料，经庭审举证、质证，足以证明。","judgedReasonDatabase":"本院认为，被告人刘国扬故意伤害他人身体，造成他人轻伤的后果，其行为侵犯了公民的身体健康权，已经构成故意伤害罪。公诉机关指控被告人刘国扬犯故意伤害罪的罪名成立，本院予以支持。被告人刘国扬经公安机关电话传唤主动到案，并如实供述犯罪事实，系自首，且认罪认罚，依法可从轻处罚。被告人刘国扬能够积极赔偿被害人经济损失，获得被害人的谅解，可酌情从轻处罚。被告人刘国扬的居住地司法局同意对其社区矫正，适用缓刑不致再危害社会，故对其从轻处罚，并适用缓刑。依照《中华人民共和国刑法》第二百三十四条第一款、第六十七条第一款、第七十二条第一款的规定，判决如下：","judgmentReason":"，被告人刘国扬故意伤害他人身体，造成他人轻伤的后果，其行为侵犯了公民的身体健康权，已经构成故意伤害罪。公诉机关指控被告人刘国扬犯故意伤害罪的罪名成立，本院予以支持。被告人刘国扬经公安机关电话传唤主动到案，并如实供述犯罪事实，系自首，且认罪认罚，依法可从轻处罚。被告人刘国扬能够积极赔偿被害人经济损失，获得被害人的谅解，可酌情从轻处罚。被告人刘国扬的居住地司法局同意对其社区矫正，适用缓刑不致再危害社会，故对其从轻处罚，并适用缓刑。依照《中华人民共和国刑法》第二百三十四条第一款、第六十七条第一款、第七十二条第一款的规定，","causeOfActionText":"刑事/侵犯公民人身权利、民主权利罪/故意伤害罪","legislationIDsCitedText":null,"notificationOfRights":"如不服本判决，可在接到判决书的第二日起十日内，通过本院或者直接向沈阳市中级人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本二份。","courtText":"辽宁省沈阳市沈河区人民法院","articleMainPoints":"","navigUrl":""},"promulgatingHistoryList":[],"contentAnnotationList":[],"pointAuthorAndOrganList":null,"coreWords":null,"explains":[]},{"docId":"MjAzNTczNDYyNjA=","title":"李某某故意伤害罪、故意伤害罪刑事一审刑事判决书","subTitle":null,"summary":"湖南省邵阳市双清区人民法院\r刑事判决书\r（2021）湘0502刑初468号\r公诉机关湖南省邵阳市双清区人民检察院。\r被告人李某某，男性，1963年4月11日出生，汉族，初中文化，无业，户籍所在地湖南省...","docType":"case","docOrdinal":2,"createTime":null,"modifiedTime":null,"lang":"cn","author":null,"count":null,"permit":true,"score":1.4142135,"attention":false,"translations":[],"additionalFields":{"judgmentDate":"2021.12.31","updateContentStatus":"00000001","caseDetail":"书\r（2021）湘0502刑初468号\r公诉机关湖南省邵阳市双清区人民检察院。\r被告人李某某，男性，1963年4月11日出生，汉族，初中文化，无业，户籍所在地湖南省邵阳市双清区。因涉嫌故意伤害罪，于2021年9月8日被邵阳市公安局双清分局刑事拘留，经邵阳市双清区人民检察院批准，于2021年10月12日被邵阳市公安局双清分局执行逮捕。现羁押于邵阳市看守所。\r湖南省邵阳市双清区人民检察院以双检刑检刑诉[2021]Z283号起诉书指控被告人李某某犯故意伤害罪，于2021年12月3日向本院提起公诉。本院即日受理后，依法组成合议庭，适用普通程序公开开庭审理了本案。邵阳市双清区人民检察院指派检察员徐小林出庭支持公诉，被告人李某某到庭参加诉讼。本案现已审理终结。\r公诉机关指控，2015年3月9日下午4时许，被害人肖文杰到棚户区改造项目部办公室找刘传学（已判决）谈按股清算事宜，要求刘传学对其股份拿个说法，刘传学不予理会，因而发生争执，肖文杰及其带来的十几名年轻伢子即对刘传学的办公室进行打砸，打砸完后肖文杰带来的年轻伢子就驾车离开，肖文杰则继续留下来理论，刘龙丹（已判决）则离开办公室到自己住的房子里拿来一把切西瓜的长刀，和被告人李某某一起来到现场，肖文杰当时就被刘传学、李**、罗志君等人围在现场，刘传学见刘龙丹等人进来则喊一声“打”，当即操起茶几上的玻璃烟灰缸砸向肖文杰的头部，刘龙丹则冲上去用刀背朝肖文杰头、胸、背部砍去，李某某也朝肖文杰的腹部踩了两脚。经鉴定，刘传学等人的行为致肖文杰轻伤二级。公诉机关提交了：1、住院就医记录、刑事和解书、抓获经过、户籍资料；2、证人刘传学、段文瑜、李**、罗志君、王青的证言；3、被害人肖文杰的陈述；4、被告人李某某的供述与辩解；5、被害人肖文杰的伤情鉴定；6、光盘一张等证据证实。\r公诉机关认为，被告人李某某故意伤害他人身体健康并致人轻伤，其行为已触犯《中华人民共和国刑法》第二百三十四条第一款，犯罪事实清楚，证据确实、充分，应当以故意伤害罪追究其刑事责任。被告人李某某在共同犯罪中起次要作用，系从犯，有坦白、自愿认罪认罚情节，还应当适用《中华人民共和国刑法》第二十五条第一款、第二十七条第一款、第二款、第六十七条第三款、《中华人民共和国刑事诉讼法》第十五条的规定。公诉机关当庭调整后的量刑建议为：可以在有期徒刑一年的基础上进行减轻，也可对被告人李某某是否适用缓刑进行适当考虑。\r被告人李某某对指控事实、罪名及量刑建议没有异议且自愿认罪认罚，在开庭审理过程中亦无异议，并请求对其从轻处罚。\r经审理查明，2015年3月9日下午4时许，被害人肖文杰到棚户区改造项目部办公室找刘传学（已判决）谈按股清算事宜，要求刘传学对其股份拿个说法，刘传学不予理会，因而发生争执，肖文杰及其带来的十几名年轻伢子即对刘传学的办公室进行打砸，打砸完后肖文杰带来的年轻伢子就驾车离开，肖文杰则继续留下来理论，刘龙丹（已判决）则离开办公室到自己住的房子里拿来一把切西瓜的长刀，和被告人李某某一起来到现场，肖文杰当时就被刘传学、李**、罗志君等人围在现场，刘传学见刘龙丹等人进来则喊一声“打”，当即操起茶几上的玻璃烟灰缸砸向肖文杰的头部，刘龙丹则冲上去用刀背朝肖文杰头、胸、背部砍去，李某某也朝肖文杰的腹部踩了两脚。经鉴定，刘传学等人的行为致肖文杰轻伤二级。经公安民警电话联系，李某某于2021年9月8日上午10时许主动到公安机关配合调查，并对自己故意伤害他人的犯罪事实供认不讳。2021年12月8日，被告人李某某与被害人肖文杰达成刑事和解，并由被害人肖文杰出具《刑事谅解书》，自愿对被告人李某某的犯罪行为予以谅解，并请求法院对被告人李某某减轻处罚。\r上述事实有经庭审质证、确认的：1、住院就医记录、刑事和解书、抓获经过、户籍资料；2、证人刘传学、段文瑜、李**、罗志君、王青的证言；3、被害人肖文杰的陈述；4、被告人李某某的供述与辩解；5、被害人肖文杰的伤情鉴定；6、光盘一张等证据证实，足以认定。\r","judgmentResult":"：\r被告人李某某犯故意伤害罪，判处拘役四个月。\r（刑期从判决执行之日起计算。判决执行前先行羁押的，羁押一日折抵刑期一日，即从2021年9月8日起至2022年1月7日止。）\r如不服本判决，可在接到判决书的第二日起十日内，通过本院或直接向湖南省邵阳市中级人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本二份。\r审　判　长　　魏永耀\r人民陪审员　　刘　洁\r人民陪审员　　羊钢键\r二〇二一年十二月三十一日\r\n","product":"BLNCETCA,BLNCETCB,BLPB,BLPN,BLPNA,BLPNB,BLPNC,BLPNCA,BLPNCB,BLPNCC,BLPNCCA,BLPNCCB,BLPNCE,BLPNCEA,BLPNCEB,BLPNCEC,BLPNCECA,BLPNCECB,BLPNCET,BLPNCETA,BLPNCETB,BLPNCETC,BLPNCZ,BLPNCZA,BLPNCZB,BLPNCZE,BLPNCZEA,BLPNCZEB,BLPNEC,BLPNECA,BLPNECB,BOLD,SCNCASE","documentNumber":"(2021)湘0502刑初468号","instancecode":"001","judgmentReason":"，被告人李某某故意伤害他人身体健康并致人轻伤，其行为已触犯《中华人民共和国刑法》第二百三十四条第一款之规定，构成故意伤害罪。公诉机关指控被告人李某某犯故意伤害罪的罪名成立，本院予以确认。被告人李某某在共同犯罪中起次要作用，系从犯，根据《中华人民共和国刑法》第二十五条第一款、第二十七条之规定，应当从轻处罚。被告人李某某经公安民警联系，主动至公安机关接受调查并如实供述自己的罪行，系自首，根据《中华人民共和国刑法》第六十七条第一款之规定，可以从轻处罚。被告人李某某自愿认罪认罚，根据《中华人民共和国刑事诉讼法》第十五条之规定，可以从宽处理。被告人李某某积极赔偿被害人损失，取得被害人谅解，本院酌情从轻处罚。综上，依照《中华人民共和国刑法》第二百三十四条第一款、第二十五条第一款、第二十七条、第六十七条第一款以及《中华人民共和国刑事诉讼法》第十五条之规定，","referenceLevel":"99","causeOfActionText":"刑事/侵犯公民人身权利、民主权利罪/故意伤害罪","legislationIDsCitedText":null,"courtText":"湖南省邵阳市双清区人民法院","articleMainPoints":"","navigUrl":""},"promulgatingHistoryList":[],"contentAnnotationList":[],"pointAuthorAndOrganList":null,"coreWords":null,"explains":[]}],"resultGroups":[],"relatedIndexCountList":[]}'
    #htmlParser(content)
