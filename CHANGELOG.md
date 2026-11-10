# Changelog

Mọi thay đổi đáng chú ý của dự án được ghi ở đây.
Định dạng theo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
phiên bản theo [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Lệnh `occ` với tùy chọn `--version`.
- Công cụ kiểm tra chất lượng: ruff, mypy (strict), pytest, pre-commit, Makefile.
- Lint cấm `cv2.imwrite` và `cv2.VideoWriter` ngoài `occ/tools/` (quyền riêng tư).
- Giấy phép AGPL-3.0, README, tài liệu phần cứng.

### Changed
- Đổi trọng tâm dự án từ đếm lượt qua vạch sang đếm số người theo vùng (đặc tả mới thay cho brief v2.0).
- Đổi tên package `mcva` thành `occ`; quản lý thư viện bằng uv, ghim phiên bản trong `uv.lock`.

### Removed
- File trọng số model và các file sinh tự động khỏi git.
