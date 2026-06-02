export const prerender = false; // Bắt buộc chạy Dynamic SSR trên Cloudflare

import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const data = await request.json();
    const { name, phone, age_group, course, message } = data;

    if (!name || !phone) {
      return new Response(
        JSON.stringify({ success: false, message: 'Vui lòng cung cấp Họ tên và Số điện thoại.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Lấy Email Binding từ Cloudflare Locals (SEND_EMAIL)
    const emailBinding = (locals as any).runtime?.env?.SEND_EMAIL;
    if (!emailBinding) {
      return new Response(
        JSON.stringify({ success: false, message: 'Chưa cấu hình Cloudflare Email Binding (SEND_EMAIL) hoặc đang chạy ở môi trường không được hỗ trợ.' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const emailSubject = `[Đăng Ký Mới] ${name} - ${phone}`;
    const emailHtml = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border-radius: 8px;">
        <h2 style="color: #0088cc; border-bottom: 2px solid #0088cc; padding-bottom: 10px; margin-top: 0;">Thông Tin Đăng Ký Học Bơi Mới</h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
          <tr>
            <td style="padding: 8px 0; font-weight: bold; width: 150px; border-bottom: 1px solid #f9f9f9;">Họ và tên:</td>
            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">${name}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; font-weight: bold; border-bottom: 1px solid #f9f9f9;">Số điện thoại:</td>
            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;"><a href="tel:${phone}" style="color: #0088cc; text-decoration: none; font-weight: bold;">${phone}</a></td>
          </tr>
          <tr>
            <td style="padding: 8px 0; font-weight: bold; border-bottom: 1px solid #f9f9f9;">Độ tuổi học viên:</td>
            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">${age_group || 'Chưa cung cấp'}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; font-weight: bold; border-bottom: 1px solid #f9f9f9;">Khóa học chọn:</td>
            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9; font-weight: bold; color: #ff7700;">${course || 'Cần tư vấn thêm'}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; font-weight: bold; vertical-align: top;">Ghi chú yêu cầu:</td>
            <td style="padding: 8px 0; white-space: pre-wrap;">${message || 'Không có ghi chú thêm.'}</td>
          </tr>
        </table>
        <div style="margin-top: 25px; font-size: 0.8rem; color: #888; border-top: 1px solid #eee; padding-top: 15px; text-align: center;">
          Thư điện tử được gửi tự động từ hệ thống landing page <a href="https://newton.dayboi.vip" style="color: #888; text-decoration: underline;">newton.dayboi.vip</a>
        </div>
      </div>
    `;

    const emailText = `HỌ VÀ TÊN: ${name}\nSỐ ĐIỆN THOẠI: ${phone}\nĐỘ TUỔI: ${age_group}\nKHÓA HỌC: ${course}\nGHI CHÚ: ${message}`;

    // Gửi email về hòm thư thứ nhất (dayboivip@gmail.com)
    await emailBinding.send({
      from: { email: 'form@dayboi.vip', name: 'CanSwim Bể bơi Newton' },
      to: [{ email: 'dayboivip@gmail.com' }],
      subject: emailSubject,
      html: emailHtml,
      text: emailText
    });

    // Gửi email về hòm thư thứ hai (buican336@gmail.com)
    try {
      await emailBinding.send({
        from: { email: 'form@dayboi.vip', name: 'CanSwim Bể bơi Newton' },
        to: [{ email: 'buican336@gmail.com' }],
        subject: emailSubject,
        html: emailHtml,
        text: emailText
      });
    } catch (err) {
      console.error('Lỗi khi gửi email đến buican336@gmail.com (Có thể do chưa verify địa chỉ nhận này trong Cloudflare):', err);
    }

    return new Response(
      JSON.stringify({ success: true, message: 'Gửi thông tin đăng ký thành công!' }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error: any) {
    console.error('API Error:', error);
    return new Response(
      JSON.stringify({ success: false, message: error.message || 'Lỗi xử lý hệ thống.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
