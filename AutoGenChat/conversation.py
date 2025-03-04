# conversation.py
from AutoGenChat.autogen_client import chat_with_autogen


def start_conversation():
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以调用 API 获取信息"}
    ]

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                print("Exiting the conversation.")
                break

            messages.append({"role": "user", "content": user_input})
            response = chat_with_autogen(messages)
            print("AutoGen:", response)

            # 记录 AutoGen 响应
            messages.append({"role": "assistant", "content": response})

        except KeyboardInterrupt:
            print("\nExiting the conversation due to user interrupt.")
            break

if __name__ == "__main__":
    start_conversation()
