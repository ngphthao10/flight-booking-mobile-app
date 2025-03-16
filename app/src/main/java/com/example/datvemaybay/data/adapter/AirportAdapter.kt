package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.text.TextUtils.concat
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.SanBay

class AirportAdapter(private val listener: (SanBay) -> Unit) : RecyclerView.Adapter<AirportAdapter.AirportViewHolder>() {

    private var airportList: List<SanBay> = emptyList()

    @SuppressLint("NotifyDataSetChanged")
    fun setData(data: List<SanBay>) {
        airportList = data
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AirportViewHolder {
        val itemView = LayoutInflater.from(parent.context).inflate(R.layout.item_airport, parent, false)
        return AirportViewHolder(itemView)
    }

    override fun onBindViewHolder(holder: AirportViewHolder, position: Int) {
        val item = airportList[position]
        holder.bind(item, listener)
    }

    override fun getItemCount(): Int {
        return airportList.size
    }

    class AirportViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val maSB: TextView = itemView.findViewById(R.id.airport_code)
        private val tenSB: TextView = itemView.findViewById(R.id.airport_name)
        private val location: TextView = itemView.findViewById(R.id.airport_location)
        private val loaiSB: TextView = itemView.findViewById(R.id.category)

        val parts = location.text.split(",")

        fun bind(airport: SanBay, listener: (SanBay) -> Unit) {
            maSB.text = airport.maSanBay
            tenSB.text = airport.tenSanBay
            location.text = concat(airport.thanhPho, ", ", airport.tenQG)
            loaiSB.text = airport.loaiSB
            itemView.setOnClickListener { listener(airport) }
        }
    }


}
