# 1. Ghi lại các quyết định kiến trúc

- Trạng thái: Chấp nhận
- Ngày: 2026-11-10

## Bối cảnh

Dự án có nhiều quyết định thiết kế ảnh hưởng lâu dài: cách đọc camera, cách chạy suy luận,
cách lưu dữ liệu, quyền riêng tư. Nếu các quyết định chỉ nằm trong đầu người viết hoặc trong
lịch sử chat, sau vài tháng sẽ không ai nhớ vì sao lại chọn như vậy, và dễ đổi ngược một
quyết định mà không biết hậu quả.

## Quyết định

Mỗi quyết định kiến trúc quan trọng được ghi thành một ADR (Architecture Decision Record)
trong `docs/adr/`, theo mẫu của Michael Nygard gồm ba phần: Bối cảnh, Quyết định, Hệ quả.

- Tên file: `NNNN-tieu-de-ngan.md`, đánh số tăng dần, không dùng lại số đã có.
- ADR đã chấp nhận thì không sửa nội dung. Khi đổi quyết định, viết ADR mới và đánh dấu
  ADR cũ là "Bị thay thế bởi ADR-NNNN".

## Hệ quả

- Người mới, hoặc chính tác giả sau này, đọc `docs/adr/` để hiểu vì sao hệ thống được
  thiết kế như hiện tại.
- Mỗi quyết định tốn thêm vài phút để viết.
- Quyết định go/no-go ở Giai đoạn 1 sẽ được ghi thành một ADR, theo đặc tả.
