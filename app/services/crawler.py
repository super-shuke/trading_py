import asyncio
import random
from fake_useragent import UserAgent
from playwright.async_api import async_playwright, Page


class AdvancedCrawler:
    def __init__(self):
        # 初始化用户代理 faker user
        self.ua = UserAgent()

    async def fetch_dynamic_content(self, url: str):

        async with async_playwright() as p:
            # 1. 启动浏览器，但要隐藏自动化特征
            # headless=True (无头模式) 很容易被识别，
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",  # 【关键】移除自动化特征
                    "--no-sandbox",
                    "--disable-infobars",
                ],
            )
            # 随机 用户代理 和窗口大小
            context = await browser.new_context(
                user_agent=self.ua.random,  # 使用随机用户代理
                viewport={"width": 1280, "height": 800},
                locale="zh-CN",
                timezone_id="America/New_York",
            )
            # 给context 注入js的脚本 彻底抹除 webdriver 痕迹
            await context.add_init_script(
                """
                    Object.defineProperty(navigator, 'webdriver', {
                            get:()=>undefined
                        });
                """
            )
            page = await context.new_page()

            try:
                print(f"Navigating to（爬取中） {url}")
                # 访问页面
                await page.goto(url, wait_until="networkidle", timeout=60000)

                target_div = page.get_by_text("今日", exact=True)

                await target_div.evaluate("element=> element.click()")

                # 模拟人类滚动页面以加载动态内容
                await self.simulate_human_scroll(page)
                # 获取页面内容 渲染后的html
                content = await page.content()
                # 注入js 脚本解析content
                titles = await page.evaluate(
                    """
                        ()=>{
                            const elements=document.querySelectorAll('.sticky_div'); // 替换为实际的选择器
                            return Array.from(elements).map(el=>el.innerText).filter(text=>text.length!==0);
                        }
                    """
                )
                return titles[:10]
            except Exception as e:
                print(f"Error fetching dynamic content from {url}: {e}")
                return []
            finally:
                # await browser.close()
                print("浏览器已关闭")

    async def simulate_human_scroll(self, page: Page):
        # 获取页面高度
        scroll_height = await page.evaluate("() => document.body.scrollHeight")
        print(f"Initial scroll height: {scroll_height}")
        viewport_height = page.viewport_size["height"]
        scroll_position = 0
        print(f"Initial viewport height: {viewport_height}")

        while scroll_position < scroll_height:
            # 随机滚动距离
            scroll_step = min(viewport_height, scroll_height - scroll_position)
            scroll_position += scroll_step
            await page.evaluate(f"window.scrollTo(0, {scroll_position})")
            # 随机等待时间 模拟人类行为
            await asyncio.sleep(0.5 + 0.5 * random.random())
            print(f"Scrolled to position: {scroll_position}")
            # 更新页面高度
            scroll_height = await page.evaluate("() => document.body.scrollHeight")
