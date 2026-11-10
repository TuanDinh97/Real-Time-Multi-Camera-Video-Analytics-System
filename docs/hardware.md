# Phần cứng và môi trường

Ghi lại máy đang dùng để phát triển, cùng các ràng buộc khi deploy sang máy khác.
Mọi báo cáo benchmark phải ghi kèm thông số này (spec, mục "Cấu hình chuẩn để so sánh").

Cập nhật lần cuối: 10/11/2026.

## Máy dev/staging hiện tại (laptop)

| Hạng mục | Giá trị |
|---|---|
| GPU | NVIDIA GeForce RTX 5050 Laptop GPU, kiến trúc Blackwell |
| VRAM | 8151 MiB (8 GB) |
| Giới hạn công suất GPU | 45 W (theo bảng `nvidia-smi`; truy vấn `power.limit` trả về `[N/A]`) |
| Driver NVIDIA (KMD) | 610.43.02 |
| CUDA tối đa driver hỗ trợ (UMD) | 13.3 |
| CPU | Intel Core 5 210H, 12 luồng (`nproc`) |
| RAM | 15 GiB (theo `free -h`), swap 14 GiB |
| Hệ điều hành | Ubuntu 24.04.4 LTS, kernel 7.0.0-31-generic |
| Docker Engine | 29.7.2 |
| Docker Compose | v5.5.0 |
| NVIDIA Container Toolkit | 1.20.0 |

## Kiểm tra GPU trong Docker

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Docker thấy GPU | `docker run --rm --gpus all ubuntu nvidia-smi` | Đạt (10/11/2026): container thấy RTX 5050, driver 610.43.02, CUDA 13.3 |
| Compose thấy GPU | `docker compose -f ~/gpu-check.yaml up` | Đạt (10/11/2026): torch 2.15.0+cu132, CUDA 13.2|
| PyTorch trên host dùng được GPU | `python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.version.cuda, torch.cuda.get_device_name(0))"` | Chưa chạy |

## Ràng buộc phiên bản CUDA

Phiên bản CUDA trong image Docker phải thỏa cả hai điều kiện:

- **Tối thiểu 12.8**: GPU kiến trúc Blackwell (dòng RTX 50) chỉ được hỗ trợ từ CUDA 12.8.
- **Tối đa 13.3**: không vượt quá phiên bản CUDA mà driver của máy hỗ trợ.

Tag `12.4.1` trong Dockerfile mẫu (Phụ lục C của spec) không dùng được trên máy này.
Phiên bản cụ thể sẽ chốt khi viết `docker/Dockerfile.engine`, theo bảng tương thích của ONNX Runtime.

## Yêu cầu với máy deploy (production)

- Driver NVIDIA đủ mới cho phiên bản CUDA của image (điền phiên bản driver tối thiểu khi chốt image).
- GPU thuộc kiến trúc mà phiên bản CUDA của image hỗ trợ.
- Docker Engine có Compose plugin và NVIDIA Container Toolkit. Hai lệnh kiểm tra ở mục trên phải đạt.
- Đo lại benchmark trên máy đích. Số camera tối đa (M4) đo trên laptop này chỉ là mức sàn.
- Nếu dùng TensorRT: build lại engine trên máy đích, vì engine gắn với từng GPU và phiên bản TensorRT.
  File `.onnx` thì dùng chung được giữa các máy.

## Lưu ý khi đọc số đo trên máy này

- GPU laptop có giới hạn công suất 45 W và có thể giảm xung khi nóng.
  Khi benchmark hoặc soak test, ghi thêm nhiệt độ và xung GPU (`nvidia-smi -q -d TEMPERATURE,CLOCK`).
- GPU này cũng đang xuất hình cho màn hình (`Disp.A: On`, Xorg dùng khoảng 90 MiB VRAM).
- Lúc ghi thông số, máy đã dùng 10 GiB RAM, chỉ còn 5,2 GiB khả dụng.
  Nên đóng bớt ứng dụng trước khi benchmark hoặc soak test.

## Cách thu thập lại thông số (dùng cho máy mới)

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version,power.limit --format=csv
lscpu | grep "Model name"; nproc; free -h; lsb_release -ds; uname -r
docker --version; docker compose version; nvidia-ctk --version
docker run --rm --gpus all ubuntu nvidia-smi
```
