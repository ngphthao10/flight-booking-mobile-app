package com.example.datvemaybay.data.adapter

import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.DichVuHanhLy
import com.example.datvemaybay.data.models.HanhLyPassenger

class PassengerLuggageAdapter(private val passengerTitles: ArrayList<String>,
                              private val luggageFlightList: List<DichVuHanhLy>,
                              private val listener: PackageLuggageAdapter.OnTotalPriceChangeListener,
                              private val luggageSelectedListener: (HanhLyPassenger) -> Unit)
    : RecyclerView.Adapter<PassengerLuggageAdapter.PersonLuggageViewHolder>() {
    private var totalPrice :Long = 0

    private var passengerLuggageList: MutableList<HanhLyPassenger> = mutableListOf()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PersonLuggageViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_passenger_luggage, parent, false)
        return PersonLuggageViewHolder(view)
    }

    override fun onBindViewHolder(holder: PersonLuggageViewHolder, position: Int) {
        val passengerTitle = passengerTitles[position]
//        val passengerTitle = passengerTitles.getOrNull(position) ?: ""
        Log.d("passengertitle", "passengertitle $passengerTitle")
        holder.bind(passengerTitle)
    }

    override fun getItemCount(): Int = passengerTitles.size

    inner class PersonLuggageViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {

        private val rvPackage: RecyclerView = itemView.findViewById(R.id.rvLuggagePackage)

        fun bind(passengerTitle: String) {
            itemView.findViewById<TextView>(R.id.passengerTitles).text = passengerTitle

            rvPackage.layoutManager = LinearLayoutManager(itemView.context, LinearLayoutManager.HORIZONTAL, false)
//            rvPackage.adapter = PackageLuggageAdapter(luggageFlightList, listener, passengerTitle)
            rvPackage.adapter = PackageLuggageAdapter(luggageFlightList, listener,
                object : PackageLuggageAdapter.OnLuggageSelectedListener {
                    override fun onLuggageSelected(selectedItem: HanhLyPassenger) {
                        luggageSelectedListener(selectedItem)
                    }
                }, passengerTitle)
            Log.d("PASSENGERLUGGAGE", " PASSENGERLUGGAGE $passengerTitle $passengerTitles")
        }
    }
}