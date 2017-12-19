
import json

# first question: which region of Taiwan?
# text : payload
region_list = {'北部':'region_north',
               '中部':'region_middle',
               '南部':'region_south',
               '東部':'region_east'
               }
def quick_reply_json(dict):
    # input: dictionary with key: title = key; payload = value
    # output: json
    option_list = []
    for k, v in dict.items():
        option_list.append(
            {
            "content_type": "text",
            "title": k,
            "payload": v
            })
            
    return(option_list)
north_city = ['台北市', '新北市','桃園市', '新竹市','新竹縣', '宜蘭縣', '基隆市']
middle_city = ['台中市', '彰化縣','雲林縣','苗栗縣','南投縣']
south_city = ['高雄市', '台南市', '嘉義市','嘉義縣','屏東縣']
east_city = ['台東縣','花蓮縣','澎湖縣','金門縣','連江縣']

def list_to_dict(l, prefix):
    d = {}
    for i in l:
        d[i] =prefix+'_'+i
    return(d)

region_to_city = {'north': north_city,
                  'middle': middle_city,
                  'south': north_city,
                  'east': east_city
                  }

disp_type = ['不限','整層住家', '獨立套房', '分租套房','雅房']
size = ['不限','10 坪以下', '10~20坪']
floor = ['不限','1層', '2-6層', '6-12層', '12層以上']
elevator = ['是', '否']
rooftop = ['是', '否']
cook = ['是', '否']
budgetMax = ['5000','7000','9000','12000','16000', '20000', '50000', '我太有錢']
budegtMin = budgetMax


search_clean = ['要', '不要']
