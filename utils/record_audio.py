import pyaudio
import wave
import keyboard

# 定义一个函数用于从麦克风录制音频并保存到文件
def record_audio(file_path):
    """
    这个函数用于从麦克风录制音频，并将其保存到指定的文件路径

    参数：
    file_path (str)：音频文件的保存路径

    """
    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()  
    # 打开音频流，设置格式、声道数、采样率等参数
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)  
    # 创建一个空列表用于存储录制的音频数据
    frames = []  
    # 打印提示信息，表示开始录制
    print("Press 's' to start recording...")
    # 等待用户按下 's' 键开始录制
    keyboard.wait('s')
    # 打印提示信息，表示开始录制
    print("Recording...")
    # 开始录制
    while True:
        # 从音频流中读取 1024 个数据样本
        data = stream.read(1024)  
        # 将数据添加到 frames 列表中
        frames.append(data)
        # 检查是否按下 'q' 键结束录制
        if keyboard.is_pressed('q'):
            break
    # 打印提示信息，表示录制已停止
    print("Recording stopped.")  
    # 停止音频流
    stream.stop_stream()
    # 关闭音频流
    stream.close()  
    # 终止 PyAudio 对象
    p.terminate()  
    # 打开文件，以写入模式打开
    wf = wave.open(file_path, 'wb')  
    # 设置音频的声道数、采样宽度和采样率
    wf.setnchannels(1)  
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))  
    wf.setframerate(16000)  
    # 将 frames 列表中的所有数据连接成一个字节串，并写入文件
    wf.writeframes(b''.join(frames))  
    # 关闭文件
    wf.close()  
    print("Done")

if __name__ == "__main__":
    record_audio("pyaudio2.wav")
————————————————
