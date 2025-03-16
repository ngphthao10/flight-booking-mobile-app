package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.DichVuHanhLy
import com.example.datvemaybay.data.models.HanhLyPassenger
import java.text.DecimalFormat

class PackageLuggageAdapter(private val listDichVuHanhLy: List<DichVuHanhLy>,
                            private val listener: OnTotalPriceChangeListener,
                            private val luggageSelectedListener: OnLuggageSelectedListener,
                            private val passengerTitle: String
) : RecyclerView.Adapter<PackageLuggageAdapter.PackageViewHolder>() {

    private var selectedPosition = RecyclerView.NO_POSITION
//    private val selectedItems = mutableSetOf<DichVuHanhLy>()
    private var selectedItem: DichVuHanhLy? = null
    interface OnTotalPriceChangeListener {
        fun onTotalPriceChanged(totalPrice: Long)
    }

    interface OnLuggageSelectedListener {
        fun onLuggageSelected(selectedItem: HanhLyPassenger)
    }


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PackageViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_luggage_package, parent, false)
        return PackageViewHolder(view)
    }

    @SuppressLint("RecyclerView")
    override fun onBindViewHolder(
        holder: PackageViewHolder,
        position: Int
    ) {
        val luggagePackage = listDichVuHanhLy[position]
        holder.bind(luggagePackage)
        holder.itemView.isSelected = selectedPosition == position
//        holder.itemView.isSelected = selectedItems.contains(luggagePackage)


//        holder.itemView.setOnClickListener {
//            if (selectedItems.contains(luggagePackage)) {
//                selectedItems.remove(luggagePackage)
//            } else {
//                selectedItems.add(luggagePackage)
//                luggageSelectedListener.onLuggageSelected(
//                    HanhLyPassenger(luggagePackage, passengerTitle)
//                )
//            }
//            notifyItemChanged(position)
//            updateTotalPrice()
//        }

//        holder.itemView.setOnClickListener {
//            // Nếu đã chọn item này, bỏ chọn nó
//            if (selectedItems.contains(luggagePackage)) {
//                selectedItems.remove(luggagePackage)
//                selectedPosition = RecyclerView.NO_POSITION
//            } else {
//                // Nếu chọn item mới, bỏ chọn item trước đó
//                val previousSelectedPosition = selectedPosition
//                selectedItems.clear() // Xóa tất cả item đã chọn
//                selectedItems.add(luggagePackage) // Thêm item mới vào danh sách đã chọn
//                selectedPosition = position // Cập nhật vị trí đã chọn
//
//                // Cập nhật giao diện cho item trước đó (nếu có)
//                if (previousSelectedPosition != RecyclerView.NO_POSITION) {
//                    notifyItemChanged(previousSelectedPosition)
//                }
//            }
//
//            // Cập nhật giao diện cho item hiện tại
//            notifyItemChanged(position)
//            updateTotalPrice()
//        }

        holder.itemView.setOnClickListener {
            if (selectedPosition == position) {
                // Unselect the item
                selectedPosition = RecyclerView.NO_POSITION
                selectedItem = null
            } else {
                // Select new item
                val previousSelectedPosition = selectedPosition
                selectedPosition = position
                selectedItem = luggagePackage

                // Update UI for previous selected item
                if (previousSelectedPosition != RecyclerView.NO_POSITION) {
                    notifyItemChanged(previousSelectedPosition)
                }
            }
            notifyItemChanged(position)
            updateTotalPrice()
            updateSelectedLuggage()
        }

    }

    override fun getItemCount(): Int = listDichVuHanhLy.size

    inner class PackageViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {

        private val luggageInfo: TextView = itemView.findViewById(R.id.luggageInfo)

        @SuppressLint("SetTextI18n")
        fun bind(luggagePackage: DichVuHanhLy) {
            luggageInfo.text =
                "+${luggagePackage.weight} kg\nVND ${formatPrice(luggagePackage.price)}"
//            itemView.isSelected = selectedItems.contains(luggagePackage)
        }

        init {
            itemView.setOnClickListener {
                notifyItemChanged(selectedPosition) // Reset previous selected item
                selectedPosition = adapterPosition
                notifyItemChanged(selectedPosition) // Highlight new selected item
            }
        }
    }

    // Hàm format tiền
    fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }

//    private fun updateTotalPrice() {
//        val totalPrice = selectedItems.sumOf { it.price }
//        listener.onTotalPriceChanged(totalPrice)
//    }

    private fun updateTotalPrice() {
        val totalPrice = selectedItem?.price ?: 0L
        listener.onTotalPriceChanged(totalPrice)
    }


    private fun updateSelectedLuggage() {
        selectedItem?.let {
            luggageSelectedListener.onLuggageSelected(HanhLyPassenger(it, passengerTitle))
        }
    }
}