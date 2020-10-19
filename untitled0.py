import pandas as pd
import numpy as np
#from datetime import datetime as dt
import datetime
import locale

pd.set_option("display.max_rows", 50)
data= pd.read_csv('data.csv')
data1  = data.copy()
#сортировка
data_sort1 = data1.sort_values(['salaryMAX','salaryMIN'], ascending=True)
#print(data_sort1[['address','salaryMAX']])
#разделение на 10 групп
unique=[]
for i in range(len(data_sort1['salaryMAX'].unique())-1):
    unique.append(int(data_sort1['salaryMAX'].unique()[i]))
#print(unique)
    
step = len(unique)//10    
for i in range(0, len(unique), step):
        range_salary = unique[i:i + step]
#        name_file = 'SalaryMAX('+ str(range_salary[0])+'-'+str(range_salary[-1])+').csv'
        bins =  np.arange(range_salary[0],range_salary[-1])
        df_filter = data_sort1['salaryMAX'].isin(bins)
        data_sort1[df_filter].to_csv(name_file)
#       названия вакансий и количество вхождений  
        print(data_sort1[df_filter]['name'].value_counts().to_frame().reset_index().rename(columns={'index':'вакансия', 'name':'количество'}))
        print()
#       среднее, максимальное и минимальное количество дней
        сount_day= []
        date_column = data_sort1[df_filter]['date'].copy()
        for dat in date_column:
            date_str = str(dat).replace("\xa0"," ").split()
            date_piblication_month = date_str[1]
            for new, old in [('января', '1'), ('февраля', '2'), ('марта', '3'), ('апреля', '4'), ('мая', '5'), ('июня', '6'), ('июля', '7'), ('августа', '8'), ('сентября', '9'), ('октября', '10'), ('ноября', '11'), ('декабря', '12')]:
                date_piblication_month = date_piblication_month.replace(new, old)
            difference = datetime.date(2020,10,18) - datetime.date(int(date_str[2]),int(date_piblication_month),int(date_str[0]))
            сount_day.append(difference.days)
        mini = min(сount_day)
        maxi = max(сount_day)
        mean = np.mean(сount_day)
        print('Минимум: ', mini , ' ,Максимум: ',maxi, ' ,Среднее: ',mean)
        print()

#       возможные значения требуемого опыта  и количество вхождений
        print(data_sort1[df_filter]['experience'].value_counts().to_frame().reset_index().rename(columns={'index':'опыт', 'experience':'количество'}))
        print()
#       возможные значения типов занятости и колияество
        print(data_sort1[df_filter]['type_of_employment'].value_counts().to_frame().reset_index().rename(columns={'index':'тип занятости', 'type_of_employment':'количество'}))
        print()
#       возможные значения рабочего графика и вхождения
        print(data_sort1[df_filter]['schedule'].value_counts().to_frame().reset_index().rename(columns={'index':'график', 'schedule':'количество'}))
        print()
#       ключевые навыки и количество вхождений
        print('Ключевые уникальные навыки ------ количество вхождений')

        skills_column = data_sort1[df_filter]['skills'].copy().astype(str)
        array_skill_all=[]
        array_skill_unique=[]
        for skill in skills_column:
            if skill!= 'nan':
                s = skill.split(',')
                for i in range(len(s)):
                    array_skill_all.append(s[i].replace('\xa0',''))
                array_skill_unique = set(array_skill_all)
        for sk in array_skill_unique:
            print(sk, '------' ,array_skill_all.count(sk) )
#            
print()
print()
############################################ЧАСТЬ 3#############################################3
#РАЗДЕЛИТЬ ПО ВАКАНСИЯМ
unique_name=data_sort1['name'].unique()
for i in unique_name:
    data_v = data_sort1.loc[data_sort1['name'] == i]
    #data_v=data_sort1.loc[data_sort1['name']=='Менеджер по продажам']
    #возможные значения максимальной и минимальной зарплаты и количество
    print(data_v['salaryMAX'].value_counts().to_frame().reset_index().rename(columns={'index':'МАКС', 'salaryMAX':'количество'}))
    print(data_v['salaryMIN'].value_counts().to_frame().reset_index().rename(columns={'index':'МИН', 'salaryMIN':'количество'}))
    #среднее, максимальное и минимальное количество дней
    date_column = data_v['date'].copy()
    сount_day=[]
    for dat in date_column:
        date_str = str(dat).replace("\xa0"," ").split()
        date_piblication_month = date_str[1]
        for new, old in [('января', '1'), ('февраля', '2'), ('марта', '3'), ('апреля', '4'), ('мая', '5'), ('июня', '6'), ('июля', '7'), ('августа', '8'), ('сентября', '9'), ('октября', '10'), ('ноября', '11'), ('декабря', '12')]:
            date_piblication_month = date_piblication_month.replace(new, old)
        difference = datetime.date(2020,10,18) - datetime.date(int(date_str[2]),int(date_piblication_month),int(date_str[0]))
        сount_day.append(difference.days)
    mini = min(сount_day)
    maxi = max(сount_day)
    mean = np.mean(сount_day)
    
    print(mini,maxi,mean)
    
    #значения требуемого опыта работы и количество вхождений
    print(data_v['experience'].value_counts().to_frame().reset_index().rename(columns={'index':'опыт', 'experience':'количество'}))
    #значения типов занятости и количество вхождений
    print(data_v['type_of_employment'].value_counts().to_frame().reset_index().rename(columns={'index':'тип занятости', 'type_of_employment':'количество'}))
    # значения рабочего графика и количество вхождений
    print(data_v['schedule'].value_counts().to_frame().reset_index().rename(columns={'index':'график', 'schedule':'количество'}))
    # уникальных ключевых навыков и количество вхождений
    skills_column = data_v['skills'].copy().astype(str)
    array_skill_all=[]
    array_skill_unique=[]
    for skill in skills_column:
        if skill!= 'nan':
            s = skill.split(',')
            for i in range(len(s)):
                array_skill_all.append(s[i].replace('\xa0',''))
            array_skill_unique = set(array_skill_all)
    for sk in array_skill_unique:
        print(sk, '------' ,array_skill_all.count(sk) )


    
