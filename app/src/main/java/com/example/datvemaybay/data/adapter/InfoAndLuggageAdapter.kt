package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.DatChoData
import java.text.SimpleDateFormat
import java.util.Locale
import kotlin.math.roundToInt

class InfoAndLuggageAdapter(
    private val bookingData: List<DatChoData>
) : RecyclerView.Adapter<InfoAndLuggageAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_booking_flight, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val bookingItem = bookingData[position]
        holder.bind(bookingItem)
    }

    override fun getItemCount() = bookingData.size

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvLoaiChuyenBay: TextView = itemView.findViewById(R.id.tvLoaiChuyen)
        private val tvThoiDiemBay: TextView = itemView.findViewById(R.id.tvDepartureTime)
        private val tvThoiGianDi: TextView = itemView.findViewById(R.id.tv_chuyen_di_time_start)
        private val tvSanBayDi: TextView = itemView.findViewById(R.id.tv_chuyen_di_location_start)
        private val tvSanBayDiID: TextView = itemView.findViewById(R.id.tv_chuyen_di_location_start_id)
        private val tvSanBayDen: TextView = itemView.findViewById(R.id.tv_chuyen_ve_location_start)
        private val tvSanBayDenID: TextView = itemView.findViewById(R.id.tv_chuyen_ve_location_start_id)
        private val tvThongTinVe: TextView = itemView.findViewById(R.id.tvThongTinVe)
        private val tvThoiGianDen: TextView = itemView.findViewById(R.id.tv_chuyen_ve_time_start)
        private val tvGoiDichVu: TextView = itemView.findViewById(R.id.tvGoiDichVu)


        @SuppressLint("SetTextI18n")
        fun bind(bookingItem: DatChoData) {
            // Nếu chuyến bay trước -> chuyến đi, chuyến sau -> chuyến về
            tvThoiDiemBay.text = "${convertDateFormat(bookingItem.chuyenBay.thoiGianDi)}  |  ${convertDecimalToText(bookingItem.chuyenBay.thoiGianBay)}"
            tvThoiGianDi.text = extractTime(bookingItem.chuyenBay.thoiGianDi)
            tvThoiGianDen.text = extractTime(bookingItem.chuyenBay.thoiGianDen)
            tvSanBayDi.text = bookingItem.chuyenBay.sanBayDi
            tvSanBayDiID.text = bookingItem.chuyenBay.maSanBayDi
            tvSanBayDen.text = bookingItem.chuyenBay.sanBayDen
            tvSanBayDenID.text = bookingItem.chuyenBay.maSanBayDen
            tvThongTinVe.text = "${bookingItem.chuyenBay.hangHangKhong}   •   ${bookingItem.chuyenBay.maChuyenBay}"
            tvGoiDichVu.text = bookingItem.goiDichVu.tenGoi

            // Gán label chuyến đi/ chuyến về
            val index = bookingData.indexOf(bookingItem)
            if (index == 0) {
                tvLoaiChuyenBay.text = "Chuyến đi"
            }
            else if (index == 1) {
                tvLoaiChuyenBay.text = "Chuyến về"
            }
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

    // Hàm chuyển tính toán số giờ (float) sang dạng "2h 30m"
    private fun convertDecimalToText(decimalHour: Float): String {
        val hours = decimalHour.toInt()
        val minutes = ((decimalHour - hours) * 60).roundToInt()
        return "${hours}h ${minutes}m"
    }
}