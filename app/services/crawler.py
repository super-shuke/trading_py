import asyncio
import random
from xml.sax.xmlreader import Locator
from fake_useragent import UserAgent
from playwright.async_api import async_playwright, Page


class AdvancedCrawler:
    def __init__(self):
        # 初始化用户代理 faker user
        self.ua = UserAgent()

    async def wait_for_dynamic_loading(self, page):
        try:
            # 尝试等待网络静默
            await page.wait_for_load_state("networkidle", timeout=5000)
        except:
            # 如果超时（说明可能有后台一直发包），则强制等待一小会儿兜底
            print("Network busy, forcing wait...")
            await asyncio.sleep(2)

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
                await page.locator("body").first.is_visible()
                # 模拟人类行为：一步步操作
                # 假设我们要点击 "今日" 这个按钮
                # 1. 定位元素
                target_div = page.locator(".classify").filter(has_text="VIP快讯")
                print("Located target div for VIP快讯", target_div)
                await target_div.is_visible()
                predicate = lambda response: (
                    response.request.resource_type in ["xhr", "fetch"]
                    and "application/json"
                    in response.headers.get("content-type", "").lower()
                    and int(response.headers.get("content-length", 1000))
                    > 100  # 简单的过滤太小的包
                )
                async with page.expect_response(predicate) as resp_info:
                    await self.human_like_click(page, target_div)
                    await self.wait_for_dynamic_loading(page)

                response = await resp_info.value
                print(
                    f"Captured XHR response: {response.url} with status {response.status}"
                )

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

    async def human_like_click(self, page: Page, target: str | Locator):

        try:
            # 1. 随机等待一段时间 (0.5 - 1.5秒)
            if isinstance(target, str):
                # 如果是字符串，就去定位它
                element = page.locator(target).first
                selector_str = target
            else:
                # 如果已经是 Locator 对象，直接用
                element = target.first
                selector_str = str(target)  # 仅用于打印日志

            # 确保元素可见
            if await element.is_visible():
                # 3. 移动鼠标到元素上方 (可选，增加真实感)
                # 获取元素位置
                box = await element.bounding_box()
                if box:
                    await page.mouse.move(
                        box["x"] + box["width"] / 2,
                        box["y"] + box["height"] / 2,
                        steps=10,  # 模拟鼠标移动轨迹
                    )

                # 4. 点击
                await element.click()
                print(f"Clicked element: {selector_str}")
            else:
                print(f"Element not visible: {selector_str}")

        except Exception as e:
            print(f"Error clicking {selector_str}: {e}")

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
