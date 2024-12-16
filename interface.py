import gradio as gr
from async_pinterest import Pinterest
import chromedriver_autoinstaller
import asyncio

class GUI:
    def __init__(self):
        # Check chromedriver exists
        chromedriver_autoinstaller.install()
        self.__demo = self.__gui_main()

    def __crawling(self,pid:str,ppw:str,URL:str,page_c:int,img_c:int|None,save:str):
        p = Pinterest(pid, ppw)
        gr.Warning("크롤링 시작...")
        asyncio.run(
        p.single_download(
            n=int(page_c),
            max_image_count=img_c,
            url=URL,
            dir=save
            ))
        gr.Info("크롤링 종료")

    def __gui_main(self)->gr.Blocks:
        with gr.Blocks() as demo:
            with gr.Column(): # Setting
                pid = gr.Textbox(label="핀터레스트 ID",type="email")
                ppw = gr.Textbox(label="핀터레스트 PW",type="password")
                gr.Markdown("[Pinterest 링크](https://kr.pinterest.com/)")
                URL = gr.Textbox(label="크롤링할 페이지",type='text')
                page_c = gr.Number(label="Page 숫자",value=-1,minimum=-1,maximum=999999)
                img_c = gr.Number(label="이미지 숫자",value=1,minimum=1,maximum=9999999)
                save = gr.Textbox(label="저장 위치",type="text",value="./downloads")
                btn = gr.Button("Start!",variant="huggingface")
            # with gr.Column(): # pass
            #     pass
        
            btn.click(fn=self.__crawling,inputs=[pid,ppw,URL,page_c,img_c,save],outputs=None)

        return demo

    def __call__(self,share:bool=False):
        self.__demo.launch(share=share)

if __name__ =="__main__":
    GUI()()