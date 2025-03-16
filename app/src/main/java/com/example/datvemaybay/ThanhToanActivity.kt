package com.example.datvemaybay

import BookingResponse
import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.CardInfo
import com.example.datvemaybay.data.models.DatChoData
import com.example.datvemaybay.data.models.ErrorResponse
import com.example.datvemaybay.data.models.HangHangKhongKhuyenMai
import com.example.datvemaybay.data.models.KhuyenMaiRequest
import com.example.datvemaybay.data.models.KhuyenMaiResponse
import com.example.datvemaybay.data.models.PaymentData
import com.example.datvemaybay.data.models.SuccessResponse
import com.example.datvemaybay.databinding.FragmentThanhToanThanhCongBinding
import com.example.datvemaybay.ui.homepage.ChiTietDatChoFragment
import com.example.datvemaybay.ui.homepage.KhuyenMaiFragment
import com.example.datvemaybay.ui.homepage.NganHangFragment
import com.example.datvemaybay.ui.homepage.ThanhToanThanhCongFragment
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.DecimalFormat
import kotlin.properties.Delegates

class ThanhToanActivity : AppCompatActivity(), NganHangFragment.OnDataPass,
    KhuyenMaiFragment.OnKhuyenMaiSelectedListener {

    private lateinit var tvThanhToan: TextView
    private lateinit var btnThanhToan: Button
    private lateinit var btnKhuyenMai: Button
    private lateinit var tvKhuyenMai: TextView
    private lateinit var btnChiTietVe: Button
    private lateinit var tvLocation: TextView
    private lateinit var tvThoiGian: TextView
    private lateinit var tvTienGiam: TextView
    private lateinit var tvTongTien: TextView
    private lateinit var tvTienThanhToan: TextView
    private lateinit var confirmButton: Button

    private lateinit var bookingResponseData: BookingResponse
    private lateinit var chuyenBay_goiDichVu: ArrayList<DatChoData>
    private var tongTien by Delegates.notNull<Long>()
    private var tongTienHanhLy by Delegates.notNull<Long>()
    private lateinit var khuyenMaiRequest: KhuyenMaiRequest

    private lateinit var thanhToanRequest: PaymentData
    private var tongTienThanhToan: Long = 0
    private var maKhuyenMai: String = ""
    private var cardInfo = CardInfo()


//    private lateinit var taiKhoanThanhToan: List<ThanhToan>




    @SuppressLint("SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_thanh_toan)

        btnThanhToan = findViewById(R.id.btnThanhToan)
        tvThanhToan = findViewById(R.id.tvThanhToan)
        btnKhuyenMai = findViewById(R.id.btnKhuyenMai)
        tvKhuyenMai = findViewById(R.id.tvKhuyenMai)
        tvLocation = findViewById(R.id.tvLocation)
        tvThoiGian = findViewById(R.id.tvThoiGian)
        btnChiTietVe = findViewById(R.id.btnChiTietVe)
        tvTienGiam = findViewById(R.id.tvTienGiam)
        tvTongTien = findViewById(R.id.tvTongTien)
        tvTienThanhToan = findViewById(R.id.tvTienThanhToan)
        confirmButton = findViewById(R.id.confirmButton)

        bookingResponseData = intent.getSerializableExtra("DATA_BOOKING_RESPONSE") as BookingResponse
        chuyenBay_goiDichVu = (intent.getSerializableExtra("DATA_CHUYENBAY_GOIDICHVU") as ArrayList<DatChoData>)
        tongTien = intent.getSerializableExtra("TONG_TIEN") as Long
        tongTienHanhLy = intent.getSerializableExtra("TONG_TIEN_HANH_LY") as Long

        // Note:
        // Cài tổng hành lý cho từng khách hàng
        // làm gửi email
        // trở về package -> clear danh sách đã có

        tvTongTien.text = "VND ${formatPrice(tongTien)}"
        tvTienThanhToan.text = "VND ${formatPrice(tongTien)}"

        khuyenMaiRequest = KhuyenMaiRequest(
            hangHangKhong = bookingResponseData.thongTinDatCho.flightUpdates.map { flight ->
            flight.value.maHhk
            },
            maChuyenBay = bookingResponseData.thongTinDatCho.chuyenBay.map {
                flight -> flight.maChuyenBay
            },
            tongTien = tongTien
        )


        btnThanhToan.setOnClickListener {
            val nganHangFragment = NganHangFragment()
            nganHangFragment.show(supportFragmentManager, nganHangFragment.tag)
        }

        btnKhuyenMai.setOnClickListener {
            val khuyenMaiFragment = KhuyenMaiFragment(khuyenMaiRequest)
            replaceFragment(khuyenMaiFragment)
        }

        btnChiTietVe.setOnClickListener {
            val chiTietDatChoFragment = ChiTietDatChoFragment(
                bookingResponseData,
                chuyenBay_goiDichVu,
                tongTien,
                tongTienHanhLy)
            replaceFragment(chiTietDatChoFragment)
        }

        confirmButton.setOnClickListener {
            // Gọi API khi bấm nút thanh toán
            thanhToanRequest = PaymentData(
                tong_tien = tongTienThanhToan,
                ma_khuyen_mai = maKhuyenMai,
                phuong_thuc = "Card",
                card_info = cardInfo
            ) // Cập nhật với dữ liệu thanh toán cần thiết
            getThanhToanResponse(thanhToanRequest)
        }

    }

    override fun onDataPass(soThe: String, hoTen: String, nganHang: String) {
        Log.d("MainActivity", "Số thẻ: $soThe, Họ tên: $hoTen, Ngân hàng: $nganHang")
        tvThanhToan.text = nganHang
        if (soThe.isNotEmpty() || hoTen.isNotEmpty() || nganHang.isNotEmpty()) {
            cardInfo = CardInfo(
                so_the = soThe,
                ten_chu_the = hoTen,
                ngan_hang = nganHang
            )
        }
    }

    private fun replaceFragment(fragment: Fragment) {
        val transaction: FragmentTransaction = supportFragmentManager.beginTransaction()
        transaction.replace(android.R.id.content, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }

    @SuppressLint("SetTextI18n")
    override fun onKhuyenMaiSelected(coupon: HangHangKhongKhuyenMai) {
        Log.d("SelectedKhuyenMai", "Khuyến mãi đã chọn: ${coupon.tenKhuyenMai}")
        tvKhuyenMai.text = coupon.maKhuyenMai
        tvTienGiam.text = "- VND ${formatPrice(coupon.tienGiam)}"
        tvTienThanhToan.text = "VND ${formatPrice(tongTien - coupon.tienGiam)}"
        tongTienThanhToan = tongTien - coupon.tienGiam
        maKhuyenMai = coupon.maKhuyenMai
    }

    fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }

    private fun getThanhToanResponse(thanhToanRequest: PaymentData) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call: Call<Any> = apiService.getThanhToanResponse(bookingResponseData.bookingId, 1, thanhToanRequest)

        call.enqueue(object : Callback<Any> {
            override fun onResponse(call: Call<Any>, response: Response<Any>) {
                if (response.isSuccessful) {
                    // Kiểm tra dữ liệu trả về có phải là SuccessResponse hay không
                    val body = response.body()
                    if (body is SuccessResponse) {
                        val successFragment = ThanhToanThanhCongFragment()
                        replaceFragment(successFragment)
                    } else if (body is ErrorResponse) {
                        Toast.makeText(this@ThanhToanActivity, "Lỗi: ${body.error.toString()}", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this@ThanhToanActivity, "Lỗi: ${response.message()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Any>, t: Throwable) {
                Toast.makeText(this@ThanhToanActivity, "Lỗi kết nối: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}