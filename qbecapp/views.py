from django.shortcuts import render,redirect
import pandas as pd
from .models import Data
# Create your views here.
filename = ""
chno = ""
data = ""
ch = ""
que = ""
ans = ""
opt1 = ""
opt2 = ""
opt3 = ""
opt4 = ""
quelen = ""
data = ""
def base(request):
    if request.method == "GET":
        return render(request,"base.html")
    else:
        file = request.POST['ifile']
        chno = request.POST['chno']
        # print(file)
        Data(file=file).save()
        data = Data.objects.all()
        # print(len(data))
        file_url = ""
        for item in data:
            file_url = item.file.url
        return redirect(f'/card/?filename={file_url}&chno={chno}')
        # return render(request,"base.html")
         
def card(request):
    global filename,chno,data,ch,que,ans,opt1,opt2,opt3,opt4,quelen,data
    if request.method == "GET":
        filename = request.GET.get('filename')
        chno = request.GET.get('chno')
        data = read(filename[1:])
        ch = data["ch_no"].loc[data["ch_no"]==chno].to_list()
        # ch = data["index"].loc[data["ch_no"]=="1"].to_list()
        que = data["que"].loc[(data["ch_no"]==chno) & (data["opt1"].notna())].to_list()
        ans = data["ans"].loc[(data["ch_no"]==chno) & (data["opt1"].notna())].to_list()
        opt1 = data["opt1"].loc[(data["ch_no"]==chno) & (data["opt1"].notna())].to_list()
        opt2 = data["opt2"].loc[(data["ch_no"]==chno) & (data["opt1"].notna())].to_list()
        opt3 = data["opt3"].loc[(data["ch_no"]==chno) & (data["opt1"].notna())].to_list()
        opt4 = data["opt4"].loc[(data["ch_no"]==chno) & (data["opt1"].notna())].to_list()
        quelen = len(opt1)
        data = zip(ch,que,ans,opt1,opt2,opt3,opt4,[x for x in range(quelen)])
        print(len(opt1))
        return render(request,"card.html",{"data":data,"quelen":quelen})
    else:
        data_length = request.POST["length"]
        result = {}
        correct = 0
        for i in range(int(data_length)):
            #  print(request.POST[])
             result[f"{que[i]}"] = [request.POST[f'opt{i}'],ans[i],opt1[i],opt2[i],opt3[i],opt4[i],i]
        for i in result.values():
            if str(i[0]).lower() == str(i[1]).lower():
                correct+=1
        return render(request,"result.html",{"result":result,"correct":correct})
def read(file):
    # with open("QB_COA_SEM-IV_2023 (1).csv") as file:
        global filename,chno,data,ch,qu,ans,opt1,opt2,opt3,opt4,quelen
        qb = pd.read_csv(file)
        # print(qb)
        qb.drop("Unnamed: 1",axis=1,inplace=True)
        qb.reset_index(inplace=True)
        data = rename(qb)
        return data

def rename(qb):
    qb.rename(columns={ "L.J Institute of Engineering and Technology, Ahmedabad. (COA) Question Bank (SEM-IV )":"ch_no","Unnamed: 2":"que","Unnamed: 3":"ans","Unnamed: 5":"opt1","Unnamed: 6":"opt2","Unnamed: 7":"opt3","Unnamed: 8":"opt4"},inplace=True)
    # print(qb.head())
    return qb
