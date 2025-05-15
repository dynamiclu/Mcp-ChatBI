from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Douyin-Open-API-Server")

"""
    这是一个demo的演示，对应tool的数据都是固定的。
    实际使用场景，可根据需求，配置相应的tool，可以查询数据库，也可调接口
"""

@mcp.tool(name="视频列表数据", description="查询视频列表, 返回视频标题、转发数、评论数、点赞数、下载数、播放数、分享数")
def video_list(open_id: str) -> dict:
    print("open_id:", open_id)
    response = {
        "extra": {
            "error_code": 0,
            "description": "",
            "sub_error_code": 0,
            "sub_description": "",
            "logid": "202008121419360101980821035705926A",
            "now": 1597213176393
        },
        "data": {
            "error_code": 0,
            "description": "",
            "has_more": False,
            "list": [
                {
                    "title": "测试视频1 #测试话题1 @抖音小助手",
                    "is_top": False,
                    "create_time": 1571075129,
                    "is_reviewed": True,
                    "video_status": 5,
                    "share_url": "https://www.iesdouyin.com/share/video/QDlWd0EzdWVMU2Q0aU5tKzVaOElvVU03ODBtRHFQUCtLUHBSMHFRT21MVkFYYi9UMDYwemRSbVlxaWczNTd6RUJRc3MrM2hvRGlqK2EwNnhBc1lGUkpRPT0=/?region=CN&mid=6753173704399670023&u_code=12h9je425&titleType=title",
                    "item_id": "@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==",
                    "media_type": 2,
                    "cover": "https://p3-dy.byteimg.com/img/tos-cn-p-0015/cfa0d6421bdc4580876cb16974539ff6~c5_300x400.jpeg",
                    "statistics": {
                        "forward_count": 100,
                        "comment_count": 1000,
                        "digg_count": 2000,
                        "download_count": 100,
                        "play_count": 30000,
                        "share_count": 1000
                    }
                },
                {
                    "title": "测试视频2 #测试话题2",
                    "is_top": False,
                    "create_time": 1571075130,
                    "is_reviewed": True,
                    "video_status": 5,
                    "share_url": "https://www.iesdouyin.com/share/video/QDlWd0EzdWVMU2Q0aU5tKzVaOElvVU03ODBtRHFQUCtLUHBSMHFRT21MVkFYYi9UMDYwemRSbVlxaWczNTd6RUJRc3MrM2hvRGlqK2EwNnhBc1lGUkpRPT0=/?region=CN&mid=6753173704399670023&u_code=12h9je425&titleType=title",
                    "item_id": "@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==",
                    "media_type": 2,
                    "cover": "https://p3-dy.byteimg.com/img/tos-cn-p-0015/cfa0d6421bdc4580876cb16974539ff6~c5_300x400.jpeg",
                    "statistics": {
                        "forward_count": 190,
                        "comment_count": 500,
                        "digg_count": 6001,
                        "download_count": 1210,
                        "play_count": 80400,
                        "share_count": 2600
                    }
                }
            ],
            "cursor": 0
        }
    }

    result = {
        "data_list": [
            {
                "title": "美猴王大闹天宫",
                "item_id": "@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==",
                "forward_count": 34200,
                "comment_count": 32401,
                "digg_count": 20040,
                "download_count": 98343,
                "play_count": 35645000,
                "share_count": 473080
            },
            {
                "title": "东海龙王藏金刚棒",
                "item_id": "@7hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x2w==",
                "forward_count": 13490,
                "comment_count": 54500,
                "digg_count": 604301,
                "download_count": 14210,
                "play_count": 80452400,
                "share_count": 234600
            },
            {
                "title": "中国粮食金融保护战",
                "item_id": "@9hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x9w==",
                "forward_count": 436000,
                "comment_count": 83662,
                "digg_count": 339000,
                "download_count": 23025,
                "play_count": 83020400,
                "share_count": 909600
            },
            {
                "title": "猫猫车诞生后，中国再无轻步兵",
                "item_id": "@10hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/10w==",
                "forward_count": 19024,
                "comment_count": 4539,
                "digg_count": 90001,
                "download_count": 671210,
                "play_count": 18304400,
                "share_count": 110000
            }
        ]
    }
    return result


@mcp.tool(name="视频点赞数据", description="视频点赞数据, 返回日期(date),点赞数(like)")
def item_like(open_id: str, item_id: str) -> dict:
    print("open_id:", open_id)
    result1 = {
        "data_list": [
            {
                "date": "2025-04-06",
                "like": 14260
            },
            {
                "date": "2025-04-07",
                "like": 15300
            },
            {
                "date": "2025-04-08",
                "like": 16320
            },
            {
                "date": "2025-04-09",
                "like": 17330
            },
            {
                "date": "2025-04-10",
                "like": 18380
            },
            {
                "date": "2025-04-11",
                "like": 16369
            },
            {
                "date": "2025-04-12",
                "like": 13349
            },
            {
                "date": "2025-04-13",
                "like": 12369
            },
            {
                "date": "2025-04-14",
                "like": 11369
            },
            {
                "date": "2025-04-15",
                "like": 20369
            }
        ],
        "chart_url": ""
    }

    result2 = {
        "data_list": [
            {
                "date": "2025-04-06",
                "like": 1460
            },
            {
                "date": "2025-04-07",
                "like": 1500
            },
            {
                "date": "2025-04-08",
                "like": 1620
            },
            {
                "date": "2025-04-09",
                "like": 1730
            },
            {
                "date": "2025-04-10",
                "like": 1880
            },
            {
                "date": "2025-04-11",
                "like": 1980
            },
            {
                "date": "2025-04-12",
                "like": 780
            },
            {
                "date": "2025-04-13",
                "like": 1380
            },
            {
                "date": "2025-04-14",
                "like": 2180
            },
            {
                "date": "2025-04-15",
                "like": 3080
            }
        ],
        "chart_url": ""
    }

    if item_id == "@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==":
        result_dict = result1
    else:
        result_dict = result2

    # https://quickchart.io/chart?c={type:'bar',data:{labels:[%27A%27,%27B%27,%27C%27],datasets:[{data:[30,60,10]}]}}
    chart_type = "bar"
    chart_labels = []
    chart_datasets_data = []
    chart_datasets_labels = "点赞数据"
    for item in result_dict["data_list"]:
        chart_labels.append(item["date"])
        chart_datasets_data.append(item["like"])
    chart_url = "https://quickchart.io/chart?c={type:'%s',data:{labels:%s,datasets:[{label:'%s',data:%s}]}}" % (
        chart_type, chart_labels, chart_datasets_labels, chart_datasets_data)
    chart_url = chart_url.replace(" ", "")
    result_dict["chart_url"] = chart_url

    return result_dict


@mcp.tool(name="视频播放数据", description="视频播放数据, 返回日期(date),播放数(play)")
def item_play(open_id: str, item_id: str) -> dict:
    print("open_id:", open_id)
    result1 = {
        "data_list": [
            {
                "date": "2025-04-06",
                "play": 3114260
            },
            {
                "date": "2025-04-07",
                "play": 3215300
            },
            {
                "date": "2025-04-08",
                "play": 3316320
            },
            {
                "date": "2025-04-09",
                "play": 3417330
            },
            {
                "date": "2025-04-10",
                "play": 3518380
            },
            {
                "date": "2025-04-11",
                "play": 2916169
            },
            {
                "date": "2025-04-12",
                "play": 4216469
            },
            {
                "date": "2025-04-13",
                "play": 4816369
            },
            {
                "date": "2025-04-14",
                "play": 5016369
            },
            {
                "date": "2025-04-15",
                "play": 6616269
            }
        ],
        "chart_url": ""
    }

    result2 = {
        "data_list": [
            {
                "date": "2025-04-06",
                "play": 211460
            },
            {
                "date": "2025-04-07",
                "play": 211500
            },
            {
                "date": "2025-04-08",
                "play": 221620
            },
            {
                "date": "2025-04-09",
                "play": 231730
            },
            {
                "date": "2025-04-10",
                "play": 241880
            },
            {
                "date": "2025-04-11",
                "play": 251980
            },
            {
                "date": "2025-04-12",
                "play": 261980
            },
            {
                "date": "2025-04-13",
                "play": 259004
            },
            {
                "date": "2025-04-14",
                "play": 293894
            },
            {
                "date": "2025-04-15",
                "play": 350212
            }
        ],
        "chart_url": ""
    }

    if item_id == "@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==":
        result_dict = result1
    else:
        result_dict = result2

    # https://quickchart.io/chart?c={type:'bar',data:{labels:[%27A%27,%27B%27,%27C%27],datasets:[{data:[30,60,10]}]}}
    chart_type = "line"
    chart_labels = []
    chart_datasets_data = []
    chart_datasets_labels = "播放数据"
    for item in result_dict["data_list"]:
        chart_labels.append(item["date"])
        chart_datasets_data.append(item["play"])
    chart_url = "https://quickchart.io/chart?c={type:'%s',data:{labels:%s,datasets:[{label:'%s',data:%s}]}}" % (
        chart_type, chart_labels, chart_datasets_labels, chart_datasets_data)
    chart_url = chart_url.replace(" ", "")
    result_dict["chart_url"] = chart_url

    return result_dict

# def generate_chart_url(result_list, label, item_type):
#     chart_type = "bar"
#     chart_labels = [item["date"] for item in result_list]
#     chart_datasets_data = [item[item_type] for item in result_list]
#     chart_datasets_labels = label
#     chart_url = f"https://quickchart.io/chart?c={{type: '{chart_type}',data:{{labels: {chart_labels},datasets: [{{label: '{chart_datasets_labels}',data: {chart_datasets_data}}}]}}"
#     return chart_url


@mcp.tool(name="视频评论数据", description="视频评论数据, 返回日期(date),点赞数(like)")
def item_comment(open_id: str, item_id: str) -> dict:
    result1 = {
        "data_list": [
            {
                "date": "2025-04-06",
                "comment": 2465
            },
            {
                "date": "2025-04-07",
                "comment": 3505
            },
            {
                "date": "2025-04-08",
                "comment": 3625
            },
            {
                "date": "2025-04-09",
                "comment": 3735
            },
            {
                "date": "2025-04-10",
                "comment": 3885
            },
            {
                "date": "2025-04-11",
                "comment": 3675
            },
            {
                "date": "2025-04-12",
                "comment": 3275
            },
            {
                "date": "2025-04-13",
                "comment": 3175
            },
            {
                "date": "2025-04-14",
                "comment": 1875
            },
            {
                "date": "2025-04-15",
                "comment": 2075
            }
        ]
    }

    result2 = {
        "data_list": [
            {
                "date": "2025-04-06",
                "comment": 12265
            },
            {
                "date": "2025-04-07",
                "comment": 13305
            },
            {
                "date": "2025-04-08",
                "comment": 14325
            },
            {
                "date": "2025-04-09",
                "comment": 15335
            },
            {
                "date": "2025-04-10",
                "comment": 16385
            },
            {
                "date": "2025-04-11",
                "comment": 15375
            },
            {
                "date": "2025-04-12",
                "comment": 12375
            },
            {
                "date": "2025-04-13",
                "comment": 11375
            },
            {
                "date": "2025-04-14",
                "comment": 8375
            },
            {
                "date": "2025-04-15",
                "comment": 14375
            }
        ]
    }

    result_ = {"data_list": [], "chart_url": ""}
    if item_id == "@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==":
        result_["data_list"] = result1["data_list"]
    else:
        result_["data_list"] = result2["data_list"]

    # https://quickchart.io/chart?c={type:'bar',data:{labels:[%27A%27,%27B%27,%27C%27],datasets:[{data:[30,60,10]}]}}
    chart_type = "line"
    chart_labels = []
    chart_datasets_data = []
    chart_datasets_labels = "评论数据"
    for item in result_["data_list"]:
        chart_labels.append(item["date"])
        chart_datasets_data.append(item["comment"])
    chart_url = "https://quickchart.io/chart?c={type:'%s',data:{labels:%s,datasets:[{label:'%s',data:%s}]}}" % (
        chart_type, chart_labels, chart_datasets_labels, chart_datasets_data)
    chart_url = chart_url.replace(" ", "")
    result_["chart_url"] = chart_url

    return result_


@mcp.tool(name="视频基础数据", description="获取视频基础数据, 返回总点赞数,总评论,总分享,平均播放时长,总播放次数")
def item_base(open_id: str, item_id: str) -> dict:
    data = {
        "result": {
            "total_like": 230400,
            "total_comment": 25300,
            "total_share": 2050,
            "avg_play_duration": 30,
            "total_play": 24054300
        },
        "description": ""
    }
    return data


@mcp.tool(name="视频发布数据", description="用户视频发布数据, 每日发布内容数、每天新增视频播放、总内容数")
def user_item(open_id: str) -> dict:
    data = {
        "result_list": [
            {
                "date": "2025-04-09",
                "new_issue": "5",
                "new_play": "502323",
                "total_issue": "480"
            },
            {
                "date": "2025-04-10",
                "new_issue": "8",
                "new_play": "502323",
                "total_issue": "490"
            },
            {
                "date": "2025-04-11",
                "new_issue": "11",
                "new_play": "502323",
                "total_issue": "502"
            },
            {
                "date": "2025-04-12",
                "new_issue": "15",
                "new_play": "502323",
                "total_issue": "520"
            },
            {
                "date": "2025-04-13",
                "new_issue": "20",
                "new_play": "502323",
                "total_issue": "530"
            },
            {
                "date": "2025-04-14",
                "new_issue": "3",
                "new_play": "502323",
                "total_issue": "533"
            },
            {
                "date": "2025-04-15",
                "new_issue": "28",
                "new_play": "502323",
                "total_issue": "561"
            },
            {
                "date": "2025-04-16",
                "new_issue": "19",
                "new_play": "234343",
                "total_issue": "580"
            }
        ]
    }
    return data


@mcp.tool(name="粉丝情况数据", description="粉丝量变化趋势, 每日新粉丝数、每天总粉丝数")
def fans_change(open_id: str) -> dict:
    data = {
        "result_list": [
            {
                "date": "2025-04-10",
                "new_fans": "90",
                "total_fans": "17302"
            },
            {
                "date": "2025-04-11",
                "new_fans": "290",
                "total_fans": "17450"
            },
            {
                "date": "2025-04-12",
                "new_fans": "270",
                "total_fans": "17890"
            },
            {
                "date": "2025-04-13",
                "new_fans": "360",
                "total_fans": "18110"
            },
            {
                "date": "2025-04-14",
                "new_fans": "270",
                "total_fans": "18410"
            },
            {
                "date": "2025-04-15",
                "new_fans": "380",
                "total_fans": "18810"
            },
            {
                "date": "2025-04-16",
                "new_fans": "890",
                "total_fans": "19410"
            }
        ]
    }

    chart_type = "line"
    chart_labels = []
    chart_datasets_data_total_fans = []
    chart_datasets_labels_total_fans = "当日总粉丝数"
    chart_datasets_data_news_fans = []
    chart_datasets_labels_news_fans = "当日新增粉丝数"
    for item in data["result_list"]:
        chart_labels.append(item["date"])
        chart_datasets_data_total_fans.append(item["total_fans"])
        chart_datasets_data_news_fans.append(item["new_fans"])
    chart_url = "https://quickchart.io/chart?c={type:'%s',data:{labels:%s,datasets:[{label:'%s',data:%s},{label:'%s',data:%s}]}}" % (
        chart_type, chart_labels, chart_datasets_labels_total_fans, chart_datasets_data_total_fans, chart_datasets_labels_news_fans, chart_datasets_data_news_fans)
    chart_url = chart_url.replace(" ", "")
    data["chart_url"] = chart_url

    return data


@mcp.tool(name="粉丝画像数据",
          description="粉丝画像数据, 所有粉丝量、粉丝活跃天数分布、粉丝年龄分布、粉丝设备分布、粉丝流量贡献、粉丝地域分布、粉丝性别分布、粉丝兴趣分布")
def fans_profile(open_id: str) -> dict:
    data = {
        "active_days_distributions": [
            {
                "item": "0~4",
                "value": 24600
            },
            {
                "item": "5~8",
                "value": 900
            },
        ],
        "age_distributions": [
            {
                "item": "1-23",
                "value": 18000
            },
            {
                "item": "24-30",
                "value": 2400
            },
            {
                "item": "31-40",
                "value": 900
            },
            {
                "item": "41-50",
                "value": 1200
            },
            {
                "item": "50-",
                "value": 10
            }
        ],
        "all_fans_num": 20280,
        "device_distributions": [
            {
                "item": "华为",
                "value": 8300
            },
            {
                "item": "小米",
                "value": 4000
            },
            {
                "item": "Iphone",
                "value": 9000
            }
        ],
        "flow_contributions": [
            {
                "all_sum": 800,
                "fans_sum": 0,
                "flow": "vv"
            }
        ],
        "gender_distributions": [
            {
                "item": "1",
                "value": 12500
            },
            {
                "item": "2",
                "value": 12800
            }
        ],
        "geographical_distributions": [
            {
                "item": "北京",
                "value": 100
            },
            {
                "item": "上海",
                "value": 150
            }
        ],
        "interest_distributions": [
            {
                "item": "美食",
                "value": 380
            },
            {
                "item": "旅行",
                "value": 400
            },
            {
                "item": "生活",
                "value": 200
            }
        ]
    }
    return data

@mcp.tool(name="粉丝来源数据", description="粉丝来源数据,直播、新用户引导页、视频详情页、面对面、发现页、其它等 ")
def fans_source(open_id: str) -> dict:
    result = {
        "fans_source": [
            {
                "source": "直播",
                "percent": 31.32
            },
            {
                "source": "视频详情页",
                "percent": 40
            },
            {
                "source": "发现页",
                "percent": 18.68
            },
            {
                "source": "新用户引导页",
                "percent": 10
            },
        ]
    }

    chart_type = "pie"
    chart_labels = []
    chart_datasets_data = []
    chart_datasets_labels = "粉丝来源数据"
    for item in result["fans_source"]:
        chart_labels.append(item["source"])
        chart_datasets_data.append(item["percent"])
    chart_url = "https://quickchart.io/chart?v=2.9.4&c={type:'%s',data:{labels:%s,datasets:[{label:'%s',data:%s}]}}" % (
        chart_type, chart_labels, chart_datasets_labels, chart_datasets_data)
    chart_url = chart_url.replace(" ", "")
    result["chart_url"] = chart_url

    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")
    # result_dict = item_like(open_id="test", item_id="@8hxdhauTCMppanGnM4ltGM780mDqPP+KPpR0qQOmLVAXb/T060zdRmYqig357zEBq6CZRp4NVe6qLIJW/V/x1w==")
    # result_dict = fans_change(open_id="test")
    # print(result_dict)
