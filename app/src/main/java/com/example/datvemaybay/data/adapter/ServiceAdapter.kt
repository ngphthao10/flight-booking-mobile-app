package com.example.datvemaybay.data.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.DichVu

class ServiceAdapter(private val listDichVu: List<DichVu>) : RecyclerView.Adapter<ServiceAdapter.ServiceViewHolder>() {

    // Tạo ViewHolder cho từng mục trong RecyclerView
    inner class ServiceViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvMoTaGoi: TextView = itemView.findViewById(R.id.tvMoTaGoi)
    }

    // Tạo và trả về ViewHolder cho mỗi item
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ServiceViewHolder {
        val itemView = LayoutInflater.from(parent.context).inflate(R.layout.item_service, parent, false)
        return ServiceViewHolder(itemView)
    }

    // Gắn dữ liệu vào các view trong ViewHolder
    override fun onBindViewHolder(holder: ServiceViewHolder, position: Int) {
        val dichVu = listDichVu[position]
        holder.tvMoTaGoi.text = dichVu.chiTiet
    }

    // Trả về số lượng item trong danh sách
    override fun getItemCount(): Int {
        return listDichVu.size
    }
}
