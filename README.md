## AUTO ĐĂNG KÝ MÔN HỌC QLDT PTIT

@Author: [quanganh208](https://github.com/quanganh208)

@Version: 1.0.1

### Description

- Hỗ trợ đăng ký môn học trên qldt. Chấp web trắng tinh vẫn đăng ký được môn.
- Hỗ trợ canh slot môn học được nhả. Tool giúp bạn canh slot 24/24, tự động đăng ký môn mà không cần phải ngồi canh nữa.

### Installation

- Chỉ đơn giản là clone git này về. Rảnh thì download tay cũng được =))))

### Config

- File **account.json**: Thay đổi thông tin tài khoản qldt PTIT.

  - _username_: Mã sinh viên của bạn
  - _password_: Mật khẩu qldt của bạn

- File **config.json**: Thay đổi config cho tool.

  - _autoRegisterCourse_: Bật/tắt tính năng tự động đăng ký môn học.
  - _autoRegisterCourseOutOfSlot_: Bật/tắt tính năng tự động canh môn học hết slot.
  - _showCourseRegistrationSuccess_: Bật/tắt tính năng xem danh sách môn học đã đăng ký thành công.
  - _timeDelayRandom_: Thời gian delay ngẫu nhiên khi canh slot môn học hết slot. Đơn vị _timeDelayRandom_: giây. Tool sẽ random delay từ 1 đến _timeDelayRandom_.
  - _Với tính năng bật/tắt, bật = true, tắt = false._

- File **danh_sach_mon_hoc.txt**: Danh sách môn học cần đăng ký
  - File này rất quan trọng, liên quan đến sự sống còn của bạn trong kì tới.
  - **Định dạng**: Mã MH|Nhóm|Tổ|Lớp. _Ví dụ: ABC1234|01|01|D22-001_
  - Nếu môn học không có mã tổ hãy bỏ trống. _Ví dụ: ABC1234|01||D22-001_
  - Mỗi môn học tồn tại trên 1 dòng, mỗi dòng định dạng như trên. _Lưu ý: Hãy chắc chắn rằng 4 dữ liệu trên của môn học khớp với dữ liệu môn học ở trên web._
- _Lưu ý: Thiếu bất cứ file nào sẽ dẫn đến lỗi, đừng xóa lung tung nhé =)))_

### Using Tool

- Mở file **AutoDKMK-PTIT.exe** tool sẽ tự động đăng nhập qldt PTIT. Tiếp theo như nào thử đi là biết.
- Thao tác rất đơn giản, chỉ cần nhấn mỗi phím ENTER thôi =))

### Donation

- Donate tiền cho Quanh mua mì tôm tại:

<img src="https://scontent.fhan14-4.fna.fbcdn.net/v/t1.15752-9/387519503_1014386016510688_7126056876433079552_n.png?_nc_cat=106&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=t40ZM-L4CoYAX_jpAVZ&_nc_ht=scontent.fhan14-4.fna&oh=03_AdRxlH2is5ZNivMetJiYjmLfTSkOsLDVeoq4nlDAM64ULw&oe=658BEBEA" alt="208046789 MB Bank NGUYEN MAC QUANG ANH" title= "QR Donate for Quanh" width="170" height="220">
