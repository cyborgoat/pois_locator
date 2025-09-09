import requests
import time
import csv

# 替换为你自己的高德API Key
AMAP_KEY = "your_amap_api_key_here"

# 中国所有地级市列表（简化示例，完整列表需自行补充）
CITIES = [
    "北京市", "上海市", "广州市", "深圳市", "天津市", "重庆市",
    "成都市", "杭州市", "南京市", "武汉市", "西安市", "沈阳市",
    # ... 补充全国300+地级市
]

def get_bank_pois_by_city(city_name):
    page = 1
    results = []
    while True:
        url = f"https://restapi.amap.com/v3/place/text"
        params = {
            "key": AMAP_KEY,
            "keywords": "中国银行",
            "types": "银行",  # 可选，更精准
            "city": city_name,
            "offset": 25,     # 每页最大25条
            "page": page,
            "extensions": "all"
        }
        try:
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            if data.get("status") != "1":
                print(f"请求失败：{data.get('info')}")
                break

            pois = data.get("pois", [])
            if not pois:
                break

            for poi in pois:
                item = {
                    "name": poi.get("name"),
                    "address": poi.get("address"),
                    "location": poi.get("location"),  # 格式：经度,纬度
                    "tel": poi.get("tel", ""),
                    "cityname": poi.get("cityname", ""),
                    "adname": poi.get("adname", ""),  # 区县
                    "id": poi.get("id")
                }
                results.append(item)

            print(f"{city_name} - 第{page}页，获取{len(pois)}条")
            page += 1
            time.sleep(0.1)  # 避免触发限流

        except Exception as e:
            print(f"异常：{e}")
            break

    return results

# 主程序
all_pois = []
for city in CITIES:
    print(f"开始采集：{city}")
    pois = get_bank_pois_by_city(city)
    all_pois.extend(pois)
    print(f"✅ {city} 完成，累计 {len(all_pois)} 条")

# 保存为CSV
with open("boc_branches_china.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "address", "location", "tel", "cityname", "adname", "id"])
    writer.writeheader()
    writer.writerows(all_pois)

print(f"🎉 采集完成，共 {len(all_pois)} 条记录，保存至 boc_branches_china.csv")