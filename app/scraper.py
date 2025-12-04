import requests
from bs4 import BeautifulSoup
import logging
import time
import random
from fake_useragent import UserAgent
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaiduNewsScraper:
    def __init__(self):
        self.base_url = "https://www.baidu.com/s"
        self.ua = UserAgent()  # 使用fake_useragent生成随机User-Agent
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.baidu.com",
            "Referer": "https://www.baidu.com/",
            "Sec-Ch-Ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }
        # 初始化抓取间隔参数
        self.base_delay = 2  # 基础延迟（秒）
        self.max_delay = 10  # 最大延迟（秒）
        self.current_delay = self.base_delay  # 当前延迟
        self.failure_count = 0  # 失败次数计数器
    
    def fetch_news(self, keyword, rtt=1, bsst=1, cl=2, tn="news", rsv_dl="ns_pc", rn=10):
        """
        从百度新闻搜索接口获取数据
        
        参数:
        keyword: 搜索关键字
        rtt: 1 - 按时间排序, 2 - 按焦点排序
        bsst: 1 - 仅包含有图新闻
        cl: 2 - 搜索类型为新闻
        tn: news - 搜索类型为新闻
        rsv_dl: ns_pc - 下载方式
        rn: 每页显示的结果数量
        
        返回:
        list: 包含新闻信息的列表，每个元素是一个字典
        """
        try:
            # 构造请求URL
            url = f"https://www.baidu.com/s?rtt={rtt}&bsst={bsst}&cl={cl}&tn={tn}&rsv_dl={rsv_dl}&word={keyword}&rn={rn}"
            
            logger.info(f"正在抓取百度新闻数据，关键字: {keyword}")
            logger.info(f"请求URL: {url}")
            
            # 随机更换User-Agent
            self.headers["User-Agent"] = self.ua.random
            logger.info(f"使用User-Agent: {self.headers['User-Agent']}")
            
            # 随机延迟，增加抓取间隔
            delay_time = random.uniform(self.base_delay, self.current_delay)
            logger.info(f"抓取前延迟 {delay_time:.2f} 秒")
            time.sleep(delay_time)
            
            # 发送请求
            response = requests.get(url, headers=self.headers, timeout=15)
            response.encoding = "utf-8"
            
            logger.info(f"请求成功，状态码: {response.status_code}")
            
            # 检查是否被反爬
            if response.status_code in [403, 429, 503]:
                logger.warning(f"请求被反爬限制，状态码: {response.status_code}")
                self.failure_count += 1
                # 增加延迟
                self.current_delay = min(self.current_delay * 2, self.max_delay)
                logger.info(f"增加延迟至 {self.current_delay} 秒")
                return []
            elif response.status_code != 200:
                logger.error(f"请求失败，状态码: {response.status_code}")
                self.failure_count += 1
                # 增加延迟
                self.current_delay = min(self.current_delay * 1.5, self.max_delay)
                logger.info(f"增加延迟至 {self.current_delay} 秒")
                return []
            
            # 请求成功，恢复基础延迟
            self.current_delay = self.base_delay
            self.failure_count = 0
            
            # 保存响应到文件，用于调试
            with open("baidu_news_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            # 解析页面内容
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 提取新闻数据
            news_list = []
            
            # 查找新闻条目 - 百度新闻可能使用不同的class名称
            # 尝试多种可能的选择器
            possible_selectors = [
                ".result",  # 原始选择器
                ".news-item",  # 另一种可能的选择器
                ".c-container",  # 通用内容容器
            ]
            
            news_items = []
            for selector in possible_selectors:
                items = soup.select(selector)
                if items:
                    news_items = items
                    logger.info(f"使用选择器 '{selector}' 找到 {len(news_items)} 条新闻")
                    break
            
            if not news_items:
                logger.warning("没有找到新闻条目")
                # 打印页面结构以便调试
                logger.debug(f"页面主要内容: {soup.body.prettify()[:5000]}")
                return []
            
            for item in news_items:
                try:
                    # 提取标题
                    title_elements = item.select(".t a, .news-title a, h3 a")
                    title = title_elements[0] if title_elements else None
                    news_title = title.text.strip() if title else ""
                    
                    # 提取原始URL
                    news_url = title["href"] if title and "href" in title.attrs else ""
                    
                    # 提取来源和时间
                    source_time_elements = item.select(".c-author, .news-source")
                    source_time = source_time_elements[0] if source_time_elements else None
                    
                    if source_time:
                        source_info = source_time.text.strip().split(" ")
                        if len(source_info) >= 2:
                            source = source_info[0]
                            publish_time = " ".join(source_info[1:])
                        else:
                            source = source_info[0] if source_info else ""
                            publish_time = ""
                    else:
                        source = ""
                        publish_time = ""
                    
                    # 提取概要
                    summary_elements = item.select(".c-summary, .news-summary")
                    summary = summary_elements[0] if summary_elements else None
                    news_summary = summary.text.strip() if summary else ""
                    
                    # 提取封面
                    cover_elements = item.select(".c-img img, .news-img img")
                    cover = cover_elements[0] if cover_elements else None
                    news_cover = cover["src"] if cover and "src" in cover.attrs else ""
                    
                    # 只有当标题和URL都存在时，才添加到新闻列表
                    if news_title and news_url:
                        news_list.append({
                            "标题": news_title,
                            "概要": news_summary,
                            "封面": news_cover,
                            "原始URL": news_url,
                            "来源": source
                            # 移除publish_time字段，因为前端模板中没有使用
                        })
                    
                except Exception as e:
                    logger.error(f"解析新闻条目时出错: {e}")
                    continue
            
            logger.info(f"成功解析 {len(news_list)} 条新闻")
            return news_list
            
        except Exception as e:
            logger.error(f"抓取百度新闻数据时出错: {e}")
            import traceback
            traceback.print_exc()
            return []

if __name__ == "__main__":
    # 测试数据抓取模块
    scraper = BaiduNewsScraper()
    keyword = "成都理工大学"
    news_list = scraper.fetch_news(keyword)
    
    print(f"抓取到 {len(news_list)} 条关于 '{keyword}' 的新闻")
    for i, news in enumerate(news_list):
        print(f"\n新闻 {i+1}:")
        print(f"标题: {news['标题']}")
        print(f"概要: {news['概要']}")
        print(f"封面: {news['封面']}")
        print(f"原始URL: {news['原始URL']}")
        print(f"来源: {news['来源']}")
