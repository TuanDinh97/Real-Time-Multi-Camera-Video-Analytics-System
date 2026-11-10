# Indoor Occupancy & Space Utilization

Hệ thống đếm số người theo từng vùng (chỗ ngồi, dãy bàn, cả phòng) từ camera, để đo mức sử dụng
không gian ở thư viện, phòng lab, văn phòng. Chạy tại chỗ trên một PC có GPU. Hệ thống chỉ lưu
số đếm, không lưu hình ảnh và không nhận dạng người.

> **Trạng thái:** đang phát triển, Giai đoạn 0 (dựng nền móng). Chưa có tính năng đếm người.

## Tài liệu

- [Đặc tả và lộ trình](docs/indoor_occupancy_spec.pdf)
- [Phần cứng và môi trường](docs/hardware.md)

## Yêu cầu

- Ubuntu 24.04, Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Để chạy bằng Docker: GPU NVIDIA có driver, Docker Engine, NVIDIA Container Toolkit

## Cài đặt môi trường dev

```bash
git clone https://github.com/TuanDinh97/Real-Time-Multi-Camera-Video-Analytics-System.git
cd Real-Time-Multi-Camera-Video-Analytics-System
make setup
```

## Lệnh thường dùng

| Lệnh | Việc |
|---|---|
| `make lint` | Kiểm tra style (ruff) và kiểu dữ liệu (mypy) |
| `make test` | Chạy test (pytest) |
| `uv run occ --version` | In phiên bản |

## Cấu trúc thư mục

```
src/occ/    mã nguồn: common, reader, engine, analytics, storage, api, tools
tests/      test tự động
scripts/    script thử nghiệm (baseline YOLO trên camera OAK)
docs/       đặc tả, tài liệu
```

## Quyền riêng tư

Khung hình chỉ tồn tại trong RAM. Hệ thống không ghi ảnh hay video ra đĩa và không nhận dạng người.
Chi tiết ở chương "Quyền riêng tư" trong đặc tả.

## Giấy phép

AGPL-3.0, xem [LICENSE](LICENSE). Dự án dùng Ultralytics YOLO, cũng phát hành theo AGPL-3.0.
