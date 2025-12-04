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
                await page.locator('body').first.is_visible()
                # 模拟人类行为：一步步操作
                # 假设我们要点击 "今日" 这个按钮
                # 1. 定位元素
                target_div = page.get_by_text("今日", exact=True).first
                await target_div.is_visible()
                await asyncio.sleep(1)
                # 2. 使用封装的拟人化点击方法
                await self.human_like_click(page, target_div)
                await asyncio.sleep(1)
                next_tournament =await page.get_by_text("英超", exact=True)

                # 如果有下一步，继续操作，例如点击某个分类
                await self.human_like_click(page, next_tournament)
                await asyncio.sleep(1)
                
                
                # 如果需要输入搜索框
                # search_input = page.locator("input[name='q']")
                # await search_input.click()
                # await page.keyboard.type("Python 爬虫", delay=100) # 模拟打字延迟

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

    async def human_like_click(self, page: Page, selector: str):
        """
        模拟人类点击行为：
        1. 随机等待
        2. 移动鼠标到元素位置
        3. 点击
        """
        try:
            # 1. 随机等待一段时间 (0.5 - 1.5秒)
            await asyncio.sleep(random.uniform(1, 3))
            
            # 2. 获取元素
            element = page.locator(selector).first
            
            # 确保元素可见
            if await element.is_visible():
                # 3. 移动鼠标到元素上方 (可选，增加真实感)
                # 获取元素位置
                box = await element.bounding_box()
                if box:
                    await page.mouse.move(
                        box["x"] + box["width"] / 2, 
                        box["y"] + box["height"] / 2,
                        steps=10 # 模拟鼠标移动轨迹
                    )
                
                # 4. 点击
                await element.click()
                print(f"Clicked element: {selector}")
            else:
                print(f"Element not visible: {selector}")
                
        except Exception as e:
            print(f"Error clicking {selector}: {e}")

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
