package com.example.datvemaybay.ui.homepage

import BookingResponse
import FlightBooking
import android.annotation.SuppressLint
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.adapter.HanhKhachDataAdapter
import com.example.datvemaybay.data.models.DatChoData
import com.example.datvemaybay.data.models.GoiDichVu
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.Locale
import kotlin.math.roundToInt

class ChiTietDatChoFragment(
    private val bookingDataResponse: BookingResponse,
    private val chuyenBayGoiDichVu: List<DatChoData>,
    private val tongTien: Long,
    private val tongTienHanhLy: Long

) : Fragment() {

    private lateinit var tvStartTimeDi: TextView
    private lateinit var tvStartTimeVe: TextView
    private lateinit var tvEndTimeDi: TextView
    private lateinit var tvEndTimeVe: TextView
    private lateinit var tvDiemDenDi: TextView
    private lateinit var tvDiemDenVe: TextView
    private lateinit var tvDiemDiDi: TextView
    private lateinit var tvDiemDiVe: TextView
    private lateinit var tvDiemDiCodeDi: TextView
    private lateinit var tvDiemDiCodeVe: TextView
    private lateinit var tvDiemDenCodeDi: TextView
    private lateinit var tvDiemDenCodeVe: TextView
    private lateinit var tvChiTietKhacDi: TextView
    private lateinit var tvChiTietKhacVe: TextView
    private lateinit var tvGoiDichVuDi: TextView
    private lateinit var tvGoiDichVuVe: TextView
    private lateinit var tvThoiGianDi: TextView
    private lateinit var tvThoiGianVe: TextView

    private lateinit var rvPassenger: RecyclerView
    private lateinit var chuyenVeContainer: LinearLayout
    private lateinit var btnCancel: ImageButton

    private lateinit var tvTongTien: TextView
    private lateinit var tvTienHanhLy: TextView
    private lateinit var tvTienVe: TextView
    private lateinit var labelTienVe: TextView

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_chi_tiet_dat_cho, container, false)

        // Initializing views
        tvStartTimeDi = view.findViewById(R.id.tv_chuyen_di_time_start)
        tvStartTimeVe = view.findViewById(R.id.tv_chuyen_ve_time_start)
        tvEndTimeDi = view.findViewById(R.id.tv_chuyen_di_time_end)
        tvEndTimeVe = view.findViewById(R.id.tv_chuyen_ve_time_end)
        tvDiemDenDi = view.findViewById(R.id.tv_chuyen_di_location_end)
        tvDiemDenVe = view.findViewById(R.id.tv_chuyen_ve_location_end)
        tvDiemDiDi = view.findViewById(R.id.tv_chuyen_di_location_start)
        tvDiemDiVe = view.findViewById(R.id.tv_chuyen_ve_location_start)
        tvDiemDiCodeDi = view.findViewById(R.id.tv_chuyen_di_location_start_id)
        tvDiemDenCodeDi = view.findViewById(R.id.tv_chuyen_di_location_end_id)
        tvChiTietKhacDi = view.findViewById(R.id.tvThongTinVeDi)
        tvChiTietKhacVe = view.findViewById(R.id.tvThongTinVeVe)
        tvDiemDiCodeVe = view.findViewById(R.id.tv_chuyen_ve_location_start_id)
        tvDiemDenCodeVe = view.findViewById(R.id.tv_chuyen_ve_location_end_id)
        tvGoiDichVuDi = view.findViewById(R.id.tvGoiDichVuDi)
        tvGoiDichVuVe = view.findViewById(R.id.tvGoiDichVuVe)
        tvThoiGianDi = view.findViewById(R.id.tvThoiGianDi)
        tvThoiGianVe = view.findViewById(R.id.tvThoiGianVe)

        rvPassenger = view.findViewById(R.id.rvPassenger)
        chuyenVeContainer = view.findViewById(R.id.chuyenVeContainer)
        btnCancel = view.findViewById(R.id.btnCancel)

        tvTongTien = view.findViewById(R.id.tongTien)
        tvTienHanhLy = view.findViewById(R.id.tienHanhLy)
        tvTienVe = view.findViewById(R.id.tienVe)
        labelTienVe = view.findViewById(R.id.labelTienVe)


        // Set data for the flight info and passenger list
        populateFlightInfo(view)
        populatePassengerList()
        setAllPrice()

        btnCancel.setOnClickListener {
            parentFragmentManager.popBackStack()
        }

        return view
    }

    @SuppressLint("SetTextI18n")
    private fun populateFlightInfo(view: View) {
        // Set flight info for outbound flight
        val outboundFlight = chuyenBayGoiDichVu[0].chuyenBay
        val outboundPackage = chuyenBayGoiDichVu[0].goiDichVu

        // Gán dữ liệu chuyến bay đi
        tvThoiGianDi.text = "${convertDateFormat(outboundFlight.thoiGianDi)}  |  ${convertDecimalToText(outboundFlight.thoiGianBay)}"
        tvStartTimeDi.text = extractTime(outboundFlight.thoiGianDi)
        tvEndTimeDi.text = extractTime(outboundFlight.thoiGianDen)
        tvChiTietKhacDi.text = "${outboundFlight.hangHangKhong}   •   ${outboundFlight.maChuyenBay}"
        tvDiemDiCodeDi.text = outboundFlight.maSanBayDi
        tvDiemDenCodeDi.text = outboundFlight.maSanBayDen
        tvDiemDiDi.text = outboundFlight.sanBayDi
        tvDiemDenDi.text = outboundFlight.sanBayDen
        tvGoiDichVuDi.text = outboundPackage.tenGoi

        // Check if return flight exists
        if (chuyenBayGoiDichVu.size > 1) {
            chuyenVeContainer.visibility = View.VISIBLE
            val returnFlight = chuyenBayGoiDichVu[1].chuyenBay
            val returnPackage = chuyenBayGoiDichVu[1].goiDichVu

            tvThoiGianDi.text = "${convertDateFormat(returnFlight.thoiGianDi)}  |  ${convertDecimalToText(returnFlight.thoiGianBay)}"
            tvStartTimeDi.text = extractTime(returnFlight.thoiGianDi)
            tvEndTimeDi.text = extractTime(returnFlight.thoiGianDen)
            tvChiTietKhacDi.text = "${returnFlight.hangHangKhong}   •   ${returnFlight.maChuyenBay}"
            tvDiemDiCodeDi.text = returnFlight.maSanBayDi
            tvDiemDenCodeDi.text = returnFlight.maSanBayDen
            tvDiemDiDi.text = returnFlight.sanBayDi
            tvDiemDenDi.text = returnFlight.sanBayDen
            tvGoiDichVuDi.text = returnPackage.tenGoi
        }


        val temp = bookingDataResponse.thongTinDatCho.hanhKhach.map { it.loaiHk }
        val loaiHkCount = temp.groupingBy { it }.eachCount()
        val result = loaiHkCount.filter { it.value > 0 } // Lọc bỏ loại hành khách có số lượng bằng 0
            .map { (loaiHk, count) -> "Tiền vé ($loaiHk) x $count:" }
            .joinToString(" ")
        labelTienVe.text = result
    }

    private fun populatePassengerList() {
        val passengerAdapter = HanhKhachDataAdapter(bookingDataResponse.thongTinDatCho.hanhKhach)
        rvPassenger.layoutManager = LinearLayoutManager(requireContext())
        rvPassenger.adapter = passengerAdapter
    }

    private fun setAllPrice() {
        tvTongTien.text = formatPrice(tongTien)
        tvTienHanhLy.text = formatPrice(tongTienHanhLy)
        tvTienVe.text = formatPrice(tongTien - tongTienHanhLy)
    }

    // Hàm chuyển tính toán số giờ (float) sang dạng "2h 30m"
    private fun convertDecimalToText(decimalHour: Float): String {
        val hours = decimalHour.toInt()
        val minutes = ((decimalHour - hours) * 60).roundToInt()
        return "${hours}h ${minutes}m"
    }

    // Hảm lấy HH:mm trong yyyy-MM-dd'T'HH:mm:ss
    fun extractTime(dateTime: String): String {
        val inputFormat =
            android.icu.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        val outputFormat = android.icu.text.SimpleDateFormat("HH:mm", Locale.getDefault())

        return try {
            val date = inputFormat.parse(dateTime)
            outputFormat.format(date)
        } catch (e: Exception) {
            "N/A"
        }
    }

    // Hảm lấy EEE, dd MMM yyyy trong yyyy-MM-dd'T'HH:mm:ss
    fun convertDateFormat(inputDate: String): String? {
        val inputFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.ENGLISH)
        val outputFormat = SimpleDateFormat("EEE, dd MMM yyyy", Locale.ENGLISH)

        return try {
            val date = inputFormat.parse(inputDate)
            date?.let { outputFormat.format(it) }
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    // Hàm format tiền
    fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,### VND")
            formatter.format(it)
        } ?: "N/A"
    }
//
//    companion object {
//        fun newInstance(bookingData: FlightBooking): ChiTietDatChoFragment {
//            val fragment = ChiTietDatChoFragment(flightBookingData)
//            val bundle = Bundle()
//            bundle.putParcelable("BOOKING_DATA", bookingData)
//            fragment.arguments = bundle
//            return fragment
//        }
//    }
}
