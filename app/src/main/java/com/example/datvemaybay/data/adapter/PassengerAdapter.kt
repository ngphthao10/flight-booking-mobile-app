package com.example.datvemaybay.data.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R

class PassengerAdapter(private val passengerTitles: List<String>,
                       private val onItemClick: (String) -> Unit) :
    RecyclerView.Adapter<PassengerAdapter.PassengerViewHolder>() {

    inner class PassengerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val titleTextView: TextView = itemView.findViewById(R.id.edtHoTen)

        init {
            itemView.setOnClickListener {
                val position = adapterPosition
                val passengerTitle = passengerTitles[position]
                onItemClick(passengerTitle)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PassengerViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_passenger, parent, false)
        return PassengerViewHolder(view)
    }

    override fun onBindViewHolder(holder: PassengerViewHolder, position: Int) {
        holder.titleTextView.text = passengerTitles[position]
    }

    override fun getItemCount(): Int = passengerTitles.size
}
