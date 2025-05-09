Đây là 1 dự án lớn, đồ án về camera AI

Sử dụng model YOLO v8 và v10 để chạy chuẩn đoán hình ảnh

Để sử dụng thì đầu tiên:

```sh
pip install -r requirements.txt 
```

Check CUDA version của máy:

```sh
nvidia-smi
```

Nếu máy bạn có CUDA, cài đặt pytorch cuda theo cách sau:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Sau khi cài đặt xong CUDA, chúng ta kiểm tra xem máy đã có torch hỗ trợ CUDA chưa:

```python
import torch

print("CUDA available:", torch.cuda.is_available())
print("CUDA version in PyTorch:", torch.version.cuda)
print("Device count:", torch.cuda.device_count())
print("Current device:", torch.cuda.current_device() if torch.cuda.is_available() else "None")
```

Chạy thử pretrained-model:

```sh
python model/run_yolov5.py
python model/run_yolov10.py
```

Khi pretrained-model chạy mượt mà, chúng ta thử cắm kết nối PLC và chạy thử

```sh 
python PLC/plc_connection.py
```

Để chạy cả giao diện và model:

```sh
python main.py
```

try this link for custom dataset training YOLO algorithm: 

https://colab.research.google.com/drive/1Jkf9k6akhm1cnwcOIup9G_h2bW6HROPq?usp=sharing