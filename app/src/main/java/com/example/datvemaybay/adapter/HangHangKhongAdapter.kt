// src/main/java/com/example/datvemaybay/adapter/HangHangKhongAdapter.kt

package com.example.datvemaybay.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.response.HangHangKhongListResponse

class HangHangKhongAdapter(private var hangList: MutableList<HangHangKhongListResponse.DataItem>) :
    RecyclerView.Adapter<HangHangKhongAdapter.HangHangKhongViewHolder>() {

    // ViewHolder cho từng item
    class HangHangKhongViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvMaHHK: TextView = itemView.findViewById(R.id.tvMaHHK)
        val tvTenHHK: TextView = itemView.findViewById(R.id.tvTenHHK)
        val tvMaQG: TextView = itemView.findViewById(R.id.tvMaQG)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): HangHangKhongViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_hhk, parent, false)
        return HangHangKhongViewHolder(view)
    }

    override fun onBindViewHolder(holder: HangHangKhongViewHolder, position: Int) {
        val hangHK = hangList[position]
        holder.tvMaHHK.text = hangHK.maHHK ?: "N/A"
        holder.tvTenHHK.text = hangHK.tenHHK ?: "N/A"
        holder.tvMaQG.text = hangHK.maQG ?: "N/A"
    }

    override fun getItemCount(): Int {
        return hangList.size
    }

    // Cập nhật dữ liệu ban đầu
    fun updateData(newHangList: List<HangHangKhongListResponse.DataItem>) {
        hangList.clear()
        hangList.addAll(newHangList)
        notifyDataSetChanged()
    }

    // Thêm một item mới vào danh sách
    fun addItem(newHHK: HangHangKhongListResponse.DataItem) {
        hangList.add(0, newHHK) // Thêm vào đầu danh sách
        notifyItemInserted(0)
    }
}
