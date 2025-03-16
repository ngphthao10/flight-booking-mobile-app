package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.icu.text.SimpleDateFormat
import android.text.TextUtils.concat
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.ChuyenBay
import com.example.datvemaybay.data.models.SanBay
import java.text.DecimalFormat
import java.util.Locale
import kotlin.math.roundToInt

class FlightAdapter(private val onItemClick: ((ChuyenBay) -> Unit)) : RecyclerView.Adapter<FlightAdapter.FlightViewHolder>() {

    private var flightList: List<ChuyenBay> = emptyList()

    @SuppressLint("NotifyDataSetChanged")
    fun setData(data: List<ChuyenBay>) {
        flightList = data
        notifyDataSetChanged()
    }

    fun isDataEmpty(): Boolean {
        return flightList.isEmpty()
    }

    // ViewHolder để giữ view cho từng item
    class FlightViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val hangHangKhongText: TextView = itemView.findViewById(R.id.tvAirline)
        val thoiGianDiText: TextView = itemView.findViewById(R.id.tvDepartureTime)
        val thoiGianDenText: TextView = itemView.findViewById(R.id.tvArrivalTime)
        val thoiGianBayText: TextView = itemView.findViewById(R.id.tvDuration)
        val giaVeText: TextView = itemView.findViewById(R.id.tvPrice)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FlightViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_flight, parent, false)

        return FlightViewHolder(view)
    }

    @SuppressLint("SetTextI18n")
    override fun onBindViewHolder(holder: FlightViewHolder, position: Int) {
        val flight = flightList[position]
        Log.d("FlightAdapter", "Binding data: $flight")
        holder.hangHangKhongText.text = flight.hangHangKhong
        holder.thoiGianBayText.text = convertDecimalToText(flight.thoiGianBay)
        holder.thoiGianDiText.text = extractTime(flight.thoiGianDi)
        holder.thoiGianDenText.text = extractTime(flight.thoiGianDen)
        holder.itemView.setOnClickListener {
            Log.d("FlightAdapter", "CardView được bấm: ${flight.maChuyenBay}")
            onItemClick.invoke(flight)
        }

        // Hiển thị giá vé phù hợp với loại ghế
        val giaVe = when (flight.loaiGhe) {
            "ECO" -> flight.giaVeEco
            "BUS" -> flight.giaVeBus
            else -> null
        }
        holder.giaVeText.text = formatPrice(giaVe)
        Log.d("FlightAdapter", "Price: ${giaVe?.toString() ?: "N/A"}")
    }

    override fun getItemCount(): Int = flightList.size

    fun extractTime(dateTime: String): String {
        val inputFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        val outputFormat = SimpleDateFormat("HH:mm", Locale.getDefault())

        return try {
            val date = inputFormat.parse(dateTime)
            outputFormat.format(date)
        } catch (e: Exception) {
            "N/A"
        }
    }

    private fun convertDecimalToText(decimalHour: Float): String {
        val hours = decimalHour.toInt()
        val minutes = ((decimalHour - hours) * 60).roundToInt()

        // Tạo chuỗi định dạng "2h 30m"
        return "${hours}h ${minutes}m"
    }

    private fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it) + " VND"
        } ?: "N/A"
    }
}