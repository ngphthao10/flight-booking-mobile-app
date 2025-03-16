package com.example.datvemaybay.data.adapter

import HanhKhach
import HanhKhachResponse
import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R

class HanhKhachDataAdapter(private val passengers: List<HanhKhachResponse>) : RecyclerView.Adapter<HanhKhachDataAdapter.PassengerViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PassengerViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_passenger_info, parent, false)
        return PassengerViewHolder(view)
    }

    @SuppressLint("SetTextI18n")
    override fun onBindViewHolder(holder: PassengerViewHolder, position: Int) {
        val passenger = passengers[position]
        holder.tvTenHanhKhach.text = passenger.hoTen
        holder.tvNgaySinh.text = passenger.ngaySinh
    }

    override fun getItemCount(): Int = passengers.size

    class PassengerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvNgaySinh: TextView = itemView.findViewById(R.id.tvNgaySinh)
        val tvTenHanhKhach: TextView = itemView.findViewById(R.id.tvPassengerName)
    }
}
