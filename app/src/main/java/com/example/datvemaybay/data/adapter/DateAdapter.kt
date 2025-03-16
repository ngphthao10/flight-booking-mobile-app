package com.example.datvemaybay.data.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R

class DateAdapter(
    private val dates: List<String>,
    private val onDateClick: (String) -> Unit,
) : RecyclerView.Adapter<DateAdapter.DateViewHolder>() {

    private var selectedPosition: Int = 0

    inner class DateViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvDate: TextView = view.findViewById(R.id.tvDate)
        val itemLayout: LinearLayout = view.findViewById(R.id.item_layout)

        fun bind(date: String) {
            tvDate.text = date

            if (position == selectedPosition) {
                itemLayout.isSelected = true // Set layout cho item được chọn
                // Áp dụng thêm thay đổi cho layout nếu cần
            } else {
                itemLayout.isSelected = false // Trở về layout chưa được chọn
                // Reset lại các thay đổi nếu cần
            }

            itemLayout.setOnClickListener {
                onDateClick(date)
                val previousPosition = selectedPosition
                selectedPosition = position

                // Thông báo cho RecyclerView rằng hai item cần update (item mới và item cũ)
                notifyItemChanged(previousPosition)
                notifyItemChanged(selectedPosition)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DateViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_date, parent, false)
        return DateViewHolder(view)
    }

    override fun onBindViewHolder(holder: DateViewHolder, position: Int) {
        holder.bind(dates[position])
    }

    override fun getItemCount(): Int = dates.size
}
