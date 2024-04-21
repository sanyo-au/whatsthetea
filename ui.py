import gradio as gr
import sendemail

def sentence_builder(Name, Email, Topics):
    sendemail.send_email(Name, Email, Topics)
    return f"""Hello {Name}, You have now subscribed to  {" and ".join(Topics)} using {Email} . """



demo = gr.Interface(
    sentence_builder,
    [
        "text", "text",
        gr.CheckboxGroup(["Tech", "AI", "Politics"], label="topics")
    ],
    "text",title="What's the Tea!"
)
if __name__ == "__main__":
    demo.launch()
