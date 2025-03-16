package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.ChuyenBay
import java.text.SimpleDateFormat
import java.util.Locale
import kotlin.math.roundToInt

class ConfirmFlightAdapter(
    private val flights: List<ChuyenBay>,
) : RecyclerView.Adapter<ConfirmFlightAdapter.ViewHolder>() {

    private var tongGiaVe: Long = 0

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_confirm_flight, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val flight = flights[position]
        holder.bind(flight)
    }

    override fun getItemCount() = flights.size

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


        @SuppressLint("SetTextI18n")
        fun bind(flight: ChuyenBay) {
             // Nếu chuyến bay trước -> chuyến đi, chuyến sau -> chuyến về
            tvThoiDiemBay.text = "${convertDateFormat(flight.thoiGianDi)}  |  ${convertDecimalToText(flight.thoiGianBay)}"
            tvThoiGianDi.text = extractTime(flight.thoiGianDi)
            tvThoiGianDen.text = extractTime(flight.thoiGianDen)
            tvSanBayDi.text = flight.sanBayDi
            tvSanBayDiID.text = flight.maSanBayDi
            tvSanBayDen.text = flight.sanBayDen
            tvSanBayDenID.text = flight.maSanBayDen
            tvThongTinVe.text = "${flight.hangHangKhong}   •   ${flight.loaiGhe}   •   ${flight.maChuyenBay}"

            // Hiển thị giá vé theo loại ghế
            tongGiaVe += when (flight.loaiGhe.lowercase()) {
                "eco" -> flight.giaVeEco
                "bus" -> flight.giaVeBus
                else -> 0
            }

            // Gán label chuyến đi/ chuyến về
            val index = flights.indexOf(flight)
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

